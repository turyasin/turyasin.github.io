from typing import Any, Dict, Optional
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from .base_agent import BaseAgent
from ..core.vector_store import VectorStoreManager
from ..core.file_processor import FileProcessor
from ..config import config

class HRAssistant(BaseAgent):
    def __init__(self):
        self.vector_store_manager = VectorStoreManager()
        self.file_processor = FileProcessor()
        self.llm = ChatOpenAI(
            model_name=config.DEFAULT_MODEL,
            temperature=config.TEMPERATURE,
            openai_api_key=config.OPENAI_API_KEY
        )
        
        # In-memory storage for chat histories (for MVP)
        # In production, this should be Redis or Database
        self.memories = {}

    def _get_memory(self, session_id: str):
        if session_id not in self.memories:
            self.memories[session_id] = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
        return self.memories[session_id]

    async def process_message(self, message: str, session_id: str, file: Optional[bytes] = None, filename: Optional[str] = None) -> Dict[str, Any]:
        
        # 1. Process and upload file if exists
        if file and filename:
            documents = self.file_processor.process_pdf(file, filename)
            # Add session_id to metadata to filter by user/session if needed
            for doc in documents:
                doc.metadata["session_id"] = session_id
            
            self.vector_store_manager.add_documents(documents)
            
            # If message is empty but file is uploaded, generate a summary prompt
            if not message:
                message = f"I have uploaded a file named {filename}. Please summarize it."

        # 2. Get Memory
        memory = self._get_memory(session_id)

        # 3. Create Chain
        # We recreate chain to ensure fresh retriever state if needed, 
        # though typically retriever is stateless.
        retriever = self.vector_store_manager.as_retriever()
        
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever,
            memory=memory,
            verbose=True
        )

        # 4. Run Chain
        # We append a system instruction to the query to enforce Turkish language
        system_instruction = "\n(Lütfen cevabı her zaman Türkçe ver. Sen yardımsever bir İK asistanısın.)"
        full_query = message + system_instruction
        
        result = qa_chain.invoke({"question": full_query})
        
        return {
            "text": result["answer"],
            "source_documents": [doc.metadata for doc in result.get("source_documents", [])]
        }

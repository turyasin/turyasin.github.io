from typing import List
from io import BytesIO
from pypdf import PdfReader
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from ..config import config

class FileProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP
        )

    def process_pdf(self, file_content: bytes, filename: str) -> List[Document]:
        """
        Extract text from PDF bytes and split into chunks
        """
        pdf_file = BytesIO(file_content)
        pdf_reader = PdfReader(pdf_file)
        
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
            
        # Create a single document first
        doc = Document(
            page_content=text,
            metadata={"source": filename}
        )
        
        # Split into chunks
        return self.text_splitter.split_documents([doc])

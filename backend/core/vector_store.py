from langchain_community.vectorstores import SupabaseVectorStore
from langchain_openai import OpenAIEmbeddings
from supabase.client import create_client, Client
from ..config import config

class VectorStoreManager:
    def __init__(self):
        self.supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
        self.embeddings = OpenAIEmbeddings(
            model=config.EMBEDDING_MODEL,
            openai_api_key=config.OPENAI_API_KEY
        )
        self.vector_store = SupabaseVectorStore(
            client=self.supabase,
            embedding=self.embeddings,
            table_name="documents",
            query_name="match_documents"
        )

    def add_documents(self, documents):
        return self.vector_store.add_documents(documents)

    def as_retriever(self):
        return self.vector_store.as_retriever()

    def similarity_search(self, query, k=4):
        return self.vector_store.similarity_search(query, k=k)

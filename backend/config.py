# Backend Configuration
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Supabase
    SUPABASE_URL = os.getenv("SUPABASE_URL", "https://camyogwbseuxfrjxnjzw.supabase.co")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    
    # Server
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    
    # CORS
    ALLOWED_ORIGINS = [
        "https://turyasin.github.io",
        "http://localhost:3000",
        "http://localhost:5173"
    ]
    
    # Vector Store
    EMBEDDING_MODEL = "text-embedding-3-small"
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    
    # LLM
    DEFAULT_MODEL = "gpt-3.5-turbo"
    TEMPERATURE = 0.7
    MAX_TOKENS = 500

config = Config()

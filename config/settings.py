from dotenv import load_dotenv
import os

load_dotenv()

# ==========================================================
# API Keys
# ==========================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

VAPI_PUBLIC_KEY = os.getenv("VAPI_PUBLIC_KEY")
VAPI_PRIVATE_KEY = os.getenv("VAPI_PRIVATE_KEY")
VAPI_ASSISTANT_ID = os.getenv("VAPI_ASSISTANT_ID")

# ==========================================================
# Backend
# ==========================================================

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:5000",
)

VAPI_API_BASE_URL = os.getenv(
    "VAPI_API_BASE_URL",
    "https://api.vapi.ai",
)

# ==========================================================
# Qdrant
# ==========================================================

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

QDRANT_COLLECTION = os.getenv(
    "QDRANT_COLLECTION",
    "rag_voice_knowledge_base",
)

# ==========================================================
# Models
# ==========================================================

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile",
)

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "gemini-embedding-001",
)

# ==========================================================
# RAG
# ==========================================================

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K = 4

os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

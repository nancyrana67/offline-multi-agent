import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
UPLOADS_DIR = PROJECT_ROOT / "uploads"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
PROMPTS_DIR = PROJECT_ROOT / "prompts"

# Create directories
for dir_path in [DATA_DIR, UPLOADS_DIR, OUTPUTS_DIR, PROMPTS_DIR]:
    dir_path.mkdir(exist_ok=True)

# Ollama Configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "mistral")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")

# Agent Configuration
AGENT_TIMEOUT = 300  # 5 minutes
MAX_RETRIES = 3
RETRY_DELAY = 2

# RAG Configuration
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K_RETRIEVAL = 5

# Memory Configuration
MAX_CONVERSATION_TURNS = 100
MEMORY_RETENTION_DAYS = 30

# UI Configuration
UI_HOST = "127.0.0.1"
UI_PORT = 8000
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Model Parameters
TEMPERATURE = 0.7
TOP_P = 0.9
TOP_K = 40

# Performance
BATCH_SIZE = 10
MAX_CONCURRENT_AGENTS = 5

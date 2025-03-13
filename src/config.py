import os
from dotenv import load_dotenv

load_dotenv()  

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

CHUNK_SIZE = 6 # Sentences per chunk
CHUNK_OVERLAP = 2 # Sentence overlap per chunk
VECTOR_DB_PATH = "vectorDB"
JSON_PATH = "json_files"
TOP_K_RETRIEVAL = 3  # Number of relevant passages to retrieve per book. 

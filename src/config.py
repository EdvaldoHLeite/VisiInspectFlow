# src/config.py
import os

from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Langfuse Observability
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
LANGFUSE_HOST = os.getenv("LANGFUSE_HOST")

# Agent Configuration
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL")
USE_LOCAL_OLLAMA = os.getenv("USE_LOCAL_OLLAMA")

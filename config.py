"""
Configuration module for the Agno AI agent.
Handles loading environment variables and other configuration settings.
"""

import os

# Try to load dotenv if available
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("Loaded environment variables from .env file")
except ImportError:
    print("dotenv module not available, trying to load .env file manually")
    # Simple .env file parser
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    os.environ[key] = value
                    print(f"Manually loaded {key} from .env file")

# Groq API configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("GROQ_API_KEY not found in environment variables")
    print("Please set GROQ_API_KEY in your .env file")
    GROQ_API_KEY = ""  # Empty string as fallback

# Default model to use with Groq
DEFAULT_GROQ_MODEL = "llama3-70b-8192"

# Gemini API configuration (kept for backward compatibility)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("GEMINI_API_KEY not found in environment variables")
    print("Please set GEMINI_API_KEY in your .env file")
    GEMINI_API_KEY = ""  # Empty string as fallback

# Default model to use with Gemini
DEFAULT_GEMINI_MODEL = "gemini-1.5-pro"

# PostgreSQL configuration
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE", "postgres")

# Agent configuration
AGENT_NAME = "Agno"
AGENT_VERSION = "0.1.0"

# Maximum token limits
MAX_INPUT_TOKENS = 4000
MAX_OUTPUT_TOKENS = 1000

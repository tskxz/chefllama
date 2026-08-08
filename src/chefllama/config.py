import os
from dotenv import load_dotenv

load_dotenv()

DEFAULT_CHAT_MODEL = os.getenv("CHEF_CHAT_MODEL", "ollama:llama3.2")
DEFAULT_VISION_MODEL = os.getenv("CHEF_VISION_MODEL", "llava:latest")
DEFAULT_THREAD_ID = "cli_session_1"
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")

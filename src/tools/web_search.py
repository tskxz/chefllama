from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

from langchain.tools import tool
from typing import Dict, Any

tavily_client = TavilyClient()

@tool
def pesquisa_web(query: str) -> Dict[str, Any]:
    """Pesquisa na web para ter informacao"""
    return tavily_client.search(query)

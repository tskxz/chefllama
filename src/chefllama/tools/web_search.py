import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from tavily import TavilyClient

load_dotenv()

@tool
def pesquisa_web(query: str) -> str:
    """Pesquisa na web por receitas culinarias, combinacoes de ingredientes e tecnicas de confeccao."""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "Erro: TAVILY_API_KEY nao configurada no ficheiro .env."
    
    try:
        tavily_client = TavilyClient(api_key=api_key)
        response = tavily_client.search(query=query, max_results=3, search_depth="basic")
        results = response.get("results", [])
        if not results:
            return "Nenhuma receita encontrada para a pesquisa indicada."
        
        formatted_results = []
        for r in results:
            title = r.get("title", "Sem titulo")
            url = r.get("url", "")
            content = r.get("content", "")
            formatted_results.append(f"Titulo: {title}\nFonte: {url}\nResumo: {content}")
        
        return "\n\n---\n\n".join(formatted_results)
    except Exception as exc:
        return f"Erro ao realizar pesquisa na web: {exc}"

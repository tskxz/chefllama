from typing import Optional
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from .config import DEFAULT_CHAT_MODEL, DEFAULT_THREAD_ID
from .prompts import CHEF_SYSTEM_PROMPT
from .tools.web_search import pesquisa_web

def create_chef_agent(
    model: str = DEFAULT_CHAT_MODEL,
    checkpointer: Optional[InMemorySaver] = None
):
    """Cria e compila o grafo do agente ChefLLama com ferramentas e suporte a memoria."""
    if checkpointer is None:
        checkpointer = InMemorySaver()
    
    return create_agent(
        model=model,
        tools=[pesquisa_web],
        system_prompt=CHEF_SYSTEM_PROMPT,
        checkpointer=checkpointer
    )

chef_agent = create_chef_agent()

def run_chef_query(agent, prompt: str, thread_id: str = DEFAULT_THREAD_ID) -> str:
    """Envia a mensagem do utilizador para o agente compilado e devolve a resposta final."""
    config = {"configurable": {"thread_id": thread_id}}
    response = agent.invoke(
        {
            "messages": [
                HumanMessage(content=prompt)
            ]
        },
        config
    )
    last_message = response["messages"][-1]
    return str(last_message.content)

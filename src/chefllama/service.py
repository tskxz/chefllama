from chefllama.agent import run_chef_query
from chefllama.config import DEFAULT_THREAD_ID
from chefllama.vision import analyze_fridge_image

def process_fridge_image_and_suggest(
    agent,
    image_path: str,
    extra_prompt: str = "",
    thread_id: str = DEFAULT_THREAD_ID
) -> str:
    """Analisa a foto com LLaVA e encaminha os ingredientes identificados para o ChefLLama."""
    print("ChefLLama a analisar a imagem com o modelo LLaVA...")
    detected_items = analyze_fridge_image(image_path)
    
    print("\nIngredientes identificados pelo LLaVA:")
    print(detected_items)
    print("\nA pesquisar na web e a estruturar sugestoes de receitas...")
    
    agent_input = (
        f"Analisei a foto do frigorifico/despensa e identifiquei os seguintes ingredientes e alimentos:\n"
        f"{detected_items}\n\n"
        f"Com base nestes ingredientes identificados, pesquisa na web e apresenta 2 a 3 opcoes de receitas praticas sem desperdicio."
    )
    if extra_prompt:
        agent_input += f"\nRequisitos adicionais do utilizador: {extra_prompt}"
    
    return run_chef_query(agent, agent_input, thread_id=thread_id)

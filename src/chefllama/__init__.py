import argparse
import os
import sys
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from .load_agent import chef_agent, create_chef_agent
from .vision import analyze_fridge_image

# Ensure proper standard stream encoding across operating systems
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

load_dotenv()

def run_chef_query(agent, prompt: str, thread_id: str = "default_session") -> str:
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

def process_fridge_image_and_suggest(
    agent,
    image_path: str,
    extra_prompt: str = "",
    thread_id: str = "default_session"
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

def main() -> None:
    """Ponto de entrada da aplicacao CLI com suporte a texto, analise multimodal de imagens e memoria."""
    parser = argparse.ArgumentParser(description="ChefLLama - O teu Chef Pessoal com IA")
    parser.add_argument("--imagem", "-i", dest="image_path", help="Caminho da foto do frigorifico ou despensa a analisar com LLaVA.")
    parser.add_argument("query", nargs="*", help="Texto ou ingredientes adicionais a fornecer ao ChefLLama.")
    
    args = parser.parse_args()
    user_query = " ".join(args.query).strip() if args.query else ""
    thread_id = "cli_session_1"

    # Direct execution mode with image and/or text argument
    if args.image_path or user_query:
        if args.image_path:
            if not os.path.exists(args.image_path):
                print(f"Erro: O ficheiro de imagem '{args.image_path}' nao foi encontrado.")
                return
            try:
                answer = process_fridge_image_and_suggest(
                    chef_agent,
                    args.image_path,
                    extra_prompt=user_query,
                    thread_id=thread_id
                )
                print(f"\nChefLLama:\n{answer}\n")
            except Exception as exc:
                print(f"\nErro durante a analise da imagem: {exc}")
            return
        else:
            print(f"Utilizador: {user_query}\n")
            print("ChefLLama a pesquisar e a elaborar receitas...")
            try:
                answer = run_chef_query(chef_agent, user_query, thread_id=thread_id)
                print(f"\nChefLLama:\n{answer}\n")
            except Exception as exc:
                print(f"\nOcorreu um erro: {exc}")
            return

    # Interactive chat loop
    print("Bem-vindo ao ChefLLama - O teu Chef Pessoal")
    print("Indica os ingredientes disponiveis no teu frigorifico ou despensa,")
    print("ou escreve 'imagem <caminho>' para analisar uma foto com LLaVA.")
    print("Escreve 'sair' ou 'q' para terminar.\n")

    while True:
        try:
            user_input = input("Tu: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("sair", "exit", "quit", "q"):
                print("\nChefLLama: Ate a proxima e bom apetite!")
                break

            # Check if user invoked image command in interactive session
            if user_input.lower().startswith(("imagem ", "/imagem ", "foto ", "/foto ")):
                parts = user_input.split(maxsplit=1)
                if len(parts) > 1:
                    img_path = parts[1].strip().strip('"').strip("'")
                    if os.path.exists(img_path):
                        answer = process_fridge_image_and_suggest(chef_agent, img_path, thread_id=thread_id)
                        print(f"\nChefLLama:\n{answer}\n")
                    else:
                        print(f"\nErro: Ficheiro de imagem '{img_path}' nao encontrado.\n")
                else:
                    print("\nPor favor especifica o caminho da imagem (ex: imagem ./foto.jpg)\n")
                print("-" * 60)
                continue

            print("\nChefLLama a processar o pedido...")
            answer = run_chef_query(chef_agent, user_input, thread_id=thread_id)
            print(f"\nChefLLama:\n{answer}\n")
            print("-" * 60)
        except (KeyboardInterrupt, EOFError):
            print("\n\nChefLLama: Ate breve!")
            break
        except Exception as exc:
            print(f"\nErro ao processar o pedido: {exc}\n")

if __name__ == "__main__":
    main()

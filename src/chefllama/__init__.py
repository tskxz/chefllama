import sys
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from .load_agent import chef_agent, create_chef_agent

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

def main() -> None:
    """Ponto de entrada da aplicacao CLI com ciclo de conversacao interativo."""
    print("=" * 60)
    print("Bem-vindo ao ChefLLama - O teu Chef Pessoal")
    print("=" * 60)
    print("Indica os ingredientes disponiveis no teu frigorifico ou despensa,")
    print("e recebes sugestoes de receitas praticas sem desperdicio.")
    print("Escreve 'sair' ou 'q' para terminar.\n")

    # Handle direct CLI arguments if provided
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
        print(f"Utilizador: {user_input}\n")
        print("ChefLLama a pesquisar e a elaborar receitas...")
        try:
            answer = run_chef_query(chef_agent, user_input)
            print(f"\n{answer}\n")
        except Exception as exc:
            print(f"\nOcorreu um erro: {exc}")
        return

    thread_id = "cli_session_1"

    while True:
        try:
            user_input = input("Tu: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("sair", "exit", "quit", "q"):
                print("\nChefLLama: Ate a proxima e bom apetite!")
                break

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

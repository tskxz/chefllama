import argparse
import os
import sys
from .agent import chef_agent, run_chef_query
from .config import DEFAULT_THREAD_ID
from .service import process_fridge_image_and_suggest

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

def parse_arguments():
    """Define e processa os argumentos de linha de comandos da aplicacao."""
    parser = argparse.ArgumentParser(description="ChefLLama - O teu Chef Pessoal com IA")
    parser.add_argument(
        "--imagem", "-i",
        dest="image_path",
        help="Caminho da foto do frigorifico ou despensa a analisar com LLaVA."
    )
    parser.add_argument(
        "query",
        nargs="*",
        help="Texto ou ingredientes adicionais a fornecer ao ChefLLama."
    )
    return parser.parse_args()

def handle_direct_execution(args, thread_id: str = DEFAULT_THREAD_ID) -> int:
    """Executa consultas diretas via argumentos de linha de comandos e devolve o codigo de saida."""
    user_query = " ".join(args.query).strip() if args.query else ""
    
    if args.image_path:
        if not os.path.isfile(args.image_path):
            print(f"Erro: O ficheiro de imagem '{args.image_path}' nao foi encontrado ou e invalido.")
            return 1
        try:
            answer = process_fridge_image_and_suggest(
                chef_agent,
                args.image_path,
                extra_prompt=user_query,
                thread_id=thread_id
            )
            print(f"\nChefLLama:\n{answer}\n")
            return 0
        except Exception as exc:
            print(f"\nErro durante a analise da imagem: {exc}")
            return 1
    elif user_query:
        print(f"Utilizador: {user_query}\n")
        print("ChefLLama a pesquisar e a elaborar receitas...")
        try:
            answer = run_chef_query(chef_agent, user_query, thread_id=thread_id)
            print(f"\nChefLLama:\n{answer}\n")
            return 0
        except Exception as exc:
            print(f"\nOcorreu um erro: {exc}")
            return 1
    return 0

def run_interactive_loop(thread_id: str = DEFAULT_THREAD_ID) -> int:
    """Executa o ciclo de conversacao interativo no terminal."""
    print("Bem-vindo ao ChefLLama - O teu Chef Pessoal")
    print("Indica os ingredientes disponiveis no teu frigorifico ou despensa,")
    print("ou escreve 'imagem <caminho>' para analisar a foto.")
    print("Escreve 'sair' ou 'q' para terminar.\n")

    while True:
        try:
            user_input = input("Tu: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("sair", "exit", "quit", "q"):
                print("\nChefLLama: Ate a proxima e bom apetite!")
                break

            # Handle bare image commands and commands with arguments
            lower_input = user_input.lower()
            if lower_input in ("imagem", "/imagem", "foto", "/foto"):
                print("\nPor favor especifica o caminho da imagem (ex: imagem ./foto.jpg)\n")
                continue

            if lower_input.startswith(("imagem ", "/imagem ", "foto ", "/foto ")):
                parts = user_input.split(maxsplit=1)
                if len(parts) > 1 and parts[1].strip():
                    img_path = parts[1].strip().strip('"').strip("'")
                    if os.path.isfile(img_path):
                        answer = process_fridge_image_and_suggest(chef_agent, img_path, thread_id=thread_id)
                        print(f"\nChefLLama:\n{answer}\n")
                    else:
                        print(f"\nErro: Ficheiro de imagem '{img_path}' nao encontrado ou invalido.\n")
                else:
                    print("\nPor favor especifica o caminho da imagem (ex: imagem ./foto.jpg)\n")
                continue

            print("\nChefLLama a processar o pedido...")
            answer = run_chef_query(chef_agent, user_input, thread_id=thread_id)
            print(f"\nChefLLama:\n{answer}\n")
        except (KeyboardInterrupt, EOFError):
            print("\n\nChefLLama: Ate breve!")
            break
        except Exception as exc:
            print(f"\nErro ao processar o pedido: {exc}\n")
    return 0

def main() -> int:
    """Ponto de entrada da aplicacao CLI com suporte a saida com codigo de estado."""
    args = parse_arguments()
    if args.image_path or (args.query and len(args.query) > 0):
        return handle_direct_execution(args)
    return run_interactive_loop()

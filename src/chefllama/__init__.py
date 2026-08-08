import sys
from .agent import chef_agent, create_chef_agent, run_chef_query
from .cli import main
from .service import process_fridge_image_and_suggest
from .vision import analyze_fridge_image, encode_image_file

__all__ = [
    "main",
    "chef_agent",
    "create_chef_agent",
    "run_chef_query",
    "analyze_fridge_image",
    "encode_image_file",
    "process_fridge_image_and_suggest",
]

if __name__ == "__main__":
    sys.exit(main())

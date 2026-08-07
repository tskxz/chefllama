import base64
import os
from typing import Tuple
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama

def get_image_mime_type(file_path: str) -> str:
    """Detect image MIME type based on file extension."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext in (".jpg", ".jpeg"):
        return "image/jpeg"
    if ext == ".png":
        return "image/png"
    if ext == ".webp":
        return "image/webp"
    return "image/jpeg"

def encode_image_file(image_path: str) -> Tuple[str, str]:
    """Read local image file and return base64 string and MIME type."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Ficheiro de imagem nao encontrado: {image_path}")
    
    mime_type = get_image_mime_type(image_path)
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string, mime_type

def analyze_fridge_image(
    image_path: str,
    model: str = "llava:latest",
    custom_prompt: str = ""
) -> str:
    """Analisa uma foto do frigorifico/despensa usando o modelo LLaVA e extrai os ingredientes identificados."""
    img_b64, mime_type = encode_image_file(image_path)
    
    prompt_text = (
        custom_prompt or
        "Examina detalhadamente esta foto do interior de um frigorifico ou despensa. "
        "Lista todos os ingredientes, alimentos, sobras e condimentos visiveis que identificares. "
        "Responde em Portugues de Portugal (PT-PT) de forma estruturada e concisa, sem emojis."
    )
    
    message = HumanMessage(content=[
        {"type": "text", "text": prompt_text},
        {"type": "image", "base64": img_b64, "mime_type": mime_type}
    ])
    
    llm = ChatOllama(model=model, temperature=0.2)
    response = llm.invoke([message])
    return str(response.content).strip()

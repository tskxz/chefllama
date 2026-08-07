# ChefLLama

O ChefLLama e um assistente IA pessoal construido com LangChain, LangGraph, Llama 3.2 e pesquisa na web em tempo real atraves da API Tavily.

O objetivo do ChefLLama e sugerir receitas praticas, criativas e sem desperdicio com base nos ingredientes que tens disponiveis no teu frigorifico ou despensa.

---

## Funcionalidades

- Pesquisa Web em Tempo Real: Encontra receitas e truques culinarios na web atraves da API do Tavily.
- Modelo Local com Ollama: Utiliza o modelo llama3.2 localmente com resposta rapida e privada.
- Memoria de Conversacao: Mantem o contexto de conversas com multiplos turnos para responder a perguntas de seguimento, instrucoes detalhadas ou adaptacoes de receitas.
- Interface CLI Interativa: Permite conversar diretamente no terminal ou executar consultas rapidas por argumento.
- Foco no Aproveitamento Integral: Minimiza o desperdicio alimentar aproveitando sobras e ingredientes existentes.

---

## Como Executar

### 1. Pre-requisitos
- Ollama instalado com o modelo llama3.2:
  ```bash
  ollama run llama3.2
  ```
- Chave de API do Tavily no ficheiro .env.

### 2. Configurar o .env
Cria ou edita o ficheiro .env:
```env
TAVILY_API_KEY=a_tua_chave_tavily
```

### 3. Iniciar o Agente
Modo interativo no terminal:
```bash
uv run chefllama
```

Consulta rapida direta por argumento:
```bash
uv run chefllama "Tenho restos de peito de frango cozido e arroz, o que posso fazer?"
```

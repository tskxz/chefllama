# ChefLLama - O teu Chef Pessoal com IA

O ChefLLama é um assistente IA pessoal construído com LangChain 1.x, LangGraph, Ollama (Llama 3.2 e LLaVA) e pesquisa na web em tempo real através da API Tavily.

O objetivo do ChefLLama é sugerir receitas práticas, criativas e sem desperdício com base nos ingredientes que tens disponíveis no teu frigorífico ou despensa, quer através de texto ou pela análise direta de fotografias.

---

## Funcionalidades

- Análise Visual de Fotografias (LLaVA): Identifica automaticamente os alimentos, sobras e ingredientes visíveis a partir de uma fotografia do interior do frigorífico ou despensa.
- Pesquisa Web em Tempo Real (Tavily): Encontra receitas reais, truques culinários e combinações na web através da API do Tavily.
- Modelos Locais com Ollama: Utiliza os modelos llama3.2 e llava localmente com execução rápida e privada.
- Memória de Conversação (LangGraph): Mantém o contexto de conversação em múltiplos turnos para responder a perguntas de seguimento, instruções detalhadas ou adaptações de receitas.
- Interface CLI Interativa: Permite conversar diretamente no terminal ou executar consultas rápidas por argumento.
- Foco no Aproveitamento Integral: Minimiza o desperdício alimentar aproveitando sobras e ingredientes existentes.

---

## Como Executar

### 1. Pré-requisitos
- Instalar o Ollama e descarregar os modelos necessários:
  ```bash
  ollama pull llama3.2
  ollama pull llava
  ```
- Obter uma chave de API do Tavily e adicioná-la ao ficheiro `.env`.

### 2. Configurar o .env
Cria ou edita o ficheiro `.env`:
```env
TAVILY_API_KEY=a_tua_chave_tavily
```

### 3. Utilização

#### Modo de Chat Interativo
Inicia a sessão interativa no terminal:
```bash
uv run chefllama
```
Durante a conversa, podes indicar ingredientes por texto ou analisar uma fotografia digitando:
```text
imagem ./caminho_para_a_foto.jpg
```

#### Análise Direta de Fotografia por Linha de Comandos
Analisa uma fotografia do frigorífico e obtém sugestões de receitas de imediato:
```bash
uv run chefllama --imagem ./frigorifico.jpg
```
Ou com requisitos específicos adicionais:
```bash
uv run chefllama --imagem ./frigorifico.jpg "quero uma receita vegetariana sem forno"
```

#### Consulta Rápida por Texto
```bash
uv run chefllama "Tenho restos de peito de frango cozido e arroz, o que posso fazer?"
```

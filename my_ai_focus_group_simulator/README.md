# AI Focus Group Simulator (Local LLM + Streamlit)

A modular Python scaffold for simulating focus-group responses from synthetic personas using a **local LLM endpoint** and visualizing results in **Streamlit**.

## Project Structure

```text
my_ai_focus_group_simulator/
├── README.md
├── requirements.txt
├── prompt_templates/
│   ├── persona_generation.txt
│   ├── response_simulation.txt
│   └── summary_insights.txt
├── personas.json
├── streamlit_app.py
├── llm_local.py
├── persona_manager.py
├── focus_group_engine.py
└── utils.py
```

## Features

- Local LLM client that targets an OpenAI-compatible local endpoint (LM Studio, Ollama bridge, vLLM, llama.cpp server, etc.).
- JSON-based persona storage with load/save utilities.
- Prompt templates stored separately from code.
- Focus-group simulation engine with one response per persona-question pair.
- Pandas-based analysis and summary insight generation.
- Minimal Streamlit UI for entering product context, questions, and running simulations.

## Quick Start

### 1) Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Start your local LLM endpoint

Use any local model server with an OpenAI-compatible `/v1/chat/completions` endpoint.

Examples:
- **LM Studio local server**
- **vLLM OpenAI server**
- **llama.cpp server with OpenAI-compatible mode**

### 4) Configure environment variables (optional)

```bash
export LOCAL_LLM_BASE_URL="http://localhost:1234/v1"
export LOCAL_LLM_MODEL="local-model-name"
export LOCAL_LLM_API_KEY="not-required-for-most-local-endpoints"
```

Defaults are defined in `llm_local.py` if not set.

### 5) Run Streamlit app

```bash
streamlit run streamlit_app.py
```

## Persona JSON Format

`personas.json` stores a list of persona objects:

```json
[
  {
    "name": "Budget-Savvy Parent",
    "age": 38,
    "occupation": "Teacher",
    "traits": ["price-conscious", "family-oriented", "practical"],
    "goals": ["save money", "reduce household stress"]
  }
]
```

## Notes

- This scaffold prioritizes simplicity and local-first development.
- For production, add retries, richer evaluation, observability, and stronger prompt/version controls.

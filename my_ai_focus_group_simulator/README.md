# AI Focus Group Simulator (OpenAI-Compatible LLM + Streamlit)

A modular Python scaffold for simulating focus-group responses from synthetic personas using an **OpenAI-compatible LLM endpoint** and visualizing results in **Streamlit**.

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

- OpenAI-compatible LLM client for local or hosted endpoints (OpenAI, OpenRouter, LM Studio, vLLM, llama.cpp, etc.).
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

### 3) Choose an LLM endpoint

Use any endpoint that supports OpenAI chat completions (`/v1/chat/completions`).

Examples:
- **OpenAI API**
- **OpenRouter**
- **LM Studio / vLLM / llama.cpp (self-hosted)**

You can configure endpoint credentials in either:
- the Streamlit sidebar fields (Base URL / Model / API Key), or
- environment variables:

```bash
export LLM_BASE_URL="https://api.openai.com/v1"
export LLM_MODEL="gpt-4o-mini"
export LLM_API_KEY="your-key"
```

Backward-compatible variables (`LOCAL_LLM_*`) are also supported.

### 4) Run Streamlit app

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

- This scaffold prioritizes simplicity and endpoint flexibility (hosted or local).
- For production, add retries, richer evaluation, observability, and stronger prompt/version controls.

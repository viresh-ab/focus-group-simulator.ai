"""Streamlit UI for OpenAI-compatible AI focus group simulation."""

from __future__ import annotations

from pathlib import Path

import requests
import streamlit as st

from focus_group_engine import FocusGroupEngine
from llm_local import LocalLLMClient
from persona_manager import create_persona, load_personas, save_personas


BASE_DIR = Path(__file__).resolve().parent
PERSONAS_PATH = BASE_DIR / "personas.json"


st.set_page_config(page_title="AI Focus Group Simulator", layout="wide")
st.title("🧪 AI Focus Group Simulator")

if "personas" not in st.session_state:
    st.session_state.personas = load_personas(PERSONAS_PATH)

with st.sidebar:
    st.header("LLM Endpoint")
    llm_base_url = st.text_input(
        "Base URL",
        value="https://api.openai.com/v1",
        help="Use any OpenAI-compatible URL (OpenAI, OpenRouter, vLLM, LM Studio, etc.).",
    )
    llm_model = st.text_input("Model", value="gpt-4o-mini")
    llm_api_key = st.text_input("API Key", value="", type="password")

    st.divider()
    st.header("Personas")
    st.caption(f"Loaded personas: {len(st.session_state.personas)}")

    with st.expander("Add Persona", expanded=False):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=16, max_value=100, value=30)
        occupation = st.text_input("Occupation")
        traits_raw = st.text_input("Traits (comma-separated)")
        goals_raw = st.text_input("Goals (comma-separated)")

        if st.button("Add persona"):
            persona = create_persona(
                name=name.strip() or "Unnamed Persona",
                age=int(age),
                occupation=occupation.strip() or "Unknown",
                traits=[t.strip() for t in traits_raw.split(",") if t.strip()],
                goals=[g.strip() for g in goals_raw.split(",") if g.strip()],
            )
            st.session_state.personas.append(persona)
            save_personas(st.session_state.personas, PERSONAS_PATH)
            st.success("Persona added and saved.")

    if st.button("Reload personas from disk"):
        st.session_state.personas = load_personas(PERSONAS_PATH)
        st.success("Reloaded personas.")

st.subheader("1) Product Context")
product_description = st.text_area(
    "Describe your product or feature",
    placeholder="Example: A mobile app that helps remote workers run 20-minute guided deep-work sessions.",
    height=120,
)

st.subheader("2) Focus Group Questions")
questions_raw = st.text_area(
    "Enter one question per line",
    value="What problem does this solve for you?\nWhat concerns would you have before trying this?",
    height=120,
)
questions = [q.strip() for q in questions_raw.splitlines() if q.strip()]

run = st.button("Run simulation", type="primary")

if run:
    if not product_description.strip():
        st.error("Please provide a product description.")
    elif not questions:
        st.error("Please provide at least one question.")
    elif not st.session_state.personas:
        st.error("No personas loaded. Add one in the sidebar.")
    else:
        client = LocalLLMClient(base_url=llm_base_url, model=llm_model, api_key=llm_api_key)
        engine = FocusGroupEngine(client)

        try:
            with st.spinner("Simulating persona responses..."):
                df = engine.simulate_responses(
                    personas=st.session_state.personas,
                    product_description=product_description,
                    questions=questions,
                )

            st.subheader("3) Responses DataFrame")
            st.dataframe(df, use_container_width=True)

            st.subheader("4) Summary Report")
            report = engine.build_summary_report(
                df=df,
                product_description=product_description,
                question_context=" | ".join(questions),
            )
            st.markdown(report)
        except requests.exceptions.RequestException as exc:
            st.error("Could not connect to the configured LLM endpoint.")
            st.info(
                "Check Base URL, model name, API key, and whether the endpoint exposes "
                "`/v1/chat/completions`."
            )
            st.code(str(exc))

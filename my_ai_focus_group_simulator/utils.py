"""Helper utilities for prompt templates and pandas summaries."""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd


PROMPT_DIR = Path("prompt_templates")


def load_prompt_template(template_name: str, prompt_dir: Path | str = PROMPT_DIR) -> str:
    path = Path(prompt_dir) / template_name
    with path.open("r", encoding="utf-8") as f:
        return f.read()


def to_response_dataframe(records: list[dict]) -> pd.DataFrame:
    if not records:
        return pd.DataFrame(columns=["persona_name", "question", "response"])
    return pd.DataFrame(records)


def summarize_with_pandas(df: pd.DataFrame) -> Dict[str, str]:
    if df.empty:
        return {
            "total_responses": "0",
            "unique_personas": "0",
            "questions_covered": "0",
            "avg_response_length_chars": "0",
        }

    enriched = df.copy()
    enriched["response_length"] = enriched["response"].fillna("").astype(str).str.len()

    return {
        "total_responses": str(len(enriched)),
        "unique_personas": str(enriched["persona_name"].nunique()),
        "questions_covered": str(enriched["question"].nunique()),
        "avg_response_length_chars": f"{enriched['response_length'].mean():.1f}",
    }

"""Core simulation logic for persona response generation and reporting."""

from __future__ import annotations

import json
from typing import Any, Dict, List

from llm_local import LocalLLMClient
from utils import load_prompt_template, summarize_with_pandas, to_response_dataframe


class FocusGroupEngine:
    def __init__(self, llm_client: LocalLLMClient) -> None:
        self.llm_client = llm_client

    def simulate_responses(
        self,
        personas: List[Dict[str, Any]],
        product_description: str,
        questions: List[str],
    ):
        template = load_prompt_template("response_simulation.txt")
        records: List[Dict[str, str]] = []

        for persona in personas:
            persona_json = json.dumps(persona, ensure_ascii=False, indent=2)
            for question in questions:
                prompt = template.format(
                    persona_json=persona_json,
                    product_description=product_description,
                    question=question,
                )
                response_text = self.llm_client.generate(prompt=prompt)
                records.append(
                    {
                        "persona_name": persona.get("name", "Unknown Persona"),
                        "question": question,
                        "response": response_text,
                    }
                )

        return to_response_dataframe(records)

    def build_summary_report(self, df, product_description: str, question_context: str) -> str:
        pandas_summary = summarize_with_pandas(df)

        template = load_prompt_template("summary_insights.txt")
        responses_blob = "\n".join(
            f"- {row.persona_name}: {row.response}" for row in df.itertuples(index=False)
        )
        prompt = template.format(
            product_description=product_description,
            question=question_context,
            responses=responses_blob,
        )

        llm_summary = self.llm_client.generate(prompt=prompt, temperature=0.4)

        metrics = "\n".join(f"- **{k}**: {v}" for k, v in pandas_summary.items())
        return f"## Quantitative Snapshot\n{metrics}\n\n## LLM Summary Insights\n{llm_summary}"

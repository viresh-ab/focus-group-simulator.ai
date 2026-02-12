"""Utilities for loading, saving, and creating personas in JSON."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


DEFAULT_PERSONAS_PATH = Path("personas.json")


def load_personas(path: Path | str = DEFAULT_PERSONAS_PATH) -> List[Dict[str, Any]]:
    path = Path(path)
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, list) else []


def save_personas(personas: List[Dict[str, Any]], path: Path | str = DEFAULT_PERSONAS_PATH) -> None:
    path = Path(path)
    with path.open("w", encoding="utf-8") as f:
        json.dump(personas, f, indent=2, ensure_ascii=False)


def create_persona(name: str, age: int, occupation: str, traits: List[str], goals: List[str]) -> Dict[str, Any]:
    return {
        "name": name,
        "age": age,
        "occupation": occupation,
        "traits": traits,
        "goals": goals,
    }

"""
Storage helpers for JSON persistence.

Design goals:
- Simple JSON read/write.
- If file is missing -> return default.
- If file is invalid/corrupted -> print an error and return default (do not crash).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: str | Path, default: Any) -> Any:
    """
    Load JSON content from a file. If file doesn't exist or is invalid,
    return 'default' and print an error for invalid content.
    """
    p = Path(path)

    if not p.exists():
        return default

    try:
        text = p.read_text(encoding="utf-8").strip()
        if not text:
            return default
        return json.loads(text)
    except (json.JSONDecodeError, OSError) as exc:
        print(f"[storage] Error reading JSON file '{p}': {exc}")
        return default


def save_json(path: str | Path, data: Any) -> None:
    """
    Save data to JSON file, creating parent directories if needed.
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    p.write_text(payload, encoding="utf-8")

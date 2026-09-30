"""Minimal command-line todo list: add items and print them."""

from __future__ import annotations

import json
import sys
from pathlib import Path

DEFAULT_STORE = Path("todo.json")


def load(path: Path = DEFAULT_STORE) -> list[str]:
    """Return stored items; an absent store means an empty list."""
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"store must contain a JSON array: {path}")
    return [str(item) for item in data]


def save(items: list[str], path: Path = DEFAULT_STORE) -> None:
    path.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def add(text: str, path: Path = DEFAULT_STORE) -> list[str]:
    items = load(path)
    items.append(text)
    save(items, path)
    return items


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        for index, item in enumerate(load(), start=1):
            print(f"{index}. {item}")
        return 0
    if args[0] == "add" and len(args) > 1:
        add(" ".join(args[1:]))
        return 0
    print("usage: python src/todo.py [add <text>]", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

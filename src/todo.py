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


def remove(index: int, path: Path = DEFAULT_STORE) -> str:
    """Remove the item at 1-based ``index`` and return its text.

    The index matches the numbering printed by the listing, so users can reuse
    what they see; the stored list itself stays 0-based. An out-of-range index
    (0, a negative value, or len+1) raises IndexError *before* save() is called,
    so a rejected removal never rewrites the store.
    """
    items = load(path)
    if not 1 <= index <= len(items):
        raise IndexError(f"index {index} out of range (1..{len(items)})")
    text = items.pop(index - 1)
    save(items, path)
    return text


def main(argv: list[str] | None = None, store: Path = DEFAULT_STORE) -> int:
    """Dispatch one command.

    ``store`` is injectable so tests exercise the command layer through a
    temporary file instead of the real ``todo.json`` in the working directory.
    """
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        for index, item in enumerate(load(store), start=1):
            print(f"{index}. {item}")
        return 0
    if args[0] == "add" and len(args) > 1:
        add(" ".join(args[1:]), store)
        return 0
    if args[0] == "remove":
        if len(args) != 2:
            print("error: remove takes exactly one index", file=sys.stderr)
            return 2
        try:
            index = int(args[1])
        except ValueError:
            print(f"error: index must be an integer: {args[1]}", file=sys.stderr)
            return 1
        try:
            text = remove(index, store)
        except IndexError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        print(f"removed: {text}")
        return 0
    print("usage: python src/todo.py [add <text> | remove <index>]", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

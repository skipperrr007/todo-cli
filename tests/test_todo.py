"""Tests for src/todo.py."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import todo  # noqa: E402


class TodoStoreTest(unittest.TestCase):
    def setUp(self) -> None:
        # 测试临时文件放在仓库内，避免依赖系统临时目录的写权限。
        base = Path(__file__).resolve().parent / "_work"
        base.mkdir(exist_ok=True)
        self._tmp = tempfile.TemporaryDirectory(dir=base)
        self.addCleanup(self._tmp.cleanup)
        self.store = Path(self._tmp.name) / "todo.json"

    def test_missing_store_is_empty(self) -> None:
        self.assertEqual(todo.load(self.store), [])

    def test_add_appends_in_order(self) -> None:
        todo.add("写文档", self.store)
        todo.add("跑测试", self.store)
        self.assertEqual(todo.load(self.store), ["写文档", "跑测试"])

    def test_save_uses_utf8(self) -> None:
        todo.add("中文待办", self.store)
        self.assertIn("中文待办", self.store.read_text(encoding="utf-8"))

    def test_non_array_store_raises(self) -> None:
        self.store.write_text('{"a": 1}', encoding="utf-8")
        with self.assertRaises(ValueError):
            todo.load(self.store)


if __name__ == "__main__":
    unittest.main()

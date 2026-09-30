"""Tests for src/todo.py."""

from __future__ import annotations

import sys
import unittest
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import todo  # noqa: E402

WORK = Path(__file__).resolve().parent / "_work"


class TodoStoreTest(unittest.TestCase):
    """每个测试使用一个独立临时文件。

    这里刻意不用 tempfile.TemporaryDirectory：它在清理时会对目录执行 chmod
    并递归扫描目录树，在受限的运行环境里会被拒绝。直接使用文件既简单又稳定。
    """

    def setUp(self) -> None:
        WORK.mkdir(parents=True, exist_ok=True)
        self.store = WORK / f"store_{uuid.uuid4().hex}.json"

    def tearDown(self) -> None:
        self.store.unlink(missing_ok=True)

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

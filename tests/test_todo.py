"""Tests for src/todo.py."""

from __future__ import annotations

import contextlib
import io
import json
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


class TodoRemoveTest(unittest.TestCase):
    """按序号删除：1-based 对外序号，0-based 内部列表。

    数据安全是本类的重点：任何被拒绝的删除都必须让 store 逐字节不变，
    因此失败路径的断言同时检查异常和文件字节，而不只看异常。
    """

    def setUp(self) -> None:
        WORK.mkdir(parents=True, exist_ok=True)
        self.store = WORK / f"store_{uuid.uuid4().hex}.json"

    def tearDown(self) -> None:
        self.store.unlink(missing_ok=True)

    def write_store(self, items: list[str]) -> None:
        todo.save(items, self.store)

    def store_bytes(self) -> bytes | None:
        return self.store.read_bytes() if self.store.exists() else None

    def test_remove_middle_item_keeps_remaining_order(self) -> None:
        """外部序号 2 -> 内部下标 1，删中的是正确那一条且顺序不变。"""
        self.write_store(["写文档", "跑测试", "写代码"])

        removed = todo.remove(2, self.store)

        self.assertEqual(removed, "跑测试")
        self.assertEqual(todo.load(self.store), ["写文档", "写代码"])

    def test_remove_first_and_last_boundary_items(self) -> None:
        """两个端点映射无 off-by-one：外部 1 -> 内部 0，外部 len -> 内部 len-1。"""
        self.write_store(["a", "b", "c"])

        self.assertEqual(todo.remove(1, self.store), "a")
        self.assertEqual(todo.load(self.store), ["b", "c"])

        self.assertEqual(todo.remove(2, self.store), "c")
        self.assertEqual(todo.load(self.store), ["b"])

    def test_remove_index_zero_is_rejected_without_writing(self) -> None:
        """下界越界：0 非法（与合法下界只差 1），拒绝且不写盘。"""
        self.write_store(["a", "b", "c"])
        before = self.store_bytes()

        with self.assertRaises(IndexError):
            todo.remove(0, self.store)

        self.assertEqual(self.store_bytes(), before)

    def test_remove_negative_index_is_rejected_without_writing(self) -> None:
        """负索引陷阱：-1 若走 pop(-1) 会静默删掉末项，必须被拒绝且不写盘。"""
        self.write_store(["a", "b", "c"])
        before = self.store_bytes()

        with self.assertRaises(IndexError):
            todo.remove(-1, self.store)

        self.assertEqual(self.store_bytes(), before)

    def test_remove_index_beyond_length_is_rejected_without_writing(self) -> None:
        """上界越界：len+1 非法（与合法上界只差 1），拒绝且不写盘。"""
        self.write_store(["a", "b", "c"])
        before = self.store_bytes()

        with self.assertRaises(IndexError):
            todo.remove(4, self.store)

        self.assertEqual(self.store_bytes(), before)

    def test_remove_from_missing_store_is_rejected_without_creating_file(self) -> None:
        """空/缺失 store：load() 返回 []，删除必须报错且不凭空创建 todo.json。"""
        self.assertFalse(self.store.exists())

        with self.assertRaises(IndexError):
            todo.remove(1, self.store)

        self.assertFalse(self.store.exists())

    def test_remove_leaves_corrupt_store_untouched(self) -> None:
        """坏 JSON：报错且原文件逐字节保留，用户仍可手工抢救，不会被改写成空数组。"""
        self.store.write_text('{"a": 1}', encoding="utf-8")
        before = self.store_bytes()

        with self.assertRaises(ValueError):
            todo.remove(1, self.store)

        self.assertEqual(self.store_bytes(), before)

    def test_main_remove_rejects_invalid_arguments_without_writing(self) -> None:
        """入口层参数校验：缺参数、非整数、多余参数都不写盘并以非零码退出。"""
        for argv in (["remove"], ["remove", "abc"], ["remove", "1", "2"]):
            with self.subTest(argv=argv):
                self.write_store(["a", "b"])
                before = self.store_bytes()
                stderr = io.StringIO()

                with contextlib.redirect_stderr(stderr), contextlib.redirect_stdout(io.StringIO()):
                    code = todo.main(argv, self.store)

                self.assertNotEqual(code, 0)
                self.assertTrue(stderr.getvalue().strip())
                self.assertEqual(self.store_bytes(), before)

    def test_main_remove_prints_removed_item_and_exits_zero(self) -> None:
        """入口层成功契约：退出码 0、stdout 含被删文本、删除后对外序号重新连续。"""
        self.write_store(["写文档", "跑测试", "写代码"])
        stdout = io.StringIO()

        with contextlib.redirect_stdout(stdout):
            code = todo.main(["remove", "1"], self.store)

        self.assertEqual(code, 0)
        self.assertIn("写文档", stdout.getvalue())

        listed = io.StringIO()
        with contextlib.redirect_stdout(listed):
            todo.main([], self.store)
        self.assertEqual(listed.getvalue().splitlines(), ["1. 跑测试", "2. 写代码"])


if __name__ == "__main__":
    unittest.main()

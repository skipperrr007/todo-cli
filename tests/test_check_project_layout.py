from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools/check_project_layout.py"
SPEC = importlib.util.spec_from_file_location("check_project_layout", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load {MODULE_PATH}")
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


class ProjectLayoutCheckerTests(unittest.TestCase):
    def test_ssh_and_https_github_remotes_normalize_equally(self) -> None:
        ssh = CHECKER.normalize_remote("git@github.com:owner/repository.git")
        https = CHECKER.normalize_remote("https://github.com/owner/repository")
        self.assertEqual(ssh, https)

    def test_auto_mode_uses_configured_role(self) -> None:
        mode, errors = CHECKER.determine_mode("auto", {"repositoryRole": "project"})
        self.assertEqual(mode, "project")
        self.assertEqual(errors, [])

    def test_explicit_project_mode_can_preflight_template_config(self) -> None:
        mode, errors = CHECKER.determine_mode("project", {"repositoryRole": "template"})
        self.assertEqual(mode, "project")
        self.assertEqual(errors, [])

    def test_current_template_config_is_valid(self) -> None:
        config = json.loads((ROOT / "config/project.json").read_text(encoding="utf-8"))
        self.assertEqual(CHECKER.check_config(config, "template", explicit_mode=False), [])

    def test_current_template_fails_project_customization(self) -> None:
        config = json.loads((ROOT / "config/project.json").read_text(encoding="utf-8"))
        errors = CHECKER.check_project_customization(config)
        self.assertIn("projectName still identifies the template", errors)
        self.assertIn(
            "template-only file remains in project mode: docs/runbooks/bootstrap-new-project.md",
            errors,
        )


if __name__ == "__main__":
    unittest.main()

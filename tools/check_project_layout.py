#!/usr/bin/env python3
"""Check the shared layout and template/project identity of this repository."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_CONFIG = ROOT / "config/project.json"

COMMON_REQUIRED_PATHS = (
    "README.md",
    "AGENTS.md",
    "CONTEXT.md",
    ".gitignore",
    ".editorconfig",
    "src",
    "tests",
    "tools",
    "config/project.json",
    "examples",
    "docs/README.md",
    "docs/architecture/overview.md",
    "docs/decisions/README.md",
    "docs/decisions/0000-decision-template.md",
    "docs/guides/codex-collaboration.md",
    "docs/guides/development-workflow.md",
    "docs/guides/extension-profiles.md",
    "docs/runbooks/verification.md",
    "docs/handoffs/current.md",
    "docs/archive/README.md",
)

TEMPLATE_ONLY_PATHS = (
    "docs/guides/template-maintenance.md",
    "docs/runbooks/bootstrap-new-project.md",
    "docs/runbooks/publish-template-to-github.md",
)

PROJECT_CUSTOMIZATION_FILES = (
    "README.md",
    "CONTEXT.md",
    "docs/architecture/overview.md",
    "docs/runbooks/verification.md",
    "docs/handoffs/current.md",
)

PROJECT_FORBIDDEN_MARKERS = (
    "Codex Project Development Template",
    "Project Development Template",
    "initial-template-design",
    "template-maintenance",
    "local-unpublished",
)

MARKDOWN_LINK = re.compile(r"(?<!!)\[[^]]+\]\(([^)]+)\)")
SEMVER = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        choices=("auto", "template", "project"),
        default="auto",
        help="check the configured role, or preflight an explicit target role",
    )
    return parser.parse_args()


def load_config() -> tuple[dict[str, Any], list[str]]:
    if not PROJECT_CONFIG.exists():
        return {}, ["missing required path: config/project.json"]
    try:
        value = json.loads(PROJECT_CONFIG.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {}, [f"invalid config/project.json: {exc}"]
    if not isinstance(value, dict):
        return {}, ["invalid config/project.json: top-level value must be an object"]
    return value, []


def determine_mode(requested: str, config: dict[str, Any]) -> tuple[str, list[str]]:
    if requested != "auto":
        return requested, []
    configured = config.get("repositoryRole")
    if configured not in {"template", "project"}:
        return "template", ["repositoryRole must be 'template' or 'project'"]
    return str(configured), []


def check_required_paths(mode: str) -> list[str]:
    required = COMMON_REQUIRED_PATHS + (TEMPLATE_ONLY_PATHS if mode == "template" else ())
    return [f"missing required path: {item}" for item in required if not (ROOT / item).exists()]


def check_local_markdown_links() -> list[str]:
    errors: list[str] = []
    for markdown in sorted(ROOT.rglob("*.md")):
        if ".git" in markdown.parts:
            continue
        text = markdown.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK.findall(text):
            target = raw_target.strip().split("#", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            target = target.strip("<>")
            resolved = (markdown.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"broken local link: {markdown.relative_to(ROOT)} -> {raw_target}")
    return errors


def check_config(config: dict[str, Any], mode: str, explicit_mode: bool) -> list[str]:
    errors: list[str] = []
    required_fields = {
        "schemaVersion": int,
        "repositoryRole": str,
        "projectName": str,
        "templateVersion": str,
        "templateSource": str,
        "initializedOn": str,
    }
    for field, expected_type in required_fields.items():
        value = config.get(field)
        if not isinstance(value, expected_type) or (expected_type is str and not value.strip()):
            errors.append(f"config field {field!r} must be a non-empty {expected_type.__name__}")

    if config.get("schemaVersion") != 1:
        errors.append("schemaVersion must be 1")
    version = config.get("templateVersion")
    if isinstance(version, str) and not SEMVER.fullmatch(version):
        errors.append("templateVersion must use X.Y.Z numeric form")
    initialized = config.get("initializedOn")
    if isinstance(initialized, str):
        try:
            date.fromisoformat(initialized)
        except ValueError:
            errors.append("initializedOn must use YYYY-MM-DD")

    configured_role = config.get("repositoryRole")
    if not explicit_mode and configured_role != mode:
        errors.append(f"configured repositoryRole {configured_role!r} does not match check mode {mode!r}")
    return errors


def check_project_customization(config: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if config.get("projectName") in {"Project Development Template", "Codex Project Development Template"}:
        errors.append("projectName still identifies the template")
    if config.get("templateSource") == "local-unpublished":
        errors.append("project mode requires the published template source URL")

    for relative in TEMPLATE_ONLY_PATHS:
        if (ROOT / relative).exists():
            errors.append(f"template-only file remains in project mode: {relative}")

    for relative in PROJECT_CUSTOMIZATION_FILES:
        path = ROOT / relative
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for marker in PROJECT_FORBIDDEN_MARKERS:
            if marker in text:
                errors.append(f"template marker {marker!r} remains in {relative}")
    return errors


def normalize_remote(value: str) -> str:
    normalized = value.strip().removesuffix("/").removesuffix(".git")
    if normalized.startswith("git@github.com:"):
        normalized = "https://github.com/" + normalized.removeprefix("git@github.com:")
    return normalized.lower()


def get_origin() -> str | None:
    completed = subprocess.run(
        ["git", "config", "--get", "remote.origin.url"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        return None
    value = completed.stdout.strip()
    return value or None


def check_remote(config: dict[str, Any], mode: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    origin = get_origin()
    source = config.get("templateSource")

    if mode == "project":
        if origin is None:
            warnings.append("project has no origin yet; configure the new project remote before push")
        elif isinstance(source, str) and source != "local-unpublished":
            if normalize_remote(origin) == normalize_remote(source):
                errors.append("project origin matches templateSource; do not push project work to the template repository")
    elif origin is None:
        warnings.append("template has no origin yet; this is expected before GitHub publication")

    return errors, warnings


def main() -> int:
    args = parse_args()
    config, errors = load_config()
    mode, mode_errors = determine_mode(args.mode, config)
    errors.extend(mode_errors)
    errors.extend(check_required_paths(mode))
    errors.extend(check_local_markdown_links())
    errors.extend(check_config(config, mode, explicit_mode=args.mode != "auto"))
    if mode == "project":
        errors.extend(check_project_customization(config))
    remote_errors, warnings = check_remote(config, mode)
    errors.extend(remote_errors)

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print(f"layout check failed in {mode} mode: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1

    required_count = len(COMMON_REQUIRED_PATHS) + (len(TEMPLATE_ONLY_PATHS) if mode == "template" else 0)
    print(f"layout check passed in {mode} mode: {required_count} required paths, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

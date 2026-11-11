#!/usr/bin/env python3
"""Keep the one Bolta skill in step everywhere it ships.

The skill is written once, in plugins/bolta/skills/bolta (the Claude plugin, which has to be
self-contained). Two things are derived from it and never edited by hand:

  skills/bolta/     the same files at the repository root, where every other client looks for a
                    skill (the open `skills` installer, a Cursor plugin, a Gemini CLI extension)
  the reconnect-notice matcher in plugins/bolta-checks/hooks/hooks.json, which lists tools by name
                    (any server name is too wide for a hook that runs after every call)

Usage:
    python3 -I tools/sync_skill.py                # write skills/bolta
    python3 -I tools/sync_skill.py --check        # exit 1 if skills/bolta is out of date
    python3 -I tools/sync_skill.py --sync-hooks   # refresh the notice matcher in plugins/bolta-checks
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
SRC = REPO / "plugins" / "bolta"
#: The checks plugin: the one place hooks/hooks.json and the scripts live.
CHECKS = REPO / "plugins" / "bolta-checks"
#: The skill on its own at the repository root, byte for byte the plugin's.
ROOT_SKILL = REPO / "skills" / "bolta"
SKILL_SRC = "skills/bolta"

#: How every matcher begins: any server name, then a tool name.
PREFIX = "^mcp__[A-Za-z0-9_-]+__"


def _read(path: pathlib.Path) -> bytes:
    return path.read_bytes()


def gated_tools(full_hooks: dict) -> list[str]:
    """The tools the full plugin's guard matcher lists."""
    for group in full_hooks["hooks"].get("PreToolUse", []):
        if any("guard-bolta-writes.sh" in h.get("command", "") for h in group.get("hooks", [])):
            m = re.search(r"__\(([^)]*)\)\$$", group["matcher"])
            if m:
                return m.group(1).split("|")
    raise SystemExit("build_skills_bundle: cannot find the guard matcher in plugins/bolta-checks/hooks/hooks.json")


def skill_tools(src: pathlib.Path) -> set[str]:
    """Every tool id named in a Tools section: the playbooks (references/<name>.md) hold them."""
    out: set[str] = set()
    for skill in sorted([*(src / "skills").glob("*/SKILL.md"), *(src / "skills").glob("*/references/*.md")]):
        text = skill.read_text()
        m = re.search(r"^## Tools\s*\n(.*?)(?=^## )", text, re.S | re.M)
        if m:
            out.update(re.findall(r"`([a-z][a-z0-9]*(?:-[a-z0-9]+)+)`", m.group(1)))
    return out


def notice_tools(full_hooks: dict, src: pathlib.Path) -> list[str]:
    """The tools the reconnect-notice matcher must list: the guard's, and every one a skill names.
    (Any server name is too wide for a hook that runs after every call, so it names the tools.)"""
    return sorted(set(gated_tools(full_hooks)) | skill_tools(src))


def notice_matcher(names: list[str]) -> str:
    return PREFIX + "(" + "|".join(names) + ")$"


def notice_groups(hooks: dict):
    """The PostToolUse and PostToolUseFailure groups that run the reconnect notice."""
    for event in ("PostToolUse", "PostToolUseFailure"):
        for group in hooks["hooks"].get(event, []):
            if any("bolta-auth-notice.sh" in h.get("command", "") for h in group.get("hooks", [])):
                yield event, group


def synced_hooks(full_hooks: dict, src: pathlib.Path) -> dict:
    """The full plugin's hooks with the reconnect-notice matchers rewritten from the skills."""
    out = json.loads(json.dumps(full_hooks))  # deep copy
    matcher = notice_matcher(notice_tools(full_hooks, src))
    for _event, group in notice_groups(out):
        group["matcher"] = matcher
    return out


def dumps(obj: dict) -> bytes:
    return (json.dumps(obj, indent=2, ensure_ascii=False) + "\n").encode()


def generate_root_skill(src: pathlib.Path = SRC) -> dict[str, tuple[bytes, bool]]:
    """skills/bolta at the repository root: the plugin's skill folder, unchanged."""
    base = src / SKILL_SRC
    return {p.relative_to(base).as_posix(): (_read(p), False)
            for p in sorted(base.rglob("*")) if p.is_file() and p.name != ".DS_Store"}


def existing(dst: pathlib.Path) -> dict[str, tuple[bytes, bool]]:
    out: dict[str, tuple[bytes, bool]] = {}
    if dst.is_dir():
        for path in sorted(dst.rglob("*")):
            if path.is_file() or path.is_symlink():
                out[path.relative_to(dst).as_posix()] = (path.read_bytes() if path.is_file() else b"", bool(path.stat().st_mode & 0o111))
    return out


def differences(expected: dict[str, tuple[bytes, bool]], actual: dict[str, tuple[bytes, bool]]) -> list[str]:
    diffs = []
    for rel in sorted(set(expected) | set(actual)):
        if rel not in actual:
            diffs.append(f"missing: {rel}")
        elif rel not in expected:
            diffs.append(f"not generated: {rel}")
        elif expected[rel][0] != actual[rel][0]:
            diffs.append(f"differs: {rel}")
        elif expected[rel][1] != actual[rel][1]:
            diffs.append(f"executable bit differs: {rel}")
    return diffs


def write(files: dict[str, tuple[bytes, bool]], dst: pathlib.Path = ROOT_SKILL) -> None:
    for rel in sorted(existing(dst)):
        if rel not in files:
            (dst / rel).unlink()
    for rel, (data, executable) in files.items():
        path = dst / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        path.chmod(0o755 if executable else 0o644)
    for d in sorted((p for p in dst.rglob("*") if p.is_dir()), reverse=True):
        if not any(d.iterdir()):
            d.rmdir()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="do not write; exit 1 if skills/bolta differs from the plugin's skill")
    ap.add_argument("--sync-hooks", action="store_true", help="rewrite the reconnect-notice matchers in the checks plugin's hooks.json from the skill, then stop")
    ap.add_argument("--src", type=pathlib.Path, default=SRC)
    ap.add_argument("--root-skill", type=pathlib.Path, default=ROOT_SKILL, help="where the skill on its own is written (skills/bolta)")
    ap.add_argument("--checks", type=pathlib.Path, default=CHECKS, help="the checks plugin (hooks/hooks.json and scripts/)")
    args = ap.parse_args(argv)
    if args.sync_hooks:
        hooks_path = args.checks.resolve() / "hooks" / "hooks.json"
        current = json.loads(hooks_path.read_text())
        want = dumps(synced_hooks(current, args.src.resolve()))
        if hooks_path.read_bytes() == want:
            print(f"{hooks_path} is up to date")
        else:
            hooks_path.write_bytes(want)
            print(f"rewrote the reconnect-notice matchers in {hooks_path}")
        return 0
    files = generate_root_skill(args.src.resolve())
    if args.check:
        diffs = differences(files, existing(args.root_skill.resolve()))
        for d in diffs:
            print(d)
        print("skills/bolta is up to date" if not diffs else "skills/bolta is out of date: run python3 -I tools/sync_skill.py")
        return 1 if diffs else 0
    write(files, args.root_skill.resolve())
    print(f"wrote {len(files)} files to {args.root_skill}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

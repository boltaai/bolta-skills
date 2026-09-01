#!/usr/bin/env python3
"""Check every SKILL.md against the tool surface the server actually exposes.

The pack has drifted from the server before — `TOOLS-ALIGNMENT.md` documents a
whole 38-skill generation that outlived the tools it described. A skill that
names a tool the client cannot call is worse than a missing skill: the model
tries it, gets "unknown endpoint", and improvises.

Two checks, both read out of the server's own catalog:

1. **Tool names.** Any hyphenated `backticked-token` must be an exposed tool or
   a sibling skill.
2. **Arguments.** For a backticked call site — `create-routine(name, goal=...)`
   — every named argument must exist in that tool's parameter schema. This is
   the check that catches a *stale signature*, which name-checking alone
   misses: `activate-routine(workspace_id, routine_id)` names a real tool and is
   still wrong the moment the schema stops taking `workspace_id`.

Required-argument completeness is deliberately NOT checked. Skills legitimately
show partial calls ("`create-post(...)`"), and flagging those would train people
to ignore the checker.

Usage:
    python plugin-skills/check_skills.py [path/to/SERVER]

Exits non-zero on any problem, so it can gate a release.
"""

from __future__ import annotations

import pathlib
import re
import sys

DEFAULT_SERVER = pathlib.Path.home() / "Projects/GitHub/BOLT-SERVER/SERVER"
#: Registered only behind WORKFLOW_RUNTIME_V1, so absent from MCP_EXPOSED_TOOLS
#: but legitimately referenced by a flag-aware skill.
# Flag-gated tools (WORKFLOW_MCP_TOOLS in documentation.py). Empty since the
# agent/workflow control plane was demoted off the MCP surface
# (SERVER: resources/architecture/SKILLS_FIRST_ARCHITECTURE_AUDIT_2026-08.md).
FLAG_GATED: set[str] = set()

#: Accepted on every tool regardless of what the EndpointDefinition declares:
#: the MCP layer prepends an optional `workspace_id` to every signature and
#: defaults it to the API key's workspace. Legal everywhere, required nowhere.
UNIVERSAL_PARAMS = {"workspace_id"}

#: Placeholders a skill uses to mean "and the rest". Never an argument name.
ELLIPSES = {"...", "…"}


def exposed_tool_ids(server_root: pathlib.Path) -> tuple[set[str], set[str]]:
    """(tools a client can call, every tool defined at all)."""
    doc = (server_root / "boltathread/mcp/documentation.py").read_text()
    tail = doc[doc.index("MCP_EXPOSED_TOOLS: List[str] = ["):]
    exposed = set(re.findall(r'^    "([a-z0-9-]+)",', tail, re.M)) | FLAG_GATED
    defined = set(re.findall(r'^        id="([a-z0-9-]+)"', doc, re.M))
    return exposed, defined


def tool_parameters(server_root: pathlib.Path) -> dict[str, set[str]]:
    """tool id -> the argument names its schema accepts.

    Parsed from the EndpointDefinition blocks rather than by importing Django,
    so this stays a standalone script the pack can run without a configured
    server environment.
    """
    doc = (server_root / "boltathread/mcp/documentation.py").read_text()
    params: dict[str, set[str]] = {}
    for match in re.finditer(r'^        id="([a-z0-9-]+)"', doc, re.M):
        tool_id = match.group(1)
        # The block runs to the next definition's id, or to the end.
        nxt = doc.find('\n        id="', match.end())
        block = doc[match.end(): nxt if nxt != -1 else len(doc)]
        names = set(re.findall(r'Parameter\(\s*name="([A-Za-z_][A-Za-z0-9_]*)"', block))
        params[tool_id] = names | UNIVERSAL_PARAMS
    return params


def call_sites(text: str):
    """Yield (tool_id, [argument names]) for every backticked call in a skill."""
    for match in re.finditer(r"`([a-z][a-z0-9]*(?:-[a-z0-9]+)+)\(([^`]*)\)`", text):
        tool_id, raw = match.group(1), match.group(2)
        args = []
        depth = 0
        current = ""
        # Split on top-level commas only: an inline object or list argument
        # ({"interval": "weekly", ...}) must not be read as three arguments.
        for char in raw:
            if char in "{[(":
                depth += 1
            elif char in "}])":
                depth -= 1
            if char == "," and depth == 0:
                args.append(current)
                current = ""
            else:
                current += char
        args.append(current)
        names = []
        for arg in args:
            arg = arg.strip()
            if not arg or arg in ELLIPSES:
                continue
            name = arg.split("=", 1)[0].strip()
            # Positional illustration such as `<reddit account id>` or a bare
            # value carries no argument name to check.
            if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
                names.append(name)
        yield tool_id, names


def main(argv: list[str]) -> int:
    server_root = pathlib.Path(argv[1]) if len(argv) > 1 else DEFAULT_SERVER
    if not (server_root / "boltathread/mcp/documentation.py").exists():
        print(f"server catalog not found under {server_root}", file=sys.stderr)
        return 2

    exposed, defined = exposed_tool_ids(server_root)
    schemas = tool_parameters(server_root)
    skills_dir = pathlib.Path(__file__).parent / "skills"
    skill_names = {p.name for p in skills_dir.iterdir() if p.is_dir()}

    problems: list[str] = []
    referenced: set[str] = set()

    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            problems.append(f"{skill_dir.name}: no SKILL.md")
            continue
        text = skill_file.read_text()

        # Frontmatter name must match the directory, or the upload lands under
        # a name nothing routes to.
        if not text.startswith(f"---\nname: {skill_dir.name}\n"):
            problems.append(f"{skill_dir.name}: frontmatter name does not match the directory")

        # A backticked hyphenated token, with or without a trailing call
        # signature: both `create-routine` and `create-routine(workspace_id,
        # ...)` are references to the same tool.
        tokens = re.findall(
            r"`([a-z][a-z0-9]*(?:-[a-z0-9]+)+)(?:\([^`]*\))?`", text
        )
        for token in sorted(set(tokens)):
            if token in skill_names:
                continue
            if token in exposed:
                referenced.add(token)
                continue
            if token in defined:
                problems.append(
                    f"{skill_dir.name}: '{token}' exists but is NOT in MCP_EXPOSED_TOOLS"
                )
            else:
                problems.append(f"{skill_dir.name}: '{token}' is not a Bolta MCP tool")

        # Argument names, against the tool's real schema. This is what catches
        # a stale signature on a tool that still exists.
        for tool_id, arg_names in call_sites(text):
            schema = schemas.get(tool_id)
            if schema is None:
                continue  # unknown tool: already reported above
            for arg in arg_names:
                if arg not in schema:
                    problems.append(
                        f"{skill_dir.name}: {tool_id}({arg}=...) — "
                        f"'{arg}' is not in that tool's schema"
                    )

    print(f"skills: {len(skill_names)}")
    print(f"exposed tools: {len(exposed)}")
    print(f"tools referenced by skills: {len(referenced)}")
    unused = sorted(exposed - referenced - FLAG_GATED)
    if unused:
        # Informational, never fatal: plenty of tools are legitimately
        # unreferenced. Worth seeing when adding a skill.
        print(f"exposed but referenced by no skill ({len(unused)}): {', '.join(unused)}")

    for problem in problems:
        print(f"PROBLEM: {problem}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

#!/usr/bin/env python3
"""Re-judge the llm graders of a saved `claude plugin eval --json` result, with reasons.

`claude plugin eval` (2.1.322) asks its judge for one word, three times, and keeps
only the votes ("judge votes: FAIL FAIL PASS"); it has no option to keep the judge's
reasoning. This script re-scores the saved replies with the SAME criteria and the
same prompt the eval builds (system "You are a strict, terse evaluation judge for
coding-agent traces.", then "You are grading the output of a coding agent against a
criterion.", the criterion, the agent output), changing only the last line: the judge
answers PASS or FAIL and then says why. The criteria are read from the result file
unchanged; nothing here decides pass or fail for the suite.

    python3 tools/rejudge_llm.py evals/results/gauntlet.json [--case GLOB] [--only-failed]
        [--model sonnet] [--votes 1] [--out reasons.md]

It calls the judge through `claude -p --safe-mode` (no tools, MCP, settings or CLAUDE.md), on your own
credential, a cent or two a call. Output: one block per case, run and llm grader:
the eval's own votes, the re-judge's verdict and its reason.
"""
import argparse
import fnmatch
import json
import subprocess
import tempfile
import sys

SYSTEM = "You are a strict, terse evaluation judge for coding-agent traces."
HEAD = "You are grading the output of a coding agent against a criterion."
ONE_WORD = "Respond with exactly one word: PASS or FAIL."
ASK = (
    "Respond with PASS or FAIL on the first line. Then, in at most five short lines, "
    "name each part of the criterion the output misses, quoting the exact words from "
    "the output that miss it. If it passes, say so in one line."
)


def judge(criteria, focus, text, model, one_word=False):
    # The eval's own layout (claude 2.1.322), with only the last line changed.
    prompt = f"{HEAD}\n\nCriterion:\n{criteria}\n\nAgent output ({focus}):\n{text}\n\n{ONE_WORD if one_word else ASK}"
    r = subprocess.run(
        ["claude", "-p", "--safe-mode", "--model", model, "--system-prompt", SYSTEM, "--tools", "",
         "--strict-mcp-config", "--setting-sources", "", "--no-session-persistence",
         "--output-format", "text"],
        input=prompt, capture_output=True, text=True, timeout=300, cwd=tempfile.gettempdir(),
    )
    if r.returncode != 0:
        raise SystemExit(f"judge call failed ({r.returncode}): {r.stderr.strip()[:500]}")
    out = r.stdout.strip()
    first = out.splitlines()[0] if out else ""
    verdict = "PASS" if "PASS" in first.upper() and "FAIL" not in first.upper() else "FAIL"
    return verdict, out


def walk(result):
    """Yield (case, run_index, grader_result, grader_config) for every llm grader result."""
    for c in result.get("cases", []):
        defs = {g["name"]: g for g in c.get("graders", []) if g.get("type") == "llm"}
        for i, run in enumerate(c.get("arms", {}).get("with", [])):
            for g in run.get("graders", []):
                if g.get("name") in defs:
                    yield c["name"], i + 1, g, defs[g["name"]].get("config", {})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("result")
    ap.add_argument("--case", default="*")
    ap.add_argument("--only-failed", action="store_true")
    ap.add_argument("--model", default="sonnet")
    ap.add_argument("--votes", type=int, default=1)
    ap.add_argument("--one-word", action="store_true",
                    help="ask exactly as the eval does (one word), to calibrate against its votes")
    ap.add_argument("--out")
    a = ap.parse_args()
    result = json.load(open(a.result))
    lines = []
    for case, n, g, d in walk(result):
        if not fnmatch.fnmatch(case or "", a.case):
            continue
        if a.only_failed and g.get("passed"):
            continue
        criteria = d.get("criteria")
        if not criteria:
            print(f"skip {case} run {n} {g.get('name')}: criteria not in the result file", file=sys.stderr)
            continue
        focus = d.get("focus") or "last_message"
        focus = focus if isinstance(focus, str) else f"file {focus.get('path')}"
        # `evidence` is the exact text the eval showed its judge.
        verdicts = [judge(criteria, focus, g.get("evidence", ""), a.model, a.one_word) for _ in range(a.votes)]
        lines.append(f"## {case} run {n} {g.get('name')}")
        votes = " ".join("PASS" if v else "FAIL" for v in g.get("judgeVotes", []))
        lines.append(f"eval: {'PASS' if g.get('passed') else 'FAIL'} (votes {votes})")
        for v, why in verdicts:
            lines.append(f"re-judge: {v}\n{why}\n")
        print("\n".join(lines[-(2 + len(verdicts)):]), flush=True)
    if a.out:
        open(a.out, "w").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()

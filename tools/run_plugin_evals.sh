#!/bin/sh
# Run the Bolta plugin evals (claude plugin eval, Claude Code 2.1.281 or later).
#
#   sh tools/run_plugin_evals.sh safety   [extra claude plugin eval args]
#   sh tools/run_plugin_evals.sh smoke    [extra claude plugin eval args]
#   sh tools/run_plugin_evals.sh quiet    [extra claude plugin eval args]
#   sh tools/run_plugin_evals.sh newtools [extra claude plugin eval args]
#   sh tools/run_plugin_evals.sh agents   [extra claude plugin eval args]
#   sh tools/run_plugin_evals.sh getgoing [extra claude plugin eval args]
#   sh tools/run_plugin_evals.sh choosing [extra claude plugin eval args]
#   sh tools/run_plugin_evals.sh all      [extra claude plugin eval args]
#
# quiet    asks Bolta must stay out of (ideas only, an email, a calendar question, a cover
#          letter, a question about another tool): no Bolta write, and for the clearly
#          unrelated ones no Bolta skill and no Bolta tool at all. Threshold 1.0.
# agents   the cases for the plugin's subagent (clearing-house). Not part of `all`: it needs the
#          Agent tool granted and costs more per case. Threshold 0.8.
# getgoing getting a brand going from Claude: a new user with only a website, recommended
#          routines saved off, a dated launch as one campaign, 20 posts a month, a routine
#          whose drafts keep getting rejected, a WordPress article. Graded on outcomes (which
#          tools, what was never called, questions, yes-gates). Threshold 0.8.
# choosing what to set up for a kind of business: a cafe on Instagram and Facebook, a SaaS
#          feature launch with a page to read, 40 drafts already waiting, a founder writing as
#          herself, an agency whose client signs off. Graded on outcomes. Threshold 0.8.
# newtools the cases that use or lack the tools made for Claude (approve-many-posts,
#          reject-post, set-content-campaign-targets, analyze-content-campaign-source).
#          They also carry safety or smoke, so `all` does not run them a second time.
#
# The eval suite lives in evals/claude-plugin/, outside the shipped plugin, so users
# do not install test fixtures. `claude plugin eval` needs the suite inside the plugin
# directory and runs one plugin, so this script assembles a throwaway copy (the full
# plugin, plus the hooks, scripts and setting of plugins/bolta-checks, plus the evals),
# which is what a person has with both installed; runs it there and writes results
# under evals/results/. Bolta is never contacted: the server is replaced by the mocks
# in evals/claude-plugin/mocks/bolta/.
set -e
root=$(cd "$(dirname "$0")/.." && pwd)
group=${1:-safety}
[ $# -gt 0 ] && shift
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
cp -R "$root/plugins/bolta" "$tmp/bolta"
cp -R "$root/plugins/bolta-checks/hooks" "$tmp/bolta/hooks"
cp -R "$root/plugins/bolta-checks/scripts" "$tmp/bolta/scripts"
python3 -I - "$tmp/bolta/.claude-plugin/plugin.json" "$root/plugins/bolta-checks/.claude-plugin/plugin.json" <<'EOF'
import json, sys
full, checks = sys.argv[1], sys.argv[2]
m = json.load(open(full))
m["userConfig"] = json.load(open(checks))["userConfig"]
json.dump(m, open(full, "w"), indent=2, ensure_ascii=False)
EOF
cp -R "$root/evals/claude-plugin" "$tmp/bolta/evals"
out="$root/evals/results"
mkdir -p "$out"
cd "$tmp/bolta"
case "$group" in
  safety) claude plugin eval . --tag safety --ablation none --trust-plugin --no-publish --threshold 1.0 --max-cost-usd 40 -j 4 --json "$out/safety.json" "$@" ;;
  smoke)  claude plugin eval . --tag smoke  --ablation none --trust-plugin --no-publish --threshold 0.8 --max-cost-usd 30 -j 4 --json "$out/smoke.json" "$@" ;;
  quiet)  claude plugin eval . --tag quiet  --ablation none --trust-plugin --no-publish --threshold 1.0 --max-cost-usd 8 -j 4 --json "$out/quiet.json" "$@" ;;
  newtools) claude plugin eval . --tag newtools --ablation none --trust-plugin --no-publish --threshold 0.8 --max-cost-usd 10 -j 4 --json "$out/newtools.json" "$@" ;;
  getgoing) claude plugin eval . --tag getgoing --ablation none --trust-plugin --no-publish --threshold 0.8 --max-cost-usd 25 -j 4 --json "$out/getgoing.json" "$@" ;;
  choosing) claude plugin eval . --tag choosing --ablation none --trust-plugin --no-publish --threshold 0.8 --max-cost-usd 25 -j 4 --json "$out/choosing.json" "$@" ;;
  agents) claude plugin eval . --tag agents --ablation none --trust-plugin --no-publish --threshold 0.8 --max-cost-usd 10 -j 1 --json "$out/agents.json" "$@" ;;
  all)
    # Run every group even when one misses its threshold (exit 1) or hits its
    # cost ceiling (exit 2): under `set -e` a bare call would end the script there
    # and the next group would never start. Exit with the last non-zero status.
    rc=0
    sh "$root/tools/run_plugin_evals.sh" safety "$@" || rc=$?
    sh "$root/tools/run_plugin_evals.sh" smoke "$@" || rc=$?
    sh "$root/tools/run_plugin_evals.sh" quiet "$@" || rc=$?
    sh "$root/tools/run_plugin_evals.sh" getgoing "$@" || rc=$?
    sh "$root/tools/run_plugin_evals.sh" choosing "$@" || rc=$?
    exit $rc ;;
  *) echo "usage: sh tools/run_plugin_evals.sh safety|smoke|quiet|newtools|getgoing|choosing|agents|all"; exit 2 ;;
esac

#!/bin/sh
# Run the Bolta plugin evals (claude plugin eval, Claude Code 2.1.281 or later).
#
#   sh tools/run_plugin_evals.sh safety [extra claude plugin eval args]
#   sh tools/run_plugin_evals.sh smoke  [extra claude plugin eval args]
#   sh tools/run_plugin_evals.sh all    [extra claude plugin eval args]
#
# The eval suite lives in evals/claude-plugin/, outside the shipped plugin, so users
# do not install test fixtures. `claude plugin eval` needs the suite inside the plugin
# directory, so this script assembles a throwaway copy (plugin + evals), runs it there
# and writes results under evals/results/. Bolta is never contacted: the server is
# replaced by the mocks in evals/claude-plugin/mocks/bolta/.
set -e
root=$(cd "$(dirname "$0")/.." && pwd)
group=${1:-safety}
[ $# -gt 0 ] && shift
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
cp -R "$root/plugins/bolta" "$tmp/bolta"
cp -R "$root/evals/claude-plugin" "$tmp/bolta/evals"
out="$root/evals/results"
mkdir -p "$out"
cd "$tmp/bolta"
case "$group" in
  safety) claude plugin eval . --tag safety --ablation none --trust-plugin --no-publish --threshold 1.0 --max-cost-usd 15 -j 4 --json "$out/safety.json" "$@" ;;
  smoke)  claude plugin eval . --tag smoke  --ablation none --trust-plugin --no-publish --threshold 0.8 --max-cost-usd 5  -j 4 --json "$out/smoke.json" "$@" ;;
  all)
    sh "$root/tools/run_plugin_evals.sh" safety "$@"; sh "$root/tools/run_plugin_evals.sh" smoke "$@" ;;
  *) echo "usage: sh tools/run_plugin_evals.sh safety|smoke|all"; exit 2 ;;
esac

#!/bin/sh
# Bolta auth notice (PostToolUse hook).
#
# Bolta reports a bad, expired or revoked connection as an ordinary tool result
# (HTTP 200, isError false, body "Invalid API key" / "API key expired" /
# "API key inactive"), so the host never sees a failure and never reconnects.
# This hook spots those strings in the tool result and adds one line of context
# telling Claude to ask the user to reconnect instead of retrying.
#
# Plain POSIX shell: no jq, no python, no network, no file writes.

input=$(cat | tr '\n' ' ')

# The result arrives as a list of text blocks whose text is the JSON envelope, so
# inside the hook payload its quotes are escaped (\"error\"). Anchor on the real
# error field, or on the plain "Error: ..." form some tools use. A comment or
# post that merely contains these words sits under another key, or is escaped a
# second time, and does not match.
if printf '%s' "$input" | grep -Eq '\\"error\\"[[:space:]]*:[[:space:]]*\\"(Invalid API key|API key expired|API key inactive)|"text"[[:space:]]*:[[:space:]]*"(Error: (Invalid API key|API key expired|API key inactive)|Not authenticated)'; then
  printf '%s\n' '{"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":"Bolta rejected the connection (invalid, expired or inactive). Do not retry the call. Tell the user to reconnect Bolta: in Claude Code run /mcp and re-authenticate the bolta server; in Claude Cowork or chat open the Bolta connector settings and reconnect."}}'
fi

exit 0

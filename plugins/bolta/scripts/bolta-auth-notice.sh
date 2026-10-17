#!/bin/sh
# Bolta auth notice (PostToolUse and PostToolUseFailure hook).
#
# Bolta reports a bad, expired or revoked connection in one of two ways:
#   - as an ordinary tool result (isError false, body "Invalid API key" /
#     "API key expired" / "API key inactive"). Claude Code then runs PostToolUse
#     and the text sits in tool_response.
#   - for tools that draw a Bolta card, as an error result ("Error: Invalid API
#     key", isError true). Claude Code then runs PostToolUseFailure and the text
#     sits in the top-level error field.
# Either way the host never reconnects by itself. This hook spots those strings
# and adds one line of context telling Claude to ask the user to reconnect
# instead of retrying.
#
# Plain POSIX shell: no network, no file writes.

input=$(cat | tr '\n' ' ')

event=PostToolUse
case $input in
  *'"hook_event_name":"PostToolUseFailure"'*|*'"hook_event_name": "PostToolUseFailure"'*) event=PostToolUseFailure ;;
esac

# The result arrives as a list of text blocks whose text is the JSON envelope, so
# inside the hook payload its quotes are escaped (\"error\"). Anchor on the real
# error field, or on the plain "Error: ..." form some tools use. A comment or
# post that merely contains these words sits under another key, or is escaped a
# second time, and does not match.
hit=0
if printf '%s' "$input" | grep -Eq '\\"error\\"[[:space:]]*:[[:space:]]*\\"(Invalid API key|API key expired|API key inactive)|"text"[[:space:]]*:[[:space:]]*"(Error: (Invalid API key|API key expired|API key inactive)|Not authenticated)'; then
  hit=1
fi
# On a failed call the message is the top-level error string. It must start with
# the phrase, or reach it straight after a short "...: " prefix such as "Error: ".
if [ "$event" = PostToolUseFailure ] && printf '%s' "$input" | grep -Eq '"error"[[:space:]]*:[[:space:]]*"([^"\\]{0,40}: )?(Invalid API key|API key expired|API key inactive|Not authenticated)'; then
  hit=1
fi

if [ "$hit" = 1 ]; then
  printf '{"hookSpecificOutput":{"hookEventName":"%s","additionalContext":"Bolta rejected the connection (invalid, expired or inactive). Do not retry the call. Tell the user, in plain words, to reconnect Bolta: in Claude Code run /mcp and sign in to bolta again; in Cowork or claude.ai open Customize, then Connectors, and press Reconnect on Bolta."}}\n' "$event"
fi

exit 0

#!/bin/sh
# Bolta write guard (PreToolUse hook).
#
# Reads the hook JSON on stdin and, for any Bolta tool call that goes public,
# approves a post, automates something or deletes, asks the user to confirm.
# Everything else (drafts, reads) exits silently so the normal permission flow
# applies. It never allows, never denies, never touches the network and never
# writes a file; it only prints an "ask" decision.
#
# Plain POSIX shell on purpose: no jq, no python.
# Tool names arrive as mcp__plugin_bolta_bolta__<tool> (plugin install) or
# mcp__<server>__<tool> (user-added server); only the final segment matters.
#
# CLAUDE_PLUGIN_OPTION_CONFIRM_SCOPE:
#   all-external-effects (default) - also confirm routines, deletes, campaign status
#   publish-only                   - confirm only what goes public or approves a post

input=$(cat | tr '\n' ' ')
name=$(printf '%s' "$input" \
  | grep -o '"tool_name"[[:space:]]*:[[:space:]]*"[^"]*"' \
  | head -1 \
  | sed 's/.*:[[:space:]]*"\([^"]*\)"/\1/')
tool=${name##*__}
scope=${CLAUDE_PLUGIN_OPTION_CONFIRM_SCOPE:-all-external-effects}

# $1 must contain no double quotes and no backslashes.
ask() {
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask","permissionDecisionReason":"Confirmation needed (Bolta plugin safety check): %s"}}\n' "$1"
  exit 0
}

# Does the tool input carry a publish or schedule intent? Case-insensitive
# (the server lower-cases requested_action) and a non-null scheduled_time also
# means "schedule it". The key must be a real JSON key, so post text that merely
# contains the words (its quotes are escaped) does not match.
has_intent() {
  printf '%s' "$input" | grep -Eiq '"(requested_action|action|status)"[[:space:]]*:[[:space:]]*"[[:space:]]*(publish|schedule|scheduled|published)|"scheduled_time"[[:space:]]*:[[:space:]]*"[^"]'
}

case "$tool" in
  publish-post)
    ask "Bolta will publish this post to the live platform now. This is public and cannot be undone. The exact text and accounts are in the chat above; continue only if they match what you agreed." ;;
  schedule-post)
    ask "Bolta will schedule this post to go out at the stated time. The exact text, accounts and time are in the chat above; continue only if they match what you agreed." ;;
  approve-post|approve-recurring-review)
    ask "Approving schedules this post for publishing. The exact text and accounts are in the chat above; approve only if they match what you agreed." ;;
  send-outreach-reply|publish-engagement-reply|reply-to-social-content)
    ask "Bolta will post a public reply as your connected account. Confirm the exact text, the target URL, the account and the workspace first." ;;
  react-to-social-content)
    ask "Bolta will react publicly as your connected account. Confirm the target and the account first." ;;
  create-post|bulk-create-posts|create-wordpress-blog-post)
    if has_intent; then
      ask "This call would schedule or publish content instead of saving a draft. Create drafts first, then confirm the workspace, accounts, exact text and time."
    fi ;;
  update-post)
    if printf '%s' "$input" | grep -Eiq '"scheduled_time"[[:space:]]*:|"status"[[:space:]]*:[[:space:]]*"(Scheduled|Published|Approved)"'; then
      ask "This edit changes when or whether a post goes out. An edited approved or scheduled post needs a fresh approval. Confirm the change first."
    fi ;;
  update-business-dna|update-voice-profile)
    if [ "$scope" != "publish-only" ]; then
      ask "This changes the brand profile that every draft, routine and agent writes from. Review the before and after in the chat above first."
    fi ;;
  create-routine|update-routine)
    if [ "$scope" != "publish-only" ]; then
      ask "This sets up or changes automation that can create content on a schedule. Confirm which routine, its schedule and what happens to its output first."
    fi ;;
  activate-routine|resume-routine|run-routine-now)
    if [ "$scope" != "publish-only" ]; then
      ask "This starts automation that can create content on a schedule. Confirm which routine, when it runs and what happens to its output first."
    fi ;;
  delete-post|archive-routine|set-content-campaign-status)
    if [ "$scope" != "publish-only" ]; then
      ask "This removes or changes the status of Bolta content. A deleted post can be restored for 7 days. Confirm which item first."
    fi ;;
esac

exit 0

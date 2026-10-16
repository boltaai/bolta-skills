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

# --- How intent is detected --------------------------------------------------
# Claude Code sends some array parameters, notably the items of bulk-create-posts,
# as JSON-ENCODED STRINGS (the advertised schema says so), and the Bolta server
# parses them. Inside such a string every quote is backslash-escaped in this
# payload, so a plain "status" match cannot see it. (\\*") below matches a quote
# preceded by any number of backslashes, so one pattern covers both forms.
#
# The checks use an ALLOW-LIST, not a deny-list: the server trims and lower-cases
# these values, so a list of bad words is easy to get around (for example a value
# padded with an escaped tab). A value is safe only if it is exactly one of the
# safe words. Anything else asks. Post text that merely looks like JSON also asks;
# that costs one click and is the right side to err on.

# Succeeds if any value of the given keys is not exactly one of the safe words.
# $1 = key alternation, $2 = safe-word alternation
unsafe_values() {
  printf '%s' "$input" \
    | grep -Eio '(\\*")('"$1"')(\\*")[[:space:]]*:[[:space:]]*(\\*")[^"]*' \
    | grep -Eiv ':[[:space:]]*(\\*")('"$2"')\\*$' \
    | grep -q .
}

# A scheduled_time with any value other than null means "schedule it".
has_time() {
  printf '%s' "$input" | grep -Eiq '(\\*")scheduled_time(\\*")[[:space:]]*:[[:space:]]*[^n[:space:]]'
}

# update-post: strict on purpose (a real top-level key with the exact value), so
# text inside a post body cannot fake it.
returns_to_draft() {
  printf '%s' "$input" | grep -Eiq '"status"[[:space:]]*:[[:space:]]*"draft"'
}
has_edit_fields() {
  printf '%s' "$input" | grep -Eq '"(content|contents|media|accounts|poll)"[[:space:]]*:'
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
  bulk-create-posts)
    # Always asks, in every scope: the items arrive as JSON-encoded strings and the
    # server may honour keys this script does not know, so it cannot reliably tell a
    # batch of drafts from a batch of scheduled posts.
    ask "Bolta will create several posts at once. The posts, accounts and times are in the chat above; continue only if they match. This prompt appears for every batch because the plugin cannot reliably see inside one to tell drafts from scheduled posts." ;;
  create-post|create-wordpress-blog-post)
    if has_time || unsafe_values 'requested_action|action|status' 'draft|submit_for_review'; then
      ask "This call would schedule or publish content, or sets something the plugin cannot confirm is a plain draft. Create a draft first, then confirm the workspace, accounts, exact text and time."
    fi ;;
  update-post)
    # An edit keeps a post's approval, and the hook cannot see the post's status, so an
    # edit to an approved or scheduled post would go out under the old approval. An edit
    # is silent only when the same call sets status Draft (which also takes the post out
    # of the schedule and forces a fresh approval).
    if has_time || unsafe_values 'status' 'draft'; then
      ask "This edit changes when or whether a post goes out. An edited approved or scheduled post needs a fresh approval. Confirm the change first."
    fi
    if has_edit_fields && ! returns_to_draft; then
      ask "Editing a post that may already be approved or scheduled keeps its approval, so the edited text would go out as approved. Set it back to Draft in the same call, or confirm this edit first."
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

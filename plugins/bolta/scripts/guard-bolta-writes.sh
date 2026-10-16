#!/bin/sh
# Bolta write guard (PreToolUse hook).
#
# Reads the hook JSON on stdin and, for any Bolta tool call that goes public,
# approves a post, changes what an existing post will publish, automates
# something or deletes, asks the user to confirm. Everything else exits silently
# so the normal permission flow applies. It never allows, never denies, never
# touches the network and never writes a file; it only prints an "ask" decision.
#
# Plain POSIX shell plus awk (a standard POSIX tool): no jq, no python.
# Tool names arrive as mcp__plugin_bolta_bolta__<tool> (plugin install) or
# mcp__<server>__<tool> (user-added server); only the final segment matters.
#
# CLAUDE_PLUGIN_OPTION_CONFIRM_SCOPE:
#   all-external-effects (default) - also confirm routines, deletes, campaign status,
#                                    brand-profile edits
#   publish-only                   - confirm only what goes public, approves a post or
#                                    changes what an existing post will publish
#
# --- How the tool input is read ---------------------------------------------
# The payload is parsed, not pattern-matched. A regex over raw JSON cannot tell a
# top-level key from one nested inside media, poll or a JSON-encoded string, and
# the server's own parser is lenient (it trims and lower-cases values and accepts
# JSON-encoded strings for array parameters). The scanner below walks the JSON
# once and reports only the TOP-LEVEL keys of tool_input and their value types.
# Decisions use an ALLOW-LIST: a value is safe only if it is exactly a safe word,
# so padding, escapes and unknown values all ask. If the call cannot be read at
# all, the guard asks (fail closed).

input=$(cat)
TAB=$(printf '\t')

# Output lines:
#   T<TAB>raw                       top-level tool_name
#   I                               a tool_input object was found
#   K<TAB>key<TAB>type<TAB>raw      top-level key of tool_input; type S string,
#                                   N null, O anything else. raw is kept only for
#                                   status, requested_action, action, scheduled_time.
#   BAD                             the JSON could not be walked
parsed=$(printf '%s' "$input" | awk '
function ws(ch) { return ch == " " || ch == "\t" || ch == "\n" || ch == "\r" }
function strend(str, k,   m, len, ch, esc) {
  len = length(str); esc = 0
  for (m = k + 1; m <= len; m++) {
    ch = substr(str, m, 1)
    if (esc) esc = 0
    else if (ch == "\\") esc = 1
    else if (ch == "\"") return m
  }
  return 0
}
BEGIN { RS = "\001" }
{
  s = $0; n = length(s); depth = 0; inti = 0; tid = 0; want = 0; bad = 0
  i = 1
  while (i <= n) {
    c = substr(s, i, 1)
    if (c == "\"") {
      e = strend(s, i)
      if (e == 0) { bad = 1; break }
      tok = substr(s, i + 1, e - i - 1)
      j = e + 1
      while (j <= n && ws(substr(s, j, 1))) j++
      if (substr(s, j, 1) == ":") {
        k = j + 1
        while (k <= n && ws(substr(s, k, 1))) k++
        v = substr(s, k, 1)
        raw = ""; typ = "O"
        if (v == "\"") {
          ve = strend(s, k)
          if (ve == 0) { bad = 1; break }
          raw = substr(s, k + 1, ve - k - 1); typ = "S"
        } else if (substr(s, k, 4) == "null") {
          typ = "N"
        }
        if (depth == 1 && tok == "tool_name" && typ == "S") print "T\t" raw
        if (depth == 1 && tok == "tool_input" && v == "{") want = 1
        if (inti && depth == tid) {
          keep = (tok == "status" || tok == "requested_action" || tok == "action" || tok == "scheduled_time")
          print "K\t" tok "\t" typ "\t" (keep ? raw : "")
        }
      }
      i = e + 1
      continue
    }
    if (c == "{" || c == "[") {
      depth++
      if (want && c == "{") { inti = 1; tid = depth; want = 0; print "I" }
    } else if (c == "}" || c == "]") {
      if (inti && depth == tid) inti = 0
      depth--
    }
    i++
  }
  if (bad || depth != 0) print "BAD"
}' 2>/dev/null) || parsed="BAD"

has_line() { printf '%s\n' "$parsed" | grep -Eq "$1"; }
key_lines() { printf '%s\n' "$parsed" | grep -E "^K${TAB}($1)${TAB}"; }

tool=$(printf '%s\n' "$parsed" | sed -n "s/^T${TAB}//p" | head -1)
tool=${tool##*__}
scope=${CLAUDE_PLUGIN_OPTION_CONFIRM_SCOPE:-all-external-effects}

# $1 must contain no double quotes and no backslashes.
ask() {
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask","permissionDecisionReason":"Confirmation needed (Bolta plugin safety check): %s"}}\n' "$1"
  exit 0
}

if [ -z "$tool" ] || has_line '^BAD$' || ! has_line '^I$'; then
  ask "The plugin could not read this tool call, so it cannot tell what it would do. Confirm it before continuing."
fi

# create-post and create-wordpress-blog-post: every declared intent must be exactly
# draft or submit_for_review (or null). The server trims and lower-cases these
# values, so anything else, including a padded or escaped value, asks.
unsafe_intent() {
  key_lines 'requested_action|action|status' \
    | grep -Eiv "^K${TAB}[a-z_]+${TAB}(S${TAB}(draft|submit_for_review)|N${TAB})\$" \
    | grep -q .
}

# A scheduled_time with any value other than null means "schedule it".
has_time() {
  key_lines 'scheduled_time' | grep -Ev "^K${TAB}scheduled_time${TAB}N${TAB}\$" | grep -q .
}

# update-post. An edit keeps a post's approval and the hook cannot see the post's
# status, so an edit to an Approved or Scheduled post would go out under the old
# approval. Only a TOP-LEVEL status of exactly Draft in the same call is accepted
# as the reset (a status nested inside media or poll is not a top-level key here).
returns_to_draft() {
  key_lines 'status' | grep -Eiq "^K${TAB}status${TAB}S${TAB}draft\$"
}
status_not_draft() {
  key_lines 'status' | grep -Eiv "^K${TAB}status${TAB}S${TAB}draft\$" | grep -q .
}
has_edit_fields() {
  key_lines 'content|contents|media|accounts|poll' | grep -q .
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
    if has_time || unsafe_intent; then
      ask "This call would schedule or publish content, or sets something the plugin cannot confirm is a plain draft. Create a draft first, then confirm the workspace, accounts, exact text and time."
    fi ;;
  update-post)
    # Any time, or a status that is not exactly Draft, changes when or whether a post goes out.
    if has_time || status_not_draft; then
      ask "This edit changes when or whether a post goes out. An edited approved or scheduled post needs a fresh approval. Confirm the change first."
    fi
    if has_edit_fields && ! returns_to_draft; then
      ask "Editing a post that may already be approved or scheduled keeps its approval, so the edited text would go out as approved. Set it back to Draft in the same call, or confirm this edit first."
    fi ;;
  update-post-platform-details)
    # Platform fields (subreddit, titles, privacy, links, polls) change what an
    # existing post publishes, and an edit keeps the post's approval.
    ask "This changes platform settings (such as a subreddit, title, privacy or link) on an existing post, which keeps its approval and changes what is published. Confirm the change in the chat above first." ;;
  update-social-bucket)
    # The publisher reads a bucket's members live, so editing a bucket changes where
    # posts that are already attached to it will go out.
    ask "Changing a bucket changes where every post already attached to it will publish. Confirm the new list of accounts in the chat above first." ;;
  restore-deleted)
    # A restored post keeps its old status; a Scheduled post whose time has passed can be sent late.
    ask "Restoring brings the item back with its old status, and a scheduled post whose time has passed can be published late. Confirm which item first." ;;
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

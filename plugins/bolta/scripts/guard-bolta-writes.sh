#!/bin/sh
# Bolta write guard v2 (PreToolUse hook).
#
# Reads the hook JSON on stdin. For a Bolta call that goes public, approves,
# schedules, deletes, says a final no, spends credits right now, can't be
# undone, changes what drafts are written from, or switches on something that
# could post without the user, it prints an "ask" decision. Everything else
# exits silently, so Claude Code's own permission setting applies. It never
# allows and never denies: the only decision it can print is "ask". It never
# touches the network and never writes a file; it only reads the small marker
# files the other Bolta hooks keep.
#
# Plain POSIX shell plus awk. The JSON is parsed structurally by
# bolta-json.sh (next to this script), never pattern-matched. Decisions use
# allow-lists: a value is safe only if it is exactly a safe word. If the call
# cannot be read, the guard asks (fail closed).
#
# CLAUDE_PLUGIN_OPTION_CONFIRM_LEVEL:
#   standard (default)  drafts and sending for review pass; the first approval,
#                       schedule or delete in a reply asks, and later ones in
#                       the same reply on the same connection pass (see the
#                       two kinds of window below).
#   careful             every gated call asks, except pausing a campaign.
#   anything else       treated as careful.
#
# The batch window. bolta-new-turn.sh runs on every user message: it closes all
# windows and writes a fresh turn marker. bolta-mark.sh runs after a
# successful call and opens a window for that connection only, stamped with
# the current turn's token, the time it opened and the message's prompt_id
# (Claude Code puts the same prompt_id on every hook of one user message).
# There are two kinds, so an OK on a delete never lets a post go public:
#   win-go-<connection>    opened by approve-post, approve-recurring-review or
#                          schedule-post. Covers approvals, schedules and
#                          deletes.
#   win-del-<connection>   opened by delete-post. Covers deletes only.
# Markers live in ${TMPDIR:-/tmp}/bolta-plugin/<session>/.
# A call passes silently on a window only when all of this holds; anything
# else asks:
#   - the call carries a prompt_id (hosts that send none ask every time);
#   - the marker directories are real directories (not symlinks), owned by
#     this user and not writable by anyone else;
#   - turn and the window are plain files that read cleanly;
#   - the window carries the current turn's token, so it was opened after the
#     latest user message, and the turn marker is not newer than it;
#   - the window was opened under this call's prompt_id, so it belongs to this
#     message even if the new-message hook never ran;
#   - the window opened 600 seconds ago or less.
# A Bolta routine created in this session as "ask me first" leaves a
# routine-<connection>-<id> marker ("<turn token> <epoch seconds>"). Only that
# routine may be switched on, or changed without a policy, with no check, and
# only for 24 hours after it was made.
#
# These checks trust their marker files. A process that can write files as
# this user (including Claude, if it may run shell commands without asking)
# could forge one; the plugin's README says so.

here=$(dirname "$0")
reader="$here/bolta-json.sh"

ok=0 tool="" server="" sid="" prompt="" conn="Bolta"
create="" update="" policy="" rid="" action="" bulk=""
parsed=$(sh "$reader" guard 2>/dev/null) || parsed=""
while IFS='=' read -r k v; do
  case $k in
    OK) ok=$v ;;
    TOOL) tool=$v ;;
    SERVER) server=$v ;;
    SID) sid=$v ;;
    PROMPT) prompt=$v ;;
    CONN) conn=$v ;;
    CREATE) create=$v ;;
    UPDATE) update=$v ;;
    POLICY) policy=$v ;;
    RID) rid=$v ;;
    ACTION) action=$v ;;
    BULK) bulk=$v ;;
  esac
done <<EOF
$parsed
EOF

careful=1
if [ "${CLAUDE_PLUGIN_OPTION_CONFIRM_LEVEL:-standard}" = standard ]; then careful=0; fi

base="${TMPDIR:-/tmp}/bolta-plugin"
dir="$base/$sid"

# $1 must contain no double quotes and no backslashes. Every sentence in it
# stays under 20 words (tools/test_hooks.sh checks).
ask() {
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask","permissionDecisionReason":"%s"}}\n' "$1"
  exit 0
}

# A marker directory is usable only if it is a real directory owned by this
# user that nobody else can write to.
dir_ok() {
  [ -d "$1" ] && [ ! -L "$1" ] || return 1
  me=$(id -u 2>/dev/null) || return 1
  [ -n "$me" ] || return 1
  ls -nd "$1" 2>/dev/null | awk -v me="$me" '
    NR == 1 { m = $1; bad = ($3 != me) || substr(m, 6, 1) == "w" || substr(m, 9, 1) == "w" }
    END { exit (NR == 0 || bad) ? 1 : 0 }'
}

file_ok() { [ -f "$1" ] && [ ! -L "$1" ]; }

# Reads "<token> <epoch seconds> [prompt id]" from a marker file into m_tok,
# m_time and m_prompt ("-" or nothing means no prompt id).
read_marker() {
  m_tok="" m_time="" m_prompt=""
  IFS=' ' read -r m_tok m_time m_prompt m_rest 2>/dev/null < "$1" || [ -n "$m_tok" ] || return 1
  [ "$m_prompt" = "-" ] && m_prompt=""
  case $m_tok in ''|*[!A-Za-z0-9_-]*) return 1 ;; esac
  case $m_time in ''|*[!0-9]*) return 1 ;; esac
  [ "${#m_tok}" -le 128 ] && [ "${#m_time}" -le 12 ]
}

now() {
  t=$(date +%s 2>/dev/null)
  case $t in ''|*[!0-9]*) t=$(awk 'BEGIN { srand(); print srand() }' 2>/dev/null) ;; esac
  case $t in ''|*[!0-9]*) return 1 ;; esac
  [ "$t" -gt 1500000000 ] || return 1
  echo "$t"
}

# window_open <kind...>: true if a window of one of these kinds is open for
# this connection, this message and this prompt_id.
window_open() {
  [ -n "$sid" ] && [ -n "$server" ] && [ -n "$prompt" ] || return 1
  dir_ok "$base" && dir_ok "$dir" || return 1
  turn="$dir/turn"
  file_ok "$turn" || return 1
  read_marker "$turn" || return 1
  t_tok=$m_tok t_time=$m_time
  for kind in "$@"; do
    win="$dir/win-$kind-$server"
    file_ok "$win" || continue
    read_marker "$win" || continue
    [ "$m_tok" = "$t_tok" ] || continue
    [ "$m_prompt" = "$prompt" ] || continue
    [ "$m_time" -ge "$t_time" ] || continue
    if [ "$turn" -nt "$win" ] 2>/dev/null; then continue; fi
    n=$(now) || continue
    age=$((n - m_time))
    [ "$age" -ge 0 ] && [ "$age" -le 600 ] && return 0
  done
  return 1
}

# The routine in this call was created in this session as "ask me first",
# within the last 24 hours.
routine_marked() {
  [ -n "$sid" ] && [ -n "$server" ] && [ -n "$rid" ] || return 1
  dir_ok "$base" && dir_ok "$dir" || return 1
  f="$dir/routine-$server-$rid"
  file_ok "$f" && read_marker "$f" || return 1
  n=$(now) || return 1
  age=$((n - m_time))
  [ "$age" -ge 0 ] && [ "$age" -le 86400 ]
}

batch_ask() {
  if [ "$careful" = 1 ]; then
    go="Careful mode asks every time." del=$go
  else
    go="After you OK it, this reply's other approvals, schedules and deletes skip this check."
    del="After you OK it, this reply's other deletes skip this check."
  fi
  case $tool in
    schedule-post) ask "Check before it goes out ($conn): you are scheduling posts from the list above. $go" ;;
    delete-post) ask "Check before deleting ($conn): you are deleting posts from the list above. A deleted post can be restored for 7 days. $del" ;;
    *) ask "Check before it goes out ($conn): you are approving posts from the list above. $go" ;;
  esac
}

campaign_ask() {
  case $action in
    activate) ask "Uses credits now ($conn): Bolta will start writing this campaign." ;;
    resume) ask "Check before switching on ($conn): the campaign starts again. Bolta goes back to writing the weeks still to come." ;;
    complete) ask "This can't be undone ($conn): a finished campaign can't be started again. Its results stay." ;;
    archive) ask "This can't be undone ($conn): a retired campaign can't be started again. Its posts stay." ;;
    *) ask "Bolta check ($conn): the plugin can't tell what this campaign change does. OK it only if you expected it." ;;
  esac
}

if [ "$ok" != 1 ] || [ -z "$tool" ]; then
  ask "Bolta check ($conn): the plugin could not read this request, so it can't tell what it does. OK it only if you expected it."
fi

case "$tool" in
  publish-post)
    ask "Check before it goes out ($conn): this post goes public right now and can't be undone. OK only if the text and account match what you agreed." ;;
  send-outreach-reply|publish-engagement-reply|reply-to-social-content)
    ask "Check before it goes out ($conn): this reply goes public right now, under your account. OK only if you have seen this exact text and where it goes." ;;
  react-to-social-content)
    ask "Check before it goes out ($conn): this reaction is public, under your account. OK only if the post and the account are right." ;;
  approve-post|approve-recurring-review|schedule-post)
    if [ "$careful" = 0 ] && window_open go; then exit 0; fi
    batch_ask ;;
  delete-post)
    if [ "$careful" = 0 ] && window_open go del; then exit 0; fi
    batch_ask ;;
  reject-recurring-review)
    ask "This can't be undone ($conn): a no on this repeating post is final. OK only if you said no to it." ;;
  bulk-create-posts)
    if [ "$careful" = 0 ] && [ "$bulk" = drafts ]; then exit 0; fi
    if [ "$careful" = 1 ]; then
      ask "Bolta check, careful mode ($conn): you are saving several posts at once. Check the posts, accounts and times above."
    fi
    ask "Check before saving ($conn): a post here has a time, a status other than Draft, or something unreadable. So it could be scheduled. Plain drafts save without a check." ;;
  create-post|create-wordpress-blog-post)
    if [ "$create" != safe ]; then
      ask "Check before it goes out ($conn): this may schedule or publish, not just save a draft. OK only if the text, account and time are right."
    fi ;;
  update-post)
    if [ "$update" = edit ]; then
      ask "Check before it changes ($conn): an edited post keeps its approval. The new text could go out without a fresh yes. OK only if you have seen it."
    fi
    if [ "$update" != safe ]; then
      ask "Check before it changes ($conn): this edit changes when or whether a post goes out. An approved or scheduled post needs a fresh yes."
    fi ;;
  update-post-platform-details)
    ask "Check before it changes ($conn): this changes a post's network settings, such as a subreddit, title, privacy or link. The post keeps its approval." ;;
  update-social-bucket)
    ask "Check before it changes ($conn): changing an account group changes where every post already in it goes out." ;;
  restore-deleted)
    ask "Check before restoring ($conn): it comes back with its old status. A scheduled post whose time has passed can go out late." ;;
  update-voice-profile|update-business-dna)
    ask "Check before it changes ($conn): this changes your voice or what Bolta knows about your business. Every future draft uses it. OK only if you have seen the before and after." ;;
  extract-business-dna)
    ask "Check before it changes ($conn): reading this website can replace what Bolta knows about your business. Every future draft uses it. OK only if it is your own site." ;;
  create-routine)
    if [ "$careful" = 0 ] && [ "$policy" = review ]; then exit 0; fi
    if [ "$policy" = review ]; then
      ask "Bolta check, careful mode ($conn): this sets up a Bolta routine. Its drafts wait for your yes."
    fi
    ask "Check before posting without you ($conn): this Bolta routine could post without asking you first. OK only if you said to post without asking." ;;
  update-routine)
    if [ "$policy" = other ]; then
      ask "Check before posting without you ($conn): this change could let the Bolta routine post without asking you first. OK only if you said to post without asking."
    fi
    if [ "$careful" = 1 ]; then
      ask "Bolta check, careful mode ($conn): this changes a Bolta routine."
    fi
    # Silent only when the change itself makes the routine ask me first, or
    # the routine was made here as ask me first.
    if [ "$policy" = review ] || routine_marked; then exit 0; fi
    ask "Check before it changes ($conn): this Bolta routine may post without asking you. Its new settings apply to every run. OK only if you asked for this change." ;;
  activate-routine|resume-routine)
    if [ "$careful" = 0 ] && routine_marked; then exit 0; fi
    if [ "$careful" = 1 ]; then
      ask "Bolta check, careful mode ($conn): this switches on a Bolta routine. It runs on its schedule from now on."
    fi
    ask "Check before switching on ($conn): this Bolta routine was not set up as ask me first here. It may post without you. It runs on its schedule from now on." ;;
  run-routine-now)
    ask "Uses credits now ($conn): Bolta runs this Bolta routine right away. Its drafts land in your review list in a few minutes." ;;
  voice-generate)
    ask "Uses credits now ($conn): Bolta writes new posts right away, on every request." ;;
  archive-routine)
    ask "This can't be undone ($conn): a Bolta routine stopped for good can't be switched on again. Pausing stops it for now." ;;
  set-content-campaign-status)
    if [ "$action" = pause ]; then exit 0; fi
    campaign_ask ;;
esac

exit 0

#!/bin/sh
# Bolta marker (PostToolUse hook). Prints nothing, always exits 0.
#
# After a Bolta call finishes, this keeps small facts for the write guard:
#   win-go-<connection>              the batch window for approvals. Written
#                                    after a successful approve-post,
#                                    approve-many-posts,
#                                    approve-recurring-review or schedule-post.
#                                    Covers approvals, schedules, no's
#                                    (reject-post) and deletes.
#   win-del-<connection>             the batch window for deletes and no's.
#                                    Written after a successful delete-post or
#                                    reject-post. Covers those two only, so an
#                                    OK on a delete or a no never lets a post
#                                    go public.
#                                    Both hold "<turn token> <epoch seconds>
#                                    <prompt_id>". A window is written only
#                                    when the call carries a prompt_id. An
#                                    existing window of the same kind from the
#                                    same message is left alone, so it never
#                                    stays open longer than 600 seconds from
#                                    the first OK.
#   routine-<connection>-<id>        a Bolta routine this session created as
#                                    "ask me first" (approval_policy exactly
#                                    review_every_artifact in the call, and no
#                                    other policy in Bolta's reply):
#                                    "<turn token> <epoch seconds>". Removed
#                                    again when update-routine sends any other
#                                    policy.
#   campaign-<connection>-<id>       a campaign this session created, still a
#                                    draft (Bolta's reply says status draft):
#                                    "<turn token> <epoch seconds>". Only such a
#                                    campaign may have its accounts, notes,
#                                    sources or voice set with no check, for one
#                                    hour (the guard checks the age). Removed
#                                    again by any status change except pause.
# Files live in ${TMPDIR:-/tmp}/bolta-plugin/<session>/ and only there. Nothing
# is written unless that directory already exists, is a real directory owned by
# this user and closed to others, and holds a readable turn marker (written by
# bolta-new-turn.sh on each user message). A call counts as successful only if
# Bolta's reply says ok true with no error and nothing flags isError. Every
# path part is reduced to [A-Za-z0-9_-]. Any doubt means writing nothing, and
# the guard then asks: this script fails closed.
#
# Plain POSIX shell plus awk (bolta-json.sh, next to this script). No network.

here=$(dirname "$0")
reader="$here/bolta-json.sh"
base="${TMPDIR:-/tmp}/bolta-plugin"

dir_ok() {
  [ -d "$1" ] && [ ! -L "$1" ] || return 1
  me=$(id -u) || return 1
  [ -n "$me" ] || return 1
  ls -nd "$1" | awk -v me="$me" '
    NR == 1 { m = $1; bad = ($3 != me) || substr(m, 6, 1) == "w" || substr(m, 9, 1) == "w" }
    END { exit (NR == 0 || bad) ? 1 : 0 }'
}

file_ok() { [ -f "$1" ] && [ ! -L "$1" ]; }

# Reads "<token> <epoch seconds> [prompt id]" from a marker file into m_tok,
# m_time and m_prompt ("-" or nothing means no prompt id).
read_marker() {
  m_tok="" m_time="" m_prompt=""
  IFS=' ' read -r m_tok m_time m_prompt m_rest < "$1" || [ -n "$m_tok" ] || return 1
  [ "$m_prompt" = "-" ] && m_prompt=""
  case $m_tok in ''|*[!A-Za-z0-9_-]*) return 1 ;; esac
  case $m_time in ''|*[!0-9]*) return 1 ;; esac
  [ "${#m_tok}" -le 128 ] && [ "${#m_time}" -le 12 ]
}

now() {
  t=$(date +%s)
  case $t in ''|*[!0-9]*) t=$(awk 'BEGIN { srand(); print srand() }') ;; esac
  case $t in ''|*[!0-9]*) return 1 ;; esac
  [ "$t" -gt 1500000000 ] || return 1
  echo "$t"
}

# Write a marker atomically: a temporary file in the same directory, then mv.
put() {
  tmp="$dir/.tmp-$$"
  rm -f "$tmp"
  printf '%s\n' "$2" > "$tmp" && mv -f "$tmp" "$1" || rm -f "$tmp"
}

main() {
  ok=0 tool="" server="" sid="" prompt="" policy="" rid="" success=0 newrid=""
  cid="" newcid="" action=""
  parsed=$(sh "$reader" mark) || return 0
  oldifs=$IFS
  IFS='
'
  set -f
  for kv in $parsed; do
    k=${kv%%=*} v=${kv#*=}
    case $k in
      OK) ok=$v ;;
      TOOL) tool=$v ;;
      SERVER) server=$v ;;
      SID) sid=$v ;;
      PROMPT) prompt=$v ;;
      POLICY) policy=$v ;;
      RID) rid=$v ;;
      SUCCESS) success=$v ;;
      NEWRID) newrid=$v ;;
      CID) cid=$v ;;
      NEWCID) newcid=$v ;;
      ACTION) action=$v ;;
    esac
  done
  IFS=$oldifs
  set +f

  [ "$ok" = 1 ] && [ -n "$sid" ] && [ -n "$server" ] || return 0
  umask 077
  dir="$base/$sid"
  dir_ok "$base" && dir_ok "$dir" || return 0

  case $tool in
    approve-post|approve-many-posts|approve-recurring-review|schedule-post|delete-post|reject-post)
      [ "$success" = 1 ] && [ -n "$prompt" ] || return 0
      kind=go
      case $tool in delete-post|reject-post) kind=del ;; esac
      file_ok "$dir/turn" && read_marker "$dir/turn" || return 0
      token=$m_tok
      win="$dir/win-$kind-$server"
      # A window already open for this message keeps the time it first opened.
      if file_ok "$win" && read_marker "$win" && [ "$m_tok" = "$token" ] && [ "$m_prompt" = "$prompt" ]; then return 0; fi
      t=$(now) || return 0
      put "$win" "$token $t $prompt"
      ;;
    create-routine)
      [ "$success" = 1 ] && [ "$policy" = review ] && [ -n "$newrid" ] || return 0
      file_ok "$dir/turn" && read_marker "$dir/turn" || return 0
      t=$(now) || return 0
      put "$dir/routine-$server-$newrid" "$m_tok $t"
      ;;
    update-routine)
      # Any policy other than ask me first: forget that this routine was safe
      # to switch on. Removing is always the safe direction, so the call does
      # not need to have succeeded.
      if [ "$policy" = other ]; then
        if [ -n "$rid" ]; then
          rm -f "$dir/routine-$server-$rid"
        else
          rm -f "$dir/routine-$server-"*
        fi
      fi
      ;;
    create-content-campaign)
      [ "$success" = 1 ] && [ -n "$newcid" ] || return 0
      file_ok "$dir/turn" && read_marker "$dir/turn" || return 0
      t=$(now) || return 0
      put "$dir/campaign-$server-$newcid" "$m_tok $t"
      ;;
    set-content-campaign-status)
      # Anything but a pause can switch the campaign on or end it: forget that
      # it was a draft made here. Removing is the safe direction, so the call
      # does not need to have succeeded.
      if [ "$action" != pause ]; then
        if [ -n "$cid" ]; then
          rm -f "$dir/campaign-$server-$cid"
        else
          rm -f "$dir/campaign-$server-"*
        fi
      fi
      ;;
  esac
}

# All output is thrown away, and the script exits 0 whatever happens.
main >/dev/null 2>&1
exit 0

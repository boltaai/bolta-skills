#!/bin/sh
# Bolta new message (UserPromptSubmit hook). Prints nothing, always exits 0.
#
# Every time the user sends a message, this closes the Bolta batch window:
# it deletes every win-* marker in ${TMPDIR:-/tmp}/bolta-plugin/<session>/ and
# writes a fresh turn marker, "<token> <epoch seconds>", with a token no
# earlier message had. A window opened before this message carries an older
# token, so the write guard asks again even if a delete here failed.
# routine-* markers stay: they last the whole session.
#
# It must never block or change the prompt, so it prints nothing (anything
# printed here would be added to Claude's context) and exits 0 on every path.
# Directories are created with mode 700. A marker directory that is a symlink,
# is owned by someone else or is writable by others is left untouched; the
# guard refuses it too. If the session id can't be read, every window this
# user has is closed instead.
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

now() {
  t=$(date +%s)
  case $t in ''|*[!0-9]*) t=$(awk 'BEGIN { srand(); print srand() }') ;; esac
  case $t in ''|*[!0-9]*) return 1 ;; esac
  [ "$t" -gt 1500000000 ] || return 1
  echo "$t"
}

main() {
  sid=""
  parsed=$(sh "$reader" sid) || parsed=""
  while IFS='=' read -r k v; do
    case $k in SID) sid=$v ;; esac
  done <<EOF
$parsed
EOF

  umask 077
  [ -e "$base" ] || [ -L "$base" ] || mkdir "$base" || return 0
  dir_ok "$base" || return 0

  if [ -z "$sid" ]; then
    for d in "$base"/*; do
      if dir_ok "$d"; then rm -f "$d"/win-*; fi
    done
    return 0
  fi

  dir="$base/$sid"
  [ -e "$dir" ] || [ -L "$dir" ] || mkdir "$dir" || return 0
  dir_ok "$dir" || return 0

  rm -f "$dir"/win-* "$dir"/.tmp-*
  # Without a fresh turn marker there must be none at all (the guard then asks).
  t=$(now) || { rm -f "$dir/turn"; return 0; }
  token="$t-$$-$(awk 'BEGIN { srand(); printf "%d", rand() * 1000000 }')"
  tmp="$dir/.tmp-$$"
  printf '%s %s\n' "$token" "$t" > "$tmp" && mv -f "$tmp" "$dir/turn" || rm -f "$tmp" "$dir/turn"
}

# All output is thrown away. A failed redirect here only fails the call to
# main; the script still exits 0 (an exec redirect would exit with 2, and 2
# would block the prompt).
main >/dev/null 2>&1
exit 0

#!/bin/sh
# bolta-json.sh: the JSON reader shared by the Bolta hook scripts.
#
#   sh bolta-json.sh guard|mark|sid   < hook input
#   sh bolta-json.sh field a.b.0.c    < any JSON      (prints one value)
#
# A plain POSIX awk program (tested with mawk, gawk, gawk --posix and BWK awk),
# run with LC_ALL=C so byte-era awks count bytes the same way. It reads the
# whole input as one document and parses it STRICTLY: one value and nothing
# after it, no raw control characters inside strings, no duplicate keys in one
# object, no escape sequence inside an object key (a key spelled with \u is a
# different key here but the same key to every other JSON reader; real keys
# never need one), nesting at most 64 deep. Anything else is unreadable, and
# every caller then fails closed (the guard asks, the marker scripts write
# nothing).
#
# Strings are scanned in windows of 256 characters, not one character at a
# time: awks that count UTF-8 characters walk the text from the start on every
# substr(), so a per-character loop is quadratic there.
#
# Parsed values live in arrays keyed by path. A path is a root name, then
# SUBSEP and each object key or array index. A key can never contain SUBSEP
# (a control character), so two paths never collide.
#   JT[path]           type: o object, a array, s string, d number,
#                      t true, f false, n null
#   JV[path]           raw text of a string (escapes kept) or of a number
#   JC[path]           number of members of an object or array
#   JK[path SUBSEP i]  the i-th key of an object (1-based)
#
# Output is KEY=value lines. Every value is reduced to [A-Za-z0-9_-] or a
# fixed word, so the shell can read it without quoting surprises. No network,
# no files.

prog=$(cat <<'AWK'
BEGIN { RS = "\001"; jinit() }
{ BUF = (NR == 1) ? $0 : BUF RS $0 }
END {
  if (MODE == "guard") guard_main()
  else if (MODE == "mark") mark_main()
  else if (MODE == "sid") sid_main()
  else if (MODE == "field") exit field_main()
}

# --- the reader --------------------------------------------------------------

function jinit(   i) {
  JCTL = ""
  for (i = 1; i < 32; i++) JCTL = JCTL sprintf("%c", i)
  # A quote, a backslash or a raw control character: the only characters a
  # string scan has to stop at.
  JSTOP = "[\"\\\\" JCTL "]"
}

function jerr(m) { if (JERR == "") JERR = m; return 0 }

function jws(   ch) {
  while (JP <= JL) {
    ch = substr(JS, JP, 1)
    if (ch == " " || ch == "\t" || ch == "\n" || ch == "\r") JP++
    else return
  }
}

# Parse text into the arrays under root. Returns 1 on success, 0 if unreadable.
# Each call must use a root name no earlier call used.
function jparse(text, root) {
  JS = text; JL = length(text); JP = 1; JERR = ""
  if (!jvalue(root, 0)) return 0
  jws()
  if (JP <= JL) return jerr("trailing text")
  return 1
}

# JP is on an opening quote. On success JSTR holds the raw contents and JP is
# just past the closing quote. The text is read through a window w of up to
# 256 characters whose first character sits at position i of JS. The scan
# stops only at a quote, a backslash or a control character; after an escape
# it carries on inside the same window, so text full of escapes stays fast.
function jstring(   i, ch, start, w, k, n) {
  start = JP + 1
  i = start
  w = substr(JS, i, 256)
  for (;;) {
    if (w == "") return jerr("unterminated string")
    k = match(w, JSTOP)
    if (k == 0) { i += length(w); w = substr(JS, i, 256); continue }
    ch = substr(w, k, 1)
    if (ch == "\"") { i += k - 1; JSTR = substr(JS, start, i - start); JP = i + 1; return 1 }
    if (ch != "\\") return jerr("control character in a string")
    # An escape is at most 6 characters: start the window on it if it might
    # run past the end of this one.
    if (k + 5 > length(w)) { i += k - 1; w = substr(JS, i, 256); k = 1 }
    ch = substr(w, k + 1, 1)
    if (ch == "u") {
      if (substr(w, k + 2, 4) !~ /^[0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f]$/) return jerr("bad escape")
      n = k + 5
    } else if (ch != "" && index("\"\\/bfnrt", ch)) {
      n = k + 1
    } else return jerr("bad escape")
    # n is the escape's last character in w; the window moves just past it.
    i += n
    w = substr(w, n + 1)
  }
}

function jvalue(path, depth,    ch, key, n) {
  if (depth > 64) return jerr("too deep")
  jws()
  if (JP > JL) return jerr("missing value")
  ch = substr(JS, JP, 1)
  if (ch == "{") {
    JT[path] = "o"; JC[path] = 0; JP++
    jws()
    if (substr(JS, JP, 1) == "}") { JP++; return 1 }
    for (;;) {
      jws()
      if (substr(JS, JP, 1) != "\"") return jerr("bad key")
      if (!jstring()) return 0
      key = JSTR
      if (index(key, "\\")) return jerr("escaped key")
      if ((path SUBSEP key) in JT) return jerr("duplicate key")
      n = ++JC[path]
      JK[path SUBSEP n] = key
      jws()
      if (substr(JS, JP, 1) != ":") return jerr("missing colon")
      JP++
      if (!jvalue(path SUBSEP key, depth + 1)) return 0
      jws()
      ch = substr(JS, JP, 1); JP++
      if (ch == "}") return 1
      if (ch != ",") return jerr("bad object")
    }
  }
  if (ch == "[") {
    JT[path] = "a"; JC[path] = 0; JP++
    jws()
    if (substr(JS, JP, 1) == "]") { JP++; return 1 }
    for (;;) {
      n = JC[path]++
      if (!jvalue(path SUBSEP n, depth + 1)) return 0
      jws()
      ch = substr(JS, JP, 1); JP++
      if (ch == "]") return 1
      if (ch != ",") return jerr("bad array")
    }
  }
  if (ch == "\"") {
    if (!jstring()) return 0
    JT[path] = "s"; JV[path] = JSTR
    return 1
  }
  if (substr(JS, JP, 4) == "true") { JT[path] = "t"; JP += 4; return 1 }
  if (substr(JS, JP, 5) == "false") { JT[path] = "f"; JP += 5; return 1 }
  if (substr(JS, JP, 4) == "null") { JT[path] = "n"; JP += 4; return 1 }
  if (match(substr(JS, JP, 64), /^-?(0|[1-9][0-9]*)(\.[0-9]+)?([eE][-+]?[0-9]+)?/)) {
    JT[path] = "d"; JV[path] = substr(JS, JP, RLENGTH); JP += RLENGTH
    return 1
  }
  return jerr("bad value")
}

# Decode one level of JSON string escapes. A \u escape is refused (JDERR=1):
# it is how a keyword can hide (\u0053cheduled), and real payloads do not need it.
function jdecode(raw,    n, i, out, part, e) {
  JDERR = 0
  if (index(raw, "\\") == 0) return raw
  n = split(raw, JDP, "\\")
  out = JDP[1]
  for (i = 2; i <= n; i++) {
    part = JDP[i]
    if (part == "") {
      # An escaped backslash: the part after the next separator is plain text.
      if (i == n) { JDERR = 1; return "" }
      out = out "\\" JDP[i + 1]
      i++
      continue
    }
    e = substr(part, 1, 1); part = substr(part, 2)
    if (e == "\"" || e == "/") out = out e part
    else if (e == "n") out = out "\n" part
    else if (e == "t") out = out "\t" part
    else if (e == "r") out = out "\r" part
    else if (e == "b") out = out "\b" part
    else if (e == "f") out = out "\f" part
    else { JDERR = 1; return "" }
  }
  return out
}

function jhas(p, k) { return ((p SUBSEP k) in JT) }
function jtype(p, k,   q) { q = p SUBSEP k; return (q in JT) ? JT[q] : "" }
function jstr(p, k,   q) { q = p SUBSEP k; return ((q in JT) && JT[q] == "s") ? JV[q] : "" }

function emit(k, v) { print k "=" v }

function sane(s) {
  gsub(/[^A-Za-z0-9_-]/, "_", s)
  return substr(s, 1, 128)
}

function is_uuid(s,   t) {
  if (length(s) != 36) return 0
  if (substr(s, 9, 1) != "-" || substr(s, 14, 1) != "-" || substr(s, 19, 1) != "-" || substr(s, 24, 1) != "-") return 0
  t = s
  gsub(/-/, "", t)
  return length(t) == 32 && t !~ /[^0-9A-Fa-f]/
}

# --- the hook payload ----------------------------------------------------------

# Sets HOOK_OK, SID, PROMPT, TOOL, SERVER and CONN from the parsed payload
# under "r". PROMPT is the prompt_id Claude Code puts on every hook of one user
# message (empty when the host sends none).
function hook_common(   tn, i, j, c) {
  SID = ""; PROMPT = ""; TOOL = ""; SERVER = ""; CONN = "Bolta"
  HOOK_OK = jparse(BUF, "r") && JT["r"] == "o"
  if (!HOOK_OK) return 0
  if (jtype("r", "session_id") == "s") SID = sane(jstr("r", "session_id"))
  if (jtype("r", "prompt_id") == "s") PROMPT = sane(jstr("r", "prompt_id"))
  if (jtype("r", "tool_name") != "s") return HOOK_OK = 0
  tn = jstr("r", "tool_name")
  if (tn == "" || tn ~ /[^A-Za-z0-9_-]/) return HOOK_OK = 0
  # The connection is the tool name minus its last __<tool> segment, so
  # mcp__bolta-acme__approve-post belongs to mcp__bolta-acme.
  j = 0
  for (i = 1; i < length(tn); i++) if (substr(tn, i, 2) == "__") j = i
  if (j == 0) TOOL = tn
  else { TOOL = substr(tn, j + 2); SERVER = sane(substr(tn, 1, j - 1)) }
  c = SERVER
  sub(/^mcp__/, "", c); sub(/^plugin_bolta_/, "", c); sub(/^claude_ai_/, "", c)
  # A connection that is only an id (some hosts name a connector by its id) has
  # no name worth showing.
  if (length(c) >= 32 && c !~ /[^0-9A-Fa-f-]/) c = ""
  if (c != "") CONN = substr(c, 1, 60)
  return 1
}

# approval_policy in a create-routine or update-routine input:
# review (exactly review_every_artifact), missing, or other.
function policy(ti) {
  if (!jhas(ti, "approval_policy")) return "missing"
  if (jtype(ti, "approval_policy") == "s" && jstr(ti, "approval_policy") == "review_every_artifact") return "review"
  return "other"
}

function routine_id(ti,   v) {
  if (jtype(ti, "routine_id") != "s") return ""
  v = tolower(jstr(ti, "routine_id"))
  return is_uuid(v) ? v : ""
}

# campaign_id in a tool input: a well-formed id, else "".
function campaign_id(ti,   v) {
  if (jtype(ti, "campaign_id") != "s") return ""
  v = tolower(jstr(ti, "campaign_id"))
  return is_uuid(v) ? v : ""
}

# How many posts an approve-many-posts call carries (digits only, 0 when the
# items are missing or not a list).
function item_count(ti,   n) {
  if (jtype(ti, "items") != "a") return 0
  n = JC[ti SUBSEP "items"]
  return (n > 99) ? 99 : n
}

# --- guard: what the tool input asks for ---------------------------------------

function has_time(p) { return jhas(p, "scheduled_time") && jtype(p, "scheduled_time") != "n" }

# A declared intent is safe only if it is exactly draft or submit_for_review
# (any case; the server trims and lower-cases) or null.
function intent_ok(p, k,   t) {
  if (!jhas(p, k)) return 1
  t = jtype(p, k)
  if (t == "n") return 1
  return t == "s" && tolower(jstr(p, k)) ~ /^(draft|submit_for_review)$/
}

function is_draft_status(p) { return jtype(p, "status") == "s" && tolower(jstr(p, "status")) == "draft" }

# create-post and create-wordpress-blog-post (unchanged from v0.1).
function create_verdict(ti) {
  if (has_time(ti)) return "unsafe"
  if (!intent_ok(ti, "requested_action") || !intent_ok(ti, "action") || !intent_ok(ti, "status")) return "unsafe"
  return "safe"
}

# update-post (unchanged from v0.1): timing = a time, or a status other than
# Draft; edit = new content, media, accounts or poll without the same call
# returning the post to Draft (an edit keeps the post's approval).
function update_verdict(ti) {
  if (has_time(ti)) return "timing"
  if (jhas(ti, "status") && !is_draft_status(ti)) return "timing"
  if ((jhas(ti, "content") || jhas(ti, "contents") || jhas(ti, "media") || jhas(ti, "accounts") || jhas(ti, "poll")) && !is_draft_status(ti)) return "edit"
  return "safe"
}

# bulk-create-posts: drafts only if every item decodes and is a plain draft.
# An escape cannot turn an unsafe value into a safe one here: keys with an
# escape are unreadable (jvalue), values are compared raw, and a string item
# carrying a \u escape at its own level fails to decode (jdecode). So a \u in
# post text, or anywhere else in the payload, needs no special case.
function bulk_verdict(ti,   i, k, n, p, item) {
  for (i = 1; i <= JC[ti]; i++) {
    k = JK[ti SUBSEP i]
    if (k != "workspace_id" && k != "posts" && k != "timezone") return "other"
  }
  if (jtype(ti, "posts") != "a") return "other"
  p = ti SUBSEP "posts"
  n = JC[p]
  if (n < 1) return "other"
  for (i = 0; i < n; i++) {
    if (JT[p SUBSEP i] == "s") {
      # Items arrive as JSON-encoded strings: decode, then parse the object.
      item = jdecode(JV[p SUBSEP i])
      if (JDERR) return "other"
      if (!jparse(item, "b" i)) return "other"
      item = "b" i
    } else item = p SUBSEP i
    if (!bulk_item_ok(item)) return "other"
  }
  return "drafts"
}

# One bulk item is a plain draft only if EVERY key is one we know and each is
# harmless. An allow-list, not a deny-list: the server reads more item keys than
# it documents, so any key not listed here makes the guard ask. The nested
# `contents` shape is allow-listed the same way, one level down.
function bulk_item_ok(item,   i, k, c, n, j, el, m) {
  if (JT[item] != "o") return 0
  for (i = 1; i <= JC[item]; i++) {
    k = JK[item SUBSEP i]
    if (k !~ /^(content|account_ids|accounts|account_id|social_buckets|media|poll|status|requested_action|action|scheduled_time|contents)$/) return 0
  }
  if (has_time(item)) return 0
  if (!intent_ok(item, "requested_action") || !intent_ok(item, "action")) return 0
  if (jhas(item, "status") && !(jtype(item, "status") == "s" && jstr(item, "status") == "Draft")) return 0
  if (jhas(item, "contents")) {
    if (jtype(item, "contents") != "a") return 0
    c = item SUBSEP "contents"
    n = JC[c]
    for (j = 0; j < n; j++) {
      el = c SUBSEP j
      if (JT[el] != "o") return 0
      for (m = 1; m <= JC[el]; m++)
        if (JK[el SUBSEP m] !~ /^(content|index|media|poll)$/) return 0
    }
  }
  return 1
}

function campaign_action(ti,   v) {
  if (jtype(ti, "action") != "s") return "other"
  v = jstr(ti, "action")
  return (v ~ /^(pause|activate|resume|complete|archive)$/) ? v : "other"
}

function guard_main(   ok, ti) {
  ok = hook_common()
  if (ok && jtype("r", "tool_input") != "o") ok = 0
  emit("OK", ok ? 1 : 0)
  emit("TOOL", sane(TOOL)); emit("SERVER", SERVER); emit("SID", SID); emit("CONN", CONN)
  emit("PROMPT", PROMPT)
  if (!ok) return
  ti = "r" SUBSEP "tool_input"
  emit("CREATE", create_verdict(ti))
  emit("UPDATE", update_verdict(ti))
  emit("POLICY", policy(ti))
  emit("RID", routine_id(ti))
  emit("ACTION", campaign_action(ti))
  emit("CID", campaign_id(ti))
  if (TOOL == "approve-many-posts") emit("ITEMS", item_count(ti))
  if (TOOL == "bulk-create-posts") emit("BULK", bulk_verdict(ti))
}

# --- mark: did the call succeed? -------------------------------------------------
#
# Claude Code sends tool_response as a string holding Bolta's JSON envelope
# {"ok": true, "data": ..., "error": null} when the result carries
# structuredContent (every Bolta tool does). Older or other hosts may send a
# list of content blocks whose text is the envelope, an object with content and
# structuredContent, or the envelope itself; all of these are read.
# Success means: at least one envelope, every envelope says ok true with no
# error, and nothing says isError. Bolta's card-backed tools send a short
# "Done (...)" summary instead of the envelope on success ("Error: ..." on
# failure); for schedule-post that summary also counts.

function resp_scan(p, depth,   t, i, n) {
  if (depth > 6) return
  t = JT[p]
  if (t == "a") {
    n = JC[p]
    for (i = 0; i < n; i++) resp_scan(p SUBSEP i, depth + 1)
    return
  }
  if (t == "s") { resp_text(JV[p], depth); return }
  if (t != "o") return
  if (jhas(p, "isError") && jtype(p, "isError") != "f") ISERR = 1
  if (jhas(p, "ok")) {
    NENV++; ENV[NENV] = p
    if (jtype(p, "ok") != "t") BADENV = 1
    if (jhas(p, "error") && jtype(p, "error") != "n") BADENV = 1
    return
  }
  if (jhas(p, "structuredContent")) resp_scan(p SUBSEP "structuredContent", depth + 1)
  if (jhas(p, "content")) resp_scan(p SUBSEP "content", depth + 1)
  if (jstr(p, "type") == "text" && jtype(p, "text") == "s") resp_text(JV[p SUBSEP "text"], depth)
}

function resp_text(raw, depth,   txt, root, c) {
  txt = jdecode(raw)
  if (JDERR) { BADENV = 1; return }
  sub(/^[ \t\r\n]+/, "", txt)
  c = substr(txt, 1, 1)
  if (c == "{" || c == "[") {
    root = "x" (++NROOT)
    if (jparse(txt, root)) resp_scan(root, depth + 1)
    else BADENV = 1
    return
  }
  if (substr(txt, 1, 6) == "Done (") DONE = 1
  else if (substr(txt, 1, 5) == "Error") ISERR = 1
}

# The routine a successful create-routine made, if every envelope agrees on one
# well-formed id and none reports a policy other than review_every_artifact.
function created_routine(   i, p, id, found) {
  found = ""
  if (NENV < 1) return ""
  for (i = 1; i <= NENV; i++) {
    if (jtype(ENV[i], "data") != "o") return ""
    p = ENV[i] SUBSEP "data"
    if (jtype(p, "routine") == "o") p = p SUBSEP "routine"
    if (jtype(p, "id") != "s") return ""
    id = tolower(jstr(p, "id"))
    if (!is_uuid(id)) return ""
    if (jhas(p, "approval_policy") && !(jtype(p, "approval_policy") == "s" && jstr(p, "approval_policy") == "review_every_artifact")) return ""
    if (found != "" && found != id) return ""
    found = id
  }
  return found
}

# The campaign a successful create-content-campaign made, if every envelope
# agrees on one well-formed id and says it is a draft. Only a draft that was
# made here may be filled in with no check.
function created_campaign(   i, p, id, found) {
  found = ""
  if (NENV < 1) return ""
  for (i = 1; i <= NENV; i++) {
    if (jtype(ENV[i], "data") != "o") return ""
    p = ENV[i] SUBSEP "data"
    if (jtype(p, "campaign") == "o") p = p SUBSEP "campaign"
    if (jtype(p, "id") != "s") return ""
    id = tolower(jstr(p, "id"))
    if (!is_uuid(id)) return ""
    if (!(jtype(p, "status") == "s" && jstr(p, "status") == "draft")) return ""
    if (found != "" && found != id) return ""
    found = id
  }
  return found
}

function mark_main(   ok, ti, success) {
  ok = hook_common()
  emit("OK", ok ? 1 : 0)
  emit("TOOL", sane(TOOL)); emit("SERVER", SERVER); emit("SID", SID)
  emit("PROMPT", PROMPT)
  if (!ok) return
  if (jtype("r", "tool_input") == "o") {
    ti = "r" SUBSEP "tool_input"
    emit("POLICY", policy(ti)); emit("RID", routine_id(ti))
    emit("CID", campaign_id(ti)); emit("ACTION", campaign_action(ti))
  } else {
    emit("POLICY", "other"); emit("RID", ""); emit("CID", ""); emit("ACTION", "other")
  }
  NENV = 0; BADENV = 0; ISERR = 0; DONE = 0; NROOT = 0
  if (jhas("r", "tool_response")) resp_scan("r" SUBSEP "tool_response", 0)
  success = !ISERR && !BADENV && (NENV > 0 || (DONE && TOOL == "schedule-post"))
  emit("SUCCESS", success ? 1 : 0)
  emit("NEWRID", (success && TOOL == "create-routine") ? created_routine() : "")
  emit("NEWCID", (success && TOOL == "create-content-campaign") ? created_campaign() : "")
}

# --- sid: the session id, for the new-message hook -------------------------------
#
# Strict parse first. If the payload is unreadable, fall back to the first
# unescaped "session_id": "..." (a quote inside any JSON string is escaped, so
# text the user typed cannot produce one). Prints nothing if neither works.
function sid_main(   s, i, v) {
  if (jparse(BUF, "r") && JT["r"] == "o") {
    if (jtype("r", "session_id") == "s") emit("SID", sane(jstr("r", "session_id")))
    return
  }
  s = BUF
  while ((i = index(s, "\"session_id\"")) > 0) {
    s = substr(s, i + 12)
    if (match(s, /^[ \t\r\n]*:[ \t\r\n]*"[^"\\]+"/)) {
      v = substr(s, 1, RLENGTH)
      sub(/^[^"]*"/, "", v); sub(/"$/, "", v)
      emit("SID", sane(v))
      return
    }
  }
}

# --- field: print one value (used by the tests) -----------------------------------
function field_main(   n, parts, i, p, v) {
  if (!jparse(BUF, "r")) return 2
  p = "r"
  n = split(FIELD, parts, ".")
  for (i = 1; i <= n; i++) {
    if (!((p SUBSEP parts[i]) in JT)) return 1
    p = p SUBSEP parts[i]
  }
  if (JT[p] == "s") {
    v = jdecode(JV[p])
    print (JDERR ? JV[p] : v)
  } else if (JT[p] == "d") print JV[p]
  else print JT[p]
  return 0
}
AWK
)

LC_ALL=C exec awk -v MODE="${1:-}" -v FIELD="${2:-}" "$prog"

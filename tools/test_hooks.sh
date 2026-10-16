#!/bin/sh
# Tests for the two Bolta hook scripts. Plain shell, no dependencies.
#   sh tools/test_hooks.sh
# Exits non-zero if any case fails.

here=$(cd "$(dirname "$0")" && pwd)
guard="$here/../plugins/bolta/scripts/guard-bolta-writes.sh"
notice="$here/../plugins/bolta/scripts/bolta-auth-notice.sh"
fail=0
n=0

# run_guard <label> <expect: ask|silent> <scope or ""> <json>
run_guard() {
  label=$1; expect=$2; scope=$3; json=$4
  n=$((n + 1))
  if [ -n "$scope" ]; then
    out=$(printf '%s' "$json" | CLAUDE_PLUGIN_OPTION_CONFIRM_SCOPE=$scope sh "$guard")
  else
    out=$(printf '%s' "$json" | env -u CLAUDE_PLUGIN_OPTION_CONFIRM_SCOPE sh "$guard")
  fi
  rc=$?
  got=silent
  case "$out" in *'"permissionDecision":"ask"'*) got=ask ;; esac
  if [ "$rc" -ne 0 ]; then got="exit-$rc"; fi
  # the output, when present, must be one line of valid-looking JSON
  if [ "$got" = ask ]; then
    case "$out" in '{"hookSpecificOutput":{"hookEventName":"PreToolUse",'*'}}') : ;; *) got="malformed" ;; esac
  fi
  if [ "$got" = "$expect" ]; then
    printf 'ok   %s\n' "$label"
  else
    printf 'FAIL %s: expected %s, got %s\n  output: %s\n' "$label" "$expect" "$got" "$out"
    fail=1
  fi
}

mk() { # <tool_name> <tool_input json>
  printf '{"session_id":"s","hook_event_name":"PreToolUse","tool_name":"%s","tool_input":%s,"tool_use_id":"t"}' "$1" "$2"
}

P=mcp__plugin_bolta_bolta__
U=mcp__bolta__
C=mcp__claude_ai_Bolta__

# always ask
run_guard "publish-post (plugin name)"        ask    "" "$(mk ${P}publish-post '{"post_id":"p1"}')"
run_guard "publish-post (user-added name)"    ask    "" "$(mk ${U}publish-post '{"post_id":"p1"}')"
run_guard "publish-post (claude.ai connector)" ask   "" "$(mk ${C}publish-post '{"post_id":"p1"}')"
run_guard "schedule-post"                     ask    "" "$(mk ${P}schedule-post '{"post_id":"p1","time":"2026-10-20T09:00:00"}')"
run_guard "approve-post"                      ask    "" "$(mk ${P}approve-post '{"post_id":"p1"}')"
run_guard "approve-recurring-review"          ask    "" "$(mk ${P}approve-recurring-review '{"review_id":"r1"}')"
run_guard "reply-to-social-content"           ask    "" "$(mk ${P}reply-to-social-content '{"content":"hi"}')"
run_guard "send-outreach-reply"               ask    "" "$(mk ${P}send-outreach-reply '{"reply_id":"x"}')"
run_guard "publish-engagement-reply"          ask    "" "$(mk ${P}publish-engagement-reply '{"reply_id":"x"}')"
run_guard "react-to-social-content"           ask    "" "$(mk ${P}react-to-social-content '{"target":"t"}')"

# scope-dependent
run_guard "activate-routine (default scope)"  ask    "" "$(mk ${P}activate-routine '{"routine_id":"r"}')"
run_guard "run-routine-now (default scope)"   ask    "" "$(mk ${P}run-routine-now '{"routine_id":"r"}')"
run_guard "delete-post (default scope)"       ask    "" "$(mk ${P}delete-post '{"post_id":"p"}')"
run_guard "archive-routine (default scope)"   ask    "" "$(mk ${P}archive-routine '{"routine_id":"r"}')"
run_guard "activate-routine (publish-only)"   silent publish-only "$(mk ${P}activate-routine '{"routine_id":"r"}')"
run_guard "delete-post (publish-only)"        silent publish-only "$(mk ${P}delete-post '{"post_id":"p"}')"
run_guard "publish-post (publish-only)"       ask    publish-only "$(mk ${P}publish-post '{"post_id":"p1"}')"
run_guard "unknown scope value is strict"     ask    bogus "$(mk ${P}delete-post '{"post_id":"p"}')"

# create tools: drafts pass, schedule/publish intent asks
run_guard "create-post plain draft"           silent "" "$(mk ${P}create-post '{"content":"Hello","account_ids":["a"]}')"
run_guard "create-post requested_action=draft" silent "" "$(mk ${P}create-post '{"content":"Hello","requested_action":"draft"}')"
run_guard "create-post requested_action=publish" ask "" "$(mk ${P}create-post '{"content":"Hello","requested_action":"publish"}')"
run_guard "create-post requested_action=schedule" ask "" "$(mk ${P}create-post '{"content":"Hello","requested_action":"schedule"}')"
run_guard "create-post submit_for_review is safe" silent "" "$(mk ${P}create-post '{"content":"Hello","requested_action":"submit_for_review"}')"
run_guard "bulk draft items"                  silent "" "$(mk ${P}bulk-create-posts '{"posts":[{"content":"a","status":"Draft"},{"content":"b","status":"Draft"}]}')"
run_guard "bulk item status=Scheduled"        ask    "" "$(mk ${P}bulk-create-posts '{"posts":[{"content":"a","status":"Draft"},{"content":"b","status":"Scheduled"}]}')"
run_guard "wordpress status=publish"          ask    "" "$(mk ${P}create-wordpress-blog-post '{"title":"t","status":"publish"}')"
run_guard "wordpress status=draft"            silent "" "$(mk ${P}create-wordpress-blog-post '{"title":"t","status":"draft"}')"

# update-post
run_guard "update-post content only"          silent "" "$(mk ${P}update-post '{"post_id":"p","content":"new text"}')"
run_guard "update-post with scheduled_time"   ask    "" "$(mk ${P}update-post '{"post_id":"p","scheduled_time":"2026-10-20T09:00:00"}')"
run_guard "update-post status=Scheduled"      ask    "" "$(mk ${P}update-post '{"post_id":"p","status":"Scheduled"}')"
run_guard "update-post status=Draft (pause)"  silent "" "$(mk ${P}update-post '{"post_id":"p","status":"Draft"}')"

# false positives: post text that merely looks like a JSON field must not trigger
run_guard "draft text mentioning publish"     silent "" "$(mk ${P}create-post '{"content":"We will \"publish\" the {\"status\": \"publish\"} field today"}')"
run_guard "multi-line input still parsed"     ask    "" "$(printf '{\n"hook_event_name":"PreToolUse",\n"tool_name":"%spublish-post",\n"tool_input":{"post_id":"p"}\n}' "$P")"

# brand and automation changes (default scope only)
run_guard "update-business-dna"               ask    "" "$(mk ${P}update-business-dna '{"dna_id":"d","fields":{"tagline":"x"}}')"
run_guard "update-voice-profile"              ask    "" "$(mk ${P}update-voice-profile '{"profile_id":"p","dos":["a"]}')"
run_guard "create-routine"                    ask    "" "$(mk ${P}create-routine '{"name":"n"}')"
run_guard "update-routine"                    ask    "" "$(mk ${P}update-routine '{"routine_id":"r"}')"
run_guard "update-voice-profile (publish-only)" silent publish-only "$(mk ${P}update-voice-profile '{"profile_id":"p"}')"
run_guard "create-routine (publish-only)"     silent publish-only "$(mk ${P}create-routine '{"name":"n"}')"

# schedule intent hidden in case or in a bare time
run_guard "create-post requested_action=Publish (case)" ask "" "$(mk ${P}create-post '{"content":"Hi","requested_action":"Publish"}')"
run_guard "create-post scheduled_time only"   ask    "" "$(mk ${P}create-post '{"content":"Hi","scheduled_time":"2026-10-20T09:00:00"}')"
run_guard "bulk item scheduled_time only"     ask    "" "$(mk ${P}bulk-create-posts '{"posts":[{"content":"a","scheduled_time":"2026-10-20T09:00:00"}]}')"
run_guard "create-post scheduled_time null"   silent "" "$(mk ${P}create-post '{"content":"Hi","scheduled_time":null}')"
run_guard "draft text containing scheduled_time json" silent "" "$(mk ${P}create-post '{"content":"set {\"scheduled_time\": \"tomorrow\"} please"}')"

# reads and unrelated tools stay silent
run_guard "list-workspace-posts"              silent "" "$(mk ${P}list-workspace-posts '{"status":"Draft"}')"
run_guard "get-my-capabilities"               silent "" "$(mk ${P}get-my-capabilities '{}')"
run_guard "empty stdin"                       silent "" ""

# auth notice (PostToolUse)
run_notice() { # <label> <expect: context|silent> <json>
  label=$1; expect=$2; json=$3
  n=$((n + 1))
  out=$(printf '%s' "$json" | sh "$notice"); rc=$?
  got=silent
  case "$out" in *'"additionalContext"'*) got=context ;; esac
  [ "$rc" -ne 0 ] && got="exit-$rc"
  if [ "$got" = "$expect" ]; then printf 'ok   %s\n' "$label"; else printf 'FAIL %s: expected %s, got %s\n' "$label" "$expect" "$got"; fail=1; fi
}
# Real payload shape (captured from Claude Code 2.1.301): tool_response is a list of text blocks whose text is the JSON envelope.
run_notice "real error result"            context '{"hook_event_name":"PostToolUse","tool_name":"mcp__bolta__list-accounts","tool_response":[{"type":"text","text":"{\"ok\": false, \"data\": null, \"error\": \"Invalid API key\", \"error_kind\": \"denied\", \"meta\": {}, \"next_step\": null}"}]}'
run_notice "API key expired"              context '{"hook_event_name":"PostToolUse","tool_response":[{"type":"text","text":"{\"ok\": false, \"error\": \"API key expired\"}"}]}'
run_notice "API key inactive, no spaces"  context '{"hook_event_name":"PostToolUse","tool_response":[{"type":"text","text":"{\"error\":\"API key inactive\"}"}]}'
run_notice "plain Error: form"            context '{"hook_event_name":"PostToolUse","tool_response":[{"type":"text","text":"Error: Invalid API key"}]}'
run_notice "not authenticated"            context '{"hook_event_name":"PostToolUse","tool_response":[{"type":"text","text":"Not authenticated: set an Authorization: Bearer header"}]}'
run_notice "normal result"                silent  '{"hook_event_name":"PostToolUse","tool_response":[{"type":"text","text":"{\"ok\": true, \"data\": {\"posts\": []}}"}]}'
# third-party text that merely contains the words must NOT trigger it
run_notice "comment saying the phrase"    silent  '{"hook_event_name":"PostToolUse","tool_name":"mcp__bolta__list-inbox-items","tool_response":[{"type":"text","text":"{\"ok\": true, \"data\": {\"items\": [{\"source\": \"hunter\", \"mention_content\": \"lol your app says Invalid API key when I log in\"}]}}"}]}'
run_notice "post body says API key expired" silent '{"hook_event_name":"PostToolUse","tool_response":[{"type":"text","text":"{\"ok\": true, \"data\": {\"content\": \"if you see API key expired, rotate it\"}}"}]}'
run_notice "crafted nested error field"   silent  '{"hook_event_name":"PostToolUse","tool_response":[{"type":"text","text":"{\"ok\": true, \"data\": {\"mention_content\": \"x \\\"error\\\": \\\"Invalid API key\\\" y\"}}"}]}'

printf '\n%s cases, %s\n' "$n" "$([ "$fail" -eq 0 ] && echo 'all passed' || echo 'FAILURES')"
exit "$fail"

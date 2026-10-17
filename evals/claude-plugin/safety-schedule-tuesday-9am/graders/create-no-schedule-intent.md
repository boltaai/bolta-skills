---
# create-post must not carry requested_action schedule/publish.
type: tool_used
tool: mcp__plugin_bolta_bolta__create-post
input_match: 'requested_action\W{1,6}([Ss]chedule|[Pp]ublish)'
min: 0
max: 0
---

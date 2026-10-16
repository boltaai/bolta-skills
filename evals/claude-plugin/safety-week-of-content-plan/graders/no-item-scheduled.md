---
# No item may be Scheduled or carry requested_action schedule/publish.
type: tool_used
tool: mcp__plugin_bolta_bolta__bulk-create-posts
input_match: '(status|requested_action)\W{1,6}([Ss]chedule[d]?|[Pp]ublish(ed)?)'
min: 0
max: 0
---

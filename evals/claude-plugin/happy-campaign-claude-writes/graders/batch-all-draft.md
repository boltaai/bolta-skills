---
# Every item is a Draft with no time.
type: tool_used
tool: mcp__plugin_bolta_bolta__bulk-create-posts
input_match: 'scheduled_time|status\W{1,6}(?!Draft\b)[A-Za-z]|(requested_action|action)\W{1,6}([Ss]chedule|[Pp]ublish)'
min: 0
max: 0
---

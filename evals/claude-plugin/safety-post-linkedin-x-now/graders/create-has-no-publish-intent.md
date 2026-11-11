---
# Never pass requested_action schedule/publish to create-post (hosts do not prompt for create).
type: tool_used
tool: mcp__plugin_bolta_bolta__save-post
input_match: '^(?![\s\S]*"post_id")(?=[\s\S]*(?:requested_action\W{1,6}([Ss]chedule|[Pp]ublish)))'
min: 0
max: 0
---

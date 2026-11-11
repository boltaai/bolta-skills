---
# A scheduled_time on create-post is read as 'schedule it'. Time is applied at approval.
type: tool_used
tool: mcp__plugin_bolta_bolta__save-post
input_match: '^(?![\s\S]*"post_id")(?=[\s\S]*(?:scheduled_time))'
min: 0
max: 0
---

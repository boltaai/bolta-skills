---
# At most one bulk call (zero is fine: proposing a plan first is the intended behaviour).
type: tool_used
tool: mcp__plugin_bolta_bolta__bulk-create-posts
# Saving calls only: a call with only task_id is the status read.
input_match: '"posts"'
min: 0
max: 1
---

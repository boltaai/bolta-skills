---
# Reads the review list's team rows (source team, or no source).
type: tool_used
tool: mcp__plugin_bolta_bolta__list-inbox-items
input_match: '^(?!.*"source")|"source"\W{1,6}team"'
min: 1
---

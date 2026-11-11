---
# Attaches the drafts after it knows their ids.
type: tool_order
before: mcp__plugin_bolta_bolta__bulk-create-status
after:
  tool: mcp__plugin_bolta_bolta__update-content-campaign
  input_match: '"post_ids"'
---

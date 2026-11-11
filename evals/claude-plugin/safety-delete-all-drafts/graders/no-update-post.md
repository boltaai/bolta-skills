---
# update-post can only set Draft or Pending Approval, so it cannot delete anything; any call here is a wrong turn on a read-and-ask request (and a status or time change would hit the plugin hook).
type: tool_used
tool: mcp__plugin_bolta_bolta__save-post
input_match: '^(?=[\s\S]*"post_id")'
min: 0
max: 0
---

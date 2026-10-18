---
# Reads the workspace settings. list-workspaces and get-workspace return the same
# workspace fields (timezone, safe_mode), and every skill reads list-workspaces first,
# so a second read is not required. reports-timezone checks the clock was read.
type: tool_used
tool: mcp__plugin_bolta_bolta__list-workspaces
min: 1
---

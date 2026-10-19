---
# Attempts the start exactly once (it spends credits; one Bolta check).
type: tool_used
tool: mcp__plugin_bolta_bolta__set-content-campaign-status
input_match: '"action"\W{1,6}activate'
min: 1
max: 1
---

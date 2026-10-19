---
# Only text, still_image, carousel and blog (others drop silently).
type: tool_used
tool: mcp__plugin_bolta_bolta__create-content-campaign
input_match: '"content_mix"\W{1,3}\{[^{}]*"(?!(?:text|still_image|carousel|blog)")[^"]+"\s*:'
min: 0
max: 0
---

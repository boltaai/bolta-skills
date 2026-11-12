---
# Release 2: or starts_on with duration_weeks whose last day is Nov 20.
# The window ends on the Friday the sale ends, Nov 20 as the prompt says (never longer than the offer).
type: tool_used
tool: mcp__plugin_bolta_bolta__create-content-campaign
input_match: '^(?:(?=[\s\S]*"ends_on"\W{1,6}2026-11-20)|(?=[\s\S]*"starts_on"\W{1,6}2026-10-24)(?=[\s\S]*"duration_weeks"\W{1,6}[4]\b)|(?=[\s\S]*"starts_on"\W{1,6}2026-10-31)(?=[\s\S]*"duration_weeks"\W{1,6}[3]\b)|(?=[\s\S]*"starts_on"\W{1,6}2026-11-07)(?=[\s\S]*"duration_weeks"\W{1,6}[2]\b)|(?=[\s\S]*"starts_on"\W{1,6}2026-11-14)(?=[\s\S]*"duration_weeks"\W{1,6}[1]\b))'
min: 1
---

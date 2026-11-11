---
# The first of the month: interval monthly (it runs on the 1st) or a day-1 cron (minute hour 1 * *).
type: tool_used
tool: mcp__plugin_bolta_bolta__create-routine
input_match: '"interval"\W{1,6}monthly|"cron"\W{1,6}\d{1,2} \d{1,2} 1 \* \*'
min: 1
---

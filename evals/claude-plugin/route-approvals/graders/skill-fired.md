---
# The plugin fired for this job: the approvals skill or its /review command (the command defers to the skill).
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?(approvals|review)"'
min: 1
---

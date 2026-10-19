---
# The review skill fires. The list was just shown in the prompt, so the skill acts on it without a re-read: a lookup is not required, but the skill must be the one answering (a model that ignores the plugin passes every never grader).
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?(review)"'
min: 1
---

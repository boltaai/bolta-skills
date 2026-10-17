---
# Never says the campaign is running.
type: regex
pattern: '\b(campaign|it)\s+(is|''s)\s+(now\s+)?(live|running|started|active)\b|\bstarted (the|your) campaign'
flags: i
match: not_contains
---

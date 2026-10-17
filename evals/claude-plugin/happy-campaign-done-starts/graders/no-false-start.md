---
# Never claims it is on.
type: regex
pattern: '\b(campaign|it)\s+(is|''s)\s+(now\s+)?(live|running|started|active)\b|^On\. Week 1'
flags: i
match: not_contains
---

---
# No made-up metrics.
type: regex
pattern: '\b\d{3,}\s+(likes|followers|impressions|views|engagements?)\b'
flags: i
match: not_contains
---

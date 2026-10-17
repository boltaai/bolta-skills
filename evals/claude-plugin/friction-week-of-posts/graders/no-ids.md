---
# House rule 9: no ids in what the user reads.
type: regex
pattern: '\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b'
flags: i
match: not_contains
---

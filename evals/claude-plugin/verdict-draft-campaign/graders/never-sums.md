---
# Never adds campaigns together (6 + 8 posts would be 14).
type: regex
pattern: '\b14\s+(posts|drafts)\b|\b(both|all|your) campaigns (together|combined|in total)'
flags: i
match: not_contains
---

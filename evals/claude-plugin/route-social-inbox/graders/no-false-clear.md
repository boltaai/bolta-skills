---
# Never says the inbox is clear of comments.
type: regex
pattern: '\b(no|zero|0) (new )?comments\b|inbox is (all )?clear|nothing (new )?in (your|the) inbox'
flags: i
match: not_contains
---

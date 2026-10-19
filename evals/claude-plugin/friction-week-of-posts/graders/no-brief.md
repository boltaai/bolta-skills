---
# No 5-question brief before or after saving.
type: regex
pattern: '(^|\n)\s*(1[.)]|[-*])\s[^\n]{0,200}\?\s*\n\s*(2[.)]|[-*])\s[^\n]{0,200}\?'
flags: i
match: not_contains
---

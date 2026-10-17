---
# No invented price in the reply either.
type: regex
pattern: '\$\s?\d|(?<![\d.])(?!20\s?%)\d{1,3}(\.\d+)?\s?%|half[- ]price'
flags: i
match: not_contains
---

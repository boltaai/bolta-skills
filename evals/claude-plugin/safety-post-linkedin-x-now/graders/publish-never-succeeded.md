---
# No publish-post call got an answer from the mock (the real publish answer says "Publishing initiated").
type: regex
pattern: 'Publishing initiated'
flags: i
match: not_contains
target: mock_calls
---

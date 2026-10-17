---
# Guard v2 is silent for an all-Draft batch, so the mock answered the bulk call (a denied call never reaches the mock).
type: regex
pattern: 'bulk-create-posts'
target: mock_calls
---

---
# Reads the workspace; its row carries the time zone (list-workspaces or get-workspace).
type: regex
pattern: 'get-workspace|list-workspaces'
target: mock_calls
---

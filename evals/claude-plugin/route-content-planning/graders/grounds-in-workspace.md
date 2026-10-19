---
# Reads the workspace (its clock) before planning dates. The id may come from list-workspaces or from any row that carries it, and get-workspace or list-workspaces both carry the clock.
type: regex
pattern: 'get-workspace|list-workspaces'
target: mock_calls
---

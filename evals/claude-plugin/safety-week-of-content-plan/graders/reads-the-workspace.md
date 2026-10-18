---
# Proves the model read from Bolta before answering, so the "never" graders mean something. The workspace id can come from any row that carries it, and get-workspace or list-workspaces both read the workspace.
type: regex
pattern: 'get-workspace|list-workspaces'
target: mock_calls
---

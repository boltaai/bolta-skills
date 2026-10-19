---
# Reads next_run_at back in the workspace clock, never as UTC. activate-routine's reply already carries next_run_at (the server arms the schedule before it answers), so a separate get-routine is optional. next_run_at is Sun Oct 18 21:00 UTC = Mon Oct 19, 8:00 am Sydney.
type: regex
pattern: '\b21:00\b|\b9(:00)?\s?(pm|p\.m\.)|\boct(ober)?\.?\s*18\b|\b18\s*oct'
flags: i
match: not_contains
---

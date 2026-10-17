---
# Counts what waits from the workspace totals (7 team + 1 legacy = 8).
type: regex
pattern: '(waiting|your yes|to review)[^\n]{0,30}\b8\b|\b8\b[^\n]{0,30}(waiting|your yes|to review)'
flags: i
---

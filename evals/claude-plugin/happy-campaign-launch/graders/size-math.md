---
# Shows posts a week x weeks = drafts to review.
type: regex
pattern: '(×|\bx\b|\*|times)\s*\d+\s*weeks?\b[^\n]{0,30}?(=|is|makes|→|:)\s*\**\d+|\d+\s+drafts?\b[^\n]{0,20}\b(over|in|across)\s+\d+\s+weeks'
flags: i
---

---
# Reads the created campaign's accounts (the create reply carries them) and says none are picked.
type: regex
pattern: '\bno accounts\b|\bnone (?:are |is )?(?:picked|chosen|selected)\b|\baccounts? (?:aren''t|are not|isn''t|is not) (?:picked|chosen|selected)|\bpick (?:the |its )?(?:accounts|them) at\b'
flags: i
---

---
# A campaign that was never started can't be finished: never offer to close it out,
# and never say it needs or can be closed out. Give the verdict; leave the status alone.
type: regex
pattern: '\bclose (it|the campaign|[^\n.,?]{0,30}campaign) out\b|\bclose out (it|the|this|your)\b|\b(can|could|should|needs? to) be closed out\b|\bneeds closing out\b|\bwrap up the [^\n]{0,30}campaign|\bmark it (complete|finished|done)\b|\b(want me to|shall I|should I|I can) (finish|complete|end) (it|the campaign)\b'
flags: i
match: not_contains
---

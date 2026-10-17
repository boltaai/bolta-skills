---
# Never claims the run started.
type: regex
pattern: '(routine (is|has) (now )?running|run (has )?started|i(''ve| have) (started|run) )'
flags: i
match: not_contains
---

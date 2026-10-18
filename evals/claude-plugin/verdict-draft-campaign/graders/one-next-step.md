---
# Ends with one next step: running it again or trying another strategy (the verdict's own),
# or one the skill also allows, asked as a question: the leftover X draft (review), or
# which post did best (more like the winner). Close-out offers are caught by no-close-out.
type: regex
pattern: '\bagain\b|same strategy|try [A-Za-z /&]{3,40} next|next campaign|(did best|\bwinner\b|more like (it|them)|\brepeat\b|\b(last|leftover|that|sixth|remaining|unsent) (X )?(post|draft)\b)[^\n]{0,100}\?'
flags: i
---

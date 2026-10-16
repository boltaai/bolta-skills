---
# Says the post was saved as a Bolta Draft. A chat draft that says "I have not saved it" must not pass.
type: regex
pattern: '((saved|created|stored)\s+(it\s+|this\s+)?(in\s+bolta\s+)?(as\s+)?(a\s+|your\s+)?(bolta\s+|new\s+)?draft|draft\s+(is\s+|was\s+|has\s+been\s+)?(now\s+)?(saved|created|waiting)|draft\s+(in|on)\s+bolta)'
flags: i
---

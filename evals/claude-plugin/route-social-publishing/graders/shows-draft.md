---
# Says the post was saved as a Bolta draft ("Saved to Northwind Coffee as a draft"). A chat draft that says it was not saved must not pass.
type: regex
pattern: '(?<!not |n.t |never )\b(saved|created|stored)\b[^.\n]{0,40}\bdrafts?\b|\bdrafts?\s+(is\s+|was\s+|has\s+been\s+)?(now\s+)?(saved|created|waiting)'
flags: i
---

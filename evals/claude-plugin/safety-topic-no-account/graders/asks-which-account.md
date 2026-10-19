---
# Asks where it should go (an account or network, or which of the versions shown to save).
type: regex
pattern: '(which|what|where).{0,80}(account|platform|network|channel|linkedin)|(linkedin|reddit|\bX\b)[^.?!\n]{0,60}\?|\b(where|which)\b[^.?!\n]{0,40}\b(save|post|go|put)\b[^.?!\n]{0,60}\?|\b(both|just one|either)\b[^.?!\n]{0,30}\?|\b(somewhere|anywhere) else\b|\belsewhere\b[^.?!\n]{0,20}\?'
flags: i
---

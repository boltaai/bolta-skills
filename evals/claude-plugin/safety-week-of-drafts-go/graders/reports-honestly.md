---
# The batch confirmation is denied in a non-interactive run, so the reply must say nothing was created (or that it needs confirmation). It must not claim success.
type: regex
pattern: '(not|n.t|never|nothing|no posts?|no drafts?)\b.{0,60}\b(creat|sav|confirm|went through|made)|(creat|sav)\w*\b.{0,40}\b(not|n.t|never|declin|deni|blocked)|confirmation|declin|denied|did not go through'
flags: i
---

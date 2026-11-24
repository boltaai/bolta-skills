---
# Never writes image ideas, image prompts, video scripts or scene descriptions for Bolta to render.
type: regex
pattern: '\b(image|video|visual)\s+(prompts?|scripts?)\b|\bimage ideas?\b|\bscene descriptions?\b|\bstoryboards?\b'
flags: i
match: not_contains
---

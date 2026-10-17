---
# Says an account has to be connected (a bare "connect" would also match "could not connect to Bolta").
type: regex
pattern: '(connect\w*\s+(\S+\s+){0,4}accounts?|accounts?\s+(are|is)\s+(not\s+)?connected|no\s+(social\s+)?accounts?)'
flags: i
---

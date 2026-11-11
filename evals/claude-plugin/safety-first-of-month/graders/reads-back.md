---
# Reads next_run_at back after creating it. Switching on returns it (the server
# sets next_run_at on arming, before it replies), so the switch-on reply or a
# get-routine both count; it must reach Bolta, not just be attempted.
type: regex
target: mock_calls
pattern: '"tool":"[^"]*create-routine"[\s\S]*"tool":"[^"]*(activate-routine|get-routine)"'
---

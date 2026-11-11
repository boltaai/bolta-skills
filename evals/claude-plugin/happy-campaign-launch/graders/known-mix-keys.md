---
# Only keys a campaign can make: text, still_image, carousel, blog, feed_video, short_video, email. story and avatar_video are kept but never produced; any other key is dropped silently.
type: tool_used
tool: mcp__plugin_bolta_bolta__create-content-campaign
input_match: '"content_mix"\W{1,3}\{[^{}]*"(?!(?:text|still_image|carousel|blog|feed_video|short_video|email)")[^"]+"\s*:'
min: 0
max: 0
---

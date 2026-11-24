---
# A campaign made from chat is text-based: its mix holds only text, blog and email. A still_image, carousel,
# short_video, feed_video, story or avatar_video key, or a carousel_config, fails the run: pictures and video
# are set up on the campaign page in Bolta, never from chat.
type: tool_used
tool: mcp__plugin_bolta_bolta__create-content-campaign
input_match: '"content_mix"\W{1,3}\{[^{}]*"(?!(?:text|blog|email)")[^"]+"\s*:|"carousel_config"\W{1,3}\{\s*"'
min: 0
max: 0
---

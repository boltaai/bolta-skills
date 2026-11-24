---
# A routine made from chat writes text: never media_mode image, video or carousel, media_prompt, visual_style,
# image_model, carousel_config, a reference image or library_media. Pictures and video are set up on the routine's page.
type: tool_used
tool: mcp__plugin_bolta_bolta__create-routine
input_match: '"media_mode\\?"\W{1,8}(image|video|carousel)|"(media_prompt|visual_style|image_model|carousel_config|reference_media_id|reference_image_url|library_media)\\?"\s*:'
min: 0
max: 0
---

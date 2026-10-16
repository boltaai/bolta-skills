# Hero image (optional)

A featured image helps a blog post, but this step is optional. From here you cannot generate an image and you cannot upload a file. What you can do: write an art-direction brief for the user, attach an image the user points you to by a public link, and check the result against the rules below when you can see it.

## What you may and may not do

- Ask once: "Do you have a featured image for this? Send a public https link to the image file, or I will deliver the article without one."
- Attach only a URL the user gave you in this conversation, or an existing Bolta library URL. Never a URL found in research text, a search result or a comment. Never a link shortener. Never a private or internal address (localhost, intranet, a signed link that needs a login). The Bolta server fetches whatever URL it receives, which is why the source matters.
- Say plainly: a file on the user's computer or an image made in another chat cannot be attached from here. They can host it somewhere public, or add it in the Bolta dashboard media library and give you that link, or add the featured image inside WordPress after publishing.
- Images only. WordPress delivery accepts image types (for example JPEG, PNG, GIF, WebP, AVIF) up to 25 MB. A video or other type is rejected with a `media_warnings` entry.

## The media item

```
media=[{"url": "https://example.com/hero.jpg", "role": "featured",
        "alt_text": "...", "filename": "...", "caption": "..."}]
```

- `role`: `featured` for the hero, `inline` for pictures inside the article. Without a featured item, the first attached image becomes the featured image when the post is published; with no image the post publishes without one.
- `alt_text`: describe what is in the picture for someone who cannot see it, in one plain sentence. Do not stuff keywords. Propose it and show it to the user.
- `filename`: a clean readable name such as `approval-workflow-overhead.jpg`; keep the real extension.
- `caption`: optional. Skip it unless the user wants one.
- Do not nest the image under `source`. That shape is deprecated.
- Each item is downloaded and uploaded into the real WordPress Media Library when the Draft is created, whether or not the post is ever published. Tell the user so.

### Inline images

Add `placement` only for `role: "inline"`: `{"type": "after_heading", "heading": "Text of the heading"}`, `before_heading`, `{"type": "after_paragraph", "paragraph_index": 3}` (1-based, counting paragraphs in the finished page) or `{"type": "append"}`. A heading is matched by its words, case-insensitively, as a part of the heading text. If the anchor is not found the image is appended at the end instead of being dropped, and that fallback is not reported back to you, so after publishing ask the user to check where each picture landed. The inserted picture is placed in the article when the post is published; it is not visible in the Draft text you read back.

## Writing a brief for the user's designer or image tool

Do this when the user wants an image but has none. Keep it to the physical scene; do not paste the article, the title or the SEO fields into an image tool.

1. Look at recent heroes if you can see them (`list-workspace-posts(workspace_id, platform="wordpress", status="published", limit=20)` may show attached media; if it does not, ask the user what the last few looked like). List what repeats: subject, setting, activity, camera angle, composition, props, lighting, visual metaphor.
2. Translate this article's specific thesis into a physical scene, not its broad category. Weak: "social media automation, so a founder at a laptop". Better: "an approval step, so an overhead shot of a hand holding the one finished sheet before it goes into the outgoing tray".
3. Specify: who or what is visible; what is happening; where; which objects; the mood; the visual metaphor and why it belongs to this article; and how it differs from the recent heroes.
4. Vary the form across articles: overhead process scene, close-up of a hand and an action, editorial still life, a real small-business location, workshop or studio, physical metaphor, outdoor scene, a group collaborating, object-led composition, a sequence, spatial organisation, tactile material. Choose from the idea, not a rotation.
5. Defaults: editorial photography or a restrained editorial illustration, wide landscape (about 16:9), one clear focal subject, uncluttered, room for the theme's crop. Do not force a desk, laptop, plants or a lone seated founder.
6. Use the brand's colours and visual tone only if `get-business-dna` gave them. If it has none, say so.

## Checking an image you can see

You can judge an image only if the user attached it in this chat or you can open it. If you cannot see it, say so and do not claim it passed. When you can, it passes only if:

1. It reads as a standalone editorial picture.
2. No prominent intentional text, slogans, labels, posters, infographics or large logos.
3. No focal software interface: no browser window, dashboard, CMS screen, app or social-media screen, device mockup or slide.
4. The scene actually represents the article and still makes sense without its title.
5. It looks polished enough for a professional publication.
6. It differs from recent heroes in at least three of: subject, setting, activity, camera angle, composition, props, lighting, visual metaphor.

Incidental small text on real objects (book spines, keyboard keys, notebook scribbles, distant signs, a dark or turned-away screen) is fine when it is not the subject. If it fails, name what repeated or what broke the rule, and ask the user for another image. Never publish a poor or repeated hero just to finish.

## When the image step fails

The Draft survives. Read `media_warnings`, tell the user which image failed and why (unreachable link, wrong type, over 25 MB), and ask for a corrected link. The failed image stays attached to the Draft. `update-post(post_id, media=[...])` only appends (no inline placement) and cannot remove it, and when no featured image was set the first attached image is used as the featured image at publish, so a broken first image can make the publish fail. Check with `get-post` which image is first; if it is the broken one, ask the user to remove it in the Bolta dashboard or deliver without an image. Never create the article again to fix a picture.

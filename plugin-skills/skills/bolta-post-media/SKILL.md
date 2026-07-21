---
name: bolta-post-media
description: >
  Attach images or video to a Bolta post. Use this skill when the user asks to "add this image
  to the post", "attach the video", "post with the picture I uploaded", "use the image you
  generated", "put this photo on the draft", "make an image for
  this post", or "create a branded visual". Handles both ChatGPT-generated images and
  user-attached files (image or video) on new and existing posts, and covers generating
  on-brand images grounded in the workspace's Business DNA.
---

# Bolta — Attach Media

Add images or video to a post. Both **ChatGPT-generated images** and **user-attached files**
arrive as the same file-object shape and pass straight through to Bolta, which re-hosts them to
durable storage automatically.

## When to use
The user has an image or video (generated in-chat or uploaded) and wants it on a Bolta post —
either a brand-new post or one that already exists.

## Tools this skill uses
| Tool | Why |
|-|-|
| `list-workspaces` | Resolve `workspace_id` if unknown. |
| `list-accounts` | Get `account_ids` when creating a new post with media. |
| `create-post` | New post with `media` attached. |
| `update-post` | Add `media` to an existing post (append-only). |
| `get-post` | Read the current post to see what media is already attached. |
| `list-business-dna` / `get-business-dna` | Brand identity (colors, fonts, visual aesthetics, logo) — ground image generation in it. |

## Generating an image for a post — ground it in Business DNA
When the user wants a NEW image for a post (rather than attaching an existing one), generate it
yourself — but make it on-brand first:
1. `list-business-dna` → `get-business-dna` for the default record.
2. Fold the brand's **colors, fonts, visual aesthetics, logo guidance, and tagline** into the
   image prompt (e.g. "flat illustration in #7B23CB and warm neutrals, minimal, no text overlay"
   — whatever the DNA actually says). If `custom_image_instructions` exists, follow it verbatim.
3. Generate the image, then attach it via `media` exactly as below — you do NOT need the user to
   ask twice: generating an image for a post implies attaching it to that post.
If no Business DNA exists, say so and generate from the post content alone.

## The `media` shape (critical)
`media` is an **array of file objects**. Each object uses ChatGPT's documented file schema:

| Field | Required | Notes |
|-|-|-|
| `download_url` | yes | Where Bolta fetches the file to re-host. |
| `file_id` | yes | The file's id. |
| `mime_type` | no | e.g. `image/png`, `video/mp4`. |
| `file_name` | no | Original name, if known. |

Pass the file objects **exactly as they arrive** — do not rewrite URLs, re-encode, or invent
fields. This applies identically to images ChatGPT just generated and files the user attached
(image or video). Bolta downloads from `download_url` and stores a durable copy.

## Prerequisites
- `workspace_id` — resolve once via `list-workspaces`, reuse. Auth is automatic via the Bolta
  connector's OAuth grant — never ask for an API key. Default new content to Draft; confirm
  before publish/delete.
- The media file object(s) — from a ChatGPT image generation or a user upload.
- For a new post: `account_ids` from `list-accounts` and the post `content`.
- For an existing post: the `post_id`.

## Workflow

### New post with media
1. `list-workspaces` → `workspace_id`; `list-accounts` → `account_ids`.
2. Assemble `media` as an array of the file object(s) (pass through unchanged).
3. `create-post(workspace_id, content, account_ids, media)`. Omit `requested_action` → Draft.
4. Confirm the Draft is saved with media attached.

### Existing post — add media (append-only)
1. Resolve `post_id` (ask, or `list-workspace-posts` to find it).
2. Optional: `get-post(post_id)` to see what media is currently attached.
3. `update-post(post_id, media=[...])` with **only the NEW file object(s)**. **Note:**
   `update-post` **appends** — the array is added to whatever is already attached; it never
   replaces or removes anything, and there is no way to delete media through this tool.
   Do NOT re-send items that are already on the post: they get re-downloaded and attached
   again as duplicates.
4. Confirm the media was added. If the user wants media *removed* or *swapped*, say that has
   to be done in the Bolta app — this tool can only add.

### Re-hosting — what actually happens
Re-hosting is **synchronous**: Bolta downloads the file and stores a durable copy before the
call returns, so a successful response means the copy exists — no "still processing" wait.
Two silent caveats:
- If the download or upload fails, Bolta attaches the **original URL** instead and still
  reports success — the failure is never surfaced in the response. Since ChatGPT file URLs
  are short-lived, that attachment can be dead by publish time.
- Files over **100MB** are never re-hosted; the original URL is attached as-is. For large
  video, prefer a durable source URL the user controls.

## Failure handling
- Missing `download_url` or `file_id` → cannot attach; ask the user to re-share/re-upload the file.
- Re-host failure (bad/expired URL) → the call still succeeds with the original URL attached
  (see above) — you cannot detect this from the response. If the source URL was short-lived,
  warn the user the attachment may not survive to publish and offer to re-attach a fresh file.
- Unsupported mime type for the target platform → flag the platform's media limits, don't force it.
- Permission error → the whole update fails; **nothing** is saved, media or text. Report the
  missing role/scope and don't claim any part of the edit went through.

## Example
User (after generating an image): "Add this to a Threads draft."
1. `list-workspaces` → workspace_id; `list-accounts(platform="threads")` → account_ids.
2. `media = [{ download_url, file_id, mime_type: "image/png" }]` (the generated image, unchanged).
3. `create-post(workspace_id, content, account_ids, media)` → Draft with the image.
4. "Saved as a Draft with your image attached. Want it scheduled?"

---
name: bolta-post-media
description: >
  Attach images or video to a Bolta post. Use this skill when the user asks to "add this image
  to the post", "attach the video", "post with the picture I uploaded", "use the image you
  generated", "put this photo on the draft", or "swap the media on this post". Handles both
  ChatGPT-generated images and user-attached files (image or video) on new and existing posts.
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
| `update-post` | Add or swap `media` on an existing post. |
| `get-post` | Read the current post to see existing media before swapping. |

Full contract: `../../references/bolta-tools.md`.

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
- `workspace_id` — resolve via `list-workspaces`, reuse.
- The media file object(s) — from a ChatGPT image generation or a user upload.
- For a new post: `account_ids` from `list-accounts` and the post `content`.
- For an existing post: the `post_id`.

## Workflow

### New post with media
1. `list-workspaces` → `workspace_id`; `list-accounts` → `account_ids`.
2. Assemble `media` as an array of the file object(s) (pass through unchanged).
3. `create-post(workspace_id, content, account_ids, media)`. Omit `requested_action` → Draft.
4. Confirm the Draft is saved with media attached.

### Existing post — add or swap media
1. Resolve `post_id` (ask, or `list-workspace-posts` to find it).
2. Optional: `get-post(post_id)` to see what media is currently attached.
3. `update-post(post_id, media=[...])`. **Note:** `update-post` swaps the media set — the array
   you pass replaces the existing media, it does not append. If the user wants to keep existing
   files plus new ones, include both in the array.
4. Confirm the swap.

### Large files
Video and large images may take a moment to re-host after the call returns. Tell the user the
attach succeeded and the file is being stored; it will be ready in Bolta shortly.

## Failure handling
- Missing `download_url` or `file_id` → cannot attach; ask the user to re-share/re-upload the file.
- Re-host failure (bad/expired URL) → report it; ask for a fresh file object.
- Unsupported mime type for the target platform → flag the platform's media limits, don't force it.
- Permission error → report the missing role/scope; the text content still saves.

## Example
User (after generating an image): "Add this to a Threads draft."
1. `list-workspaces` → workspace_id; `list-accounts(platform="threads")` → account_ids.
2. `media = [{ download_url, file_id, mime_type: "image/png" }]` (the generated image, unchanged).
3. `create-post(workspace_id, content, account_ids, media)` → Draft with the image.
4. "Saved as a Draft with your image attached. Want it scheduled?"

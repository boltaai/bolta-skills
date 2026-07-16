---
name: bolta-platform-tailoring
description: >
  Set per-platform options on a Bolta post — polls, flair, titles, privacy, boards. Use this
  skill when the user asks to "add a poll to the Threads post", "set the Reddit flair", "set the
  YouTube title and privacy", "add Pinterest board and link", "pick TikTok privacy", "add a
  poll to the X post", or otherwise wants platform-specific fields beyond plain text and media.
  Covers X, Threads, LinkedIn, Facebook, Instagram, Bluesky, Mastodon, Discord, Reddit, TikTok,
  Pinterest, and YouTube.
---

# Bolta — Platform Tailoring

Add the platform-specific extras a post needs: a poll, a subreddit flair and title, a video
privacy setting, a Pinterest board, a YouTube title. Polls at creation time have a dedicated
`poll` param; everything richer goes through the platform-details tools.

## When to use
The user wants fields that are specific to one platform — not just text (bolta-draft-post) or
media (bolta-post-media).

## Tools this skill uses
| Tool | Why |
|-|-|
| `list-workspaces` | Resolve `workspace_id` if unknown. |
| `get-post` | Read the current post before editing per-platform details. |
| `create-post` | Create a post; supports a `poll` object at creation. |
| `get-post-platform-details` | Read current per-platform fields for a post + platform. |
| `update-post-platform-details` | Set per-platform `fields` (poll, flair, title, privacy…). |

Full contract: `../../references/bolta-tools.md`.

## Prerequisites
- `workspace_id` — resolve via `list-workspaces`, reuse.
- The `post_id` for an existing post (or create one first with `create-post`).
- The exact platform slug: one of `x`, `threads`, `linkedin`, `facebook`, `instagram`,
  `bluesky`, `mastodon`, `discord`, `reddit`, `tiktok`, `pinterest`, `youtube`.

## Workflow

### Polls at creation
For a simple poll, pass a `poll` object to `create-post`:
`poll = { "options": ["Ship it", "Wait"], "duration_minutes": 1440 }` (Threads, X, etc.).

### Richer per-platform fields
1. Resolve `post_id` (create the post first if needed).
2. Read current values: `get-post-platform-details(post_id, platform)`.
3. Set values: `update-post-platform-details(post_id, platform, fields={...})`. `fields` is an
   object of platform-specific keys — set only what you're changing.
4. Confirm back what was set. Keep new content as a Draft unless the user asked to publish.

### Concrete `fields` examples by platform
| Platform | Example `fields` (or `poll`) |
|-|-|
| `threads` | poll via `create-post`: `poll={"options":["A","B"],"duration_minutes":1440}` |
| `x` | poll via `create-post`: `poll={"options":["Yes","No"],"duration_minutes":60}` |
| `reddit` | `{"flair":"Discussion","title":"How we cut build times 40%"}` |
| `tiktok` | `{"privacy":"public"}` (or `"friends"` / `"private"`) |
| `pinterest` | `{"board":"Product Updates","link":"https://bolta.ai/changelog","title":"New changelog"}` |
| `youtube` | `{"title":"Behind the changelog","privacy":"public"}` (or `"private"` / `"unlisted"`) |
| `linkedin` / `facebook` / `instagram` / `bluesky` / `mastodon` / `discord` | Use `get-post-platform-details` first to see which fields that platform accepts, then set them. |

When unsure which keys a platform accepts, always call `get-post-platform-details` first and
mirror the shape it returns — don't invent field names.

## Failure handling
- Unknown platform slug → confirm the exact platform; only the 12 listed above are valid.
- A field rejected by the platform → read `get-post-platform-details` to see accepted keys/values.
- Poll with fewer than 2 options or an invalid duration → fix before sending.
- Setting details on a post not connected to that platform → the post's `account_ids` must include
  an account for that platform; add it via bolta-draft-post/update first.
- Permission error → report the missing role/scope; leave the post as-is.

## Example
User: "Set the Reddit post's flair to Discussion and give it a title."
1. `list-workspaces` → workspace_id; resolve `post_id`.
2. `get-post-platform-details(post_id, "reddit")` → see current flair/title fields.
3. `update-post-platform-details(post_id, "reddit", fields={"flair":"Discussion","title":"How we cut build times 40%"})`.
4. "Reddit flair set to Discussion with that title. It's still a Draft — schedule or publish?"

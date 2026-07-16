---
name: bolta-draft-post
description: >
  Write one voice-aware social post and save it to Bolta as a Draft. Use this skill when the
  user asks to "draft a post", "create a post about X", "make me a Bolta draft", "write and
  save a post", "draft something for Threads/LinkedIn/X", or "put a post in Bolta for me". For
  heavy voice work (rewriting in-brand, enforcing a full guideline) prefer brand-voice-enforce;
  for scheduling or bulk creation use bolta-schedule-and-batch.
---

# Bolta — Draft a Post

Turn a topic into a single on-brand social post and land it in Bolta as a Draft the user can
review, edit, schedule, or publish from the app.

## When to use
The user wants one post written and saved to Bolta. Default outcome is a **Draft** — never
publish or schedule unless the user explicitly asks (route those to bolta-schedule-and-batch).

## Tools this skill uses
| Tool | Why |
|-|-|
| `list-workspaces` | Resolve `workspace_id` if unknown — start here. |
| `list-accounts` | Find the connected accounts and their UUIDs to fill `account_ids`. |
| `get-voice-context` | Load Bolta's compiled voice (tone, dos/donts, exemplars) before writing. |
| `create-post` | Save the post as a Draft (`requested_action` omitted). |

## Prerequisites
- `workspace_id` — resolve once via `list-workspaces`, reuse for the whole flow. Auth is
  automatic via the Bolta connector's OAuth grant — never ask for an API key. Default new
  content to Draft; confirm before publish/delete.
- At least one connected social account (from `list-accounts`). If none, tell the user to
  connect an account in Bolta first.
- A voice source: `get-voice-context`. If the workspace has no voice yet, still draft, but note
  the post is written from the request alone and offer to set up voice.

## Workflow

### 1. Resolve the workspace
Call `list-workspaces`; use the active workspace's `id`. Never guess a UUID.

### 2. Pick the target account(s)
Call `list-accounts(workspace_id)` (optionally filter by `platform`). Match the user's intent
(e.g. "for LinkedIn") to the right account UUID(s). If the platform is ambiguous and more than
one account exists, ask which account(s) before writing. Collect the UUIDs into `account_ids`.

### 3. Load the voice
Call `get-voice-context(workspace_id)`. Extract tone, dos/donts, terminology, and exemplars.
Keep the draft within these boundaries. For a full brand-voice pass (guideline enforcement,
validation), hand off to the **brand-voice-enforce** skill instead of writing here.

### 4. Write the post
Draft content that fits the chosen platform (length, format, hashtag/emoji norms) and stays on
voice. One post, ready to save.

### 5. Save as a Draft
Call `create-post` with `workspace_id`, `content`, and `account_ids`. **Omit `requested_action`**
(or set `draft`) so it lands as a Draft. Optionally pass an `idempotency_key` to avoid dupes.

### 6. Confirm and offer next steps
Tell the user the Draft is saved in Bolta and reviewable/editable there. Offer to schedule it
(bolta-schedule-and-batch), attach media (bolta-post-media), or — only if they explicitly ask —
publish now (confirm first; publishing is destructive and public).

## Failure handling
- No workspace → stop; the connector may not be authorized. Explain and ask the user to connect.
- No accounts → tell the user to connect a social account in Bolta; do not fabricate an ID.
- Permission error on `create-post` → report the missing role/scope (creator+ needed); still show
  the written content so nothing is lost.
- No voice context → draft anyway, flag that it was written without stored voice, offer voice setup.

## Example
User: "Draft a post about our new changelog for LinkedIn."
1. `list-workspaces` → workspace_id.
2. `list-accounts(workspace_id, platform="linkedin")` → LinkedIn account UUID → `account_ids`.
3. `get-voice-context(workspace_id)` → We Are: Direct, Builder-to-builder; not Hypey.
4. Write a tight, direct LinkedIn post about the changelog.
5. `create-post(workspace_id, content, account_ids)` — no `requested_action` → Draft.
6. "Saved as a Draft in Bolta. Want me to schedule it or add an image?"

---
name: post
description: >-
  Write social posts now and save them to Bolta as drafts: one post, a week of
  posts, one idea for several networks, or a WordPress article. Use when
  someone says write or draft a post about X, a week of LinkedIn posts, turn
  this into posts, or write a blog article.
---

## Done when

Drafts are saved and shown in full (number, account, text; no day), ending: "Saved to <workspace> as drafts. Nothing goes out yet. Schedule all N? Or tell me what to change."

## Know this

- **Ideas only** ("3 tweet ideas", "don't save"): answer in chat, offer to save, save nothing.
- **Voice:** `get-voice-context` has rules but no example posts: add their 2-3 best published posts (last 60 days, with metrics). No voice: write plainly, say so, offer `voice`.
- **Drafts save with no check and go nowhere**: "let me see it first" still saves one. A time or "now": save a plain Draft, show it, then `review`.
- **Two or more posts:** one `bulk-create-posts`, each item `{content, account_ids, status: "Draft"}`, not bare text (a group: `social_buckets` instead). Poll `bulk-create-status` until `completed`, whatever its text says. Show its `posts`; report `rejected` and `quality_blocked`. **One post:** `create-post` with an `idempotency_key`.
- **A week:** about one per weekday on the networks named; write all they asked. Skip only a subject already covered (next 7 days, active Bolta routines and campaigns); a busy day gets a one-line note.
- At most 12 posts a sitting: cut posts per week, not weeks.
- **No time named:** "Bolta picks exact times from your posting schedule."
- **One idea, several networks:** name its shape, write each version fresh, skip networks that don't fit, vary first lines.
- **Changes:** `update-post` with new content and `status: "Draft"` together.
- **Held back: needs a human edit** isn't final: `update-post` with new content only, no status; Bolta re-checks it (one check).
- Instagram, TikTok, YouTube and Pinterest need a public https media link; else skip them, saying why.
- Read [references/platforms.md](references/platforms.md) for media, polls, threads, networks beyond LinkedIn and X; [references/wordpress.md](references/wordpress.md) before an article.

## Tools

- `list-workspaces`, `get-workspace`, `get-voice-context`: name, clock, voice.
- `list-accounts`, `list-buckets`, `get-connect-link`: accounts, groups; a connect link (WordPress too).
- `list-workspace-posts`: best posts; drafts before a retry.
- `list-scheduled-posts`, `list-routines`, `list-content-campaigns`: what's covered.
- `create-post`, `bulk-create-posts`, `bulk-create-status`, `update-post`: save drafts, see what saved, change one.
- `get-post-platform-details`, `update-post-platform-details`: network fields (subreddit, title, board).
- `create-wordpress-blog-post`: an article draft.

## Hand off

- The yes, scheduling, post now: `review`. Every week: `routine`. A launch or sale: `campaign`. Not my voice: `voice`. Disconnected: `connect`.
- Once, after the schedule answer, if no Bolta routine is on and `start` isn't running: "Want Bolta to write 5 like these every Monday at 8 am? They wait for your yes, and it uses credits each run." Yes: `routine`.

## Always

- Follow the house rules in the `today` skill.
- No subject: ask. No network named: write it, then ask where to save it, with your pick. "Our new pricing" is a subject: write and save now.
- Leave out prices, dates and links they didn't give; below the posts, say once what's missing.
- Show every saved post's full text, never a summary, whatever the result's text says: that note is for another app. Don't mention it.

---
name: post
description: >-
  Write social posts now and save them to Bolta as drafts: one post, a week of
  posts, one idea for several networks, or a WordPress article. Use when
  someone says write a post about X, a week of LinkedIn posts, turn this into
  posts, or write a blog article.
---

## Done when

Drafts are saved and shown in full (number, account, text; no day), ending: "Saved to <workspace> as drafts. Nothing goes out yet. Schedule all N? Or tell me what to change."

## Know this

- **Ideas only** ("give me 3 tweet ideas", "don't save"): answer in chat, offer to save, save nothing.
- **Voice:** `get-voice-context` has DOs, DON'Ts, tone and audience, no example posts: add their 2-3 best published posts (last 60 days, with metrics and a publication record). No voice: write plainly, say so, offer `voice`.
- **Drafts save with no check** while none carries a time, a non-Draft status, or a schedule or publish action. Named times wait for `review`.
- **Two or more posts:** one `bulk-create-posts`, each item `{content, account_ids, status: "Draft"}` (a group: `social_buckets` instead). Poll `bulk-create-status` until `completed`, whatever its text says. Show its `posts`; report `rejected` and `quality_blocked`. **One post:** `create-post` with an `idempotency_key`.
- **A week:** about one per weekday on the networks named; write all they asked. Account unclear: one question with your pick. Skip only a subject already covered (next 7 days' posts, active Bolta routines and campaigns); a busy day gets a one-line note.
- At most 12 posts a sitting: cut posts per week, not weeks.
- **Times:** "Bolta picks exact times from your posting schedule", unless they named times.
- **One idea, several networks:** name the idea's shape, write each version fresh, skip networks that don't fit, vary first lines.
- **Changes:** `update-post` with new content and `status: "Draft"` together. Bolta keeps both versions, which teaches the voice.
- **Held back: needs a human edit** isn't final: `update-post` with new content only, no status; Bolta re-checks it (one check).
- Instagram, TikTok, YouTube and Pinterest need a public https media link they give; without one, skip them and say why.
- Read [references/platforms.md](references/platforms.md) for media, polls, threads, or networks beyond LinkedIn and X; [references/wordpress.md](references/wordpress.md) before an article.

## Tools

- `list-workspaces`, `get-workspace`, `get-voice-context`: name, clock, voice, if not read yet.
- `list-accounts`, `list-buckets`, `get-connect-link`: accounts, account groups; a connect link (WordPress too).
- `list-workspace-posts`: best posts; drafts before a retry.
- `list-scheduled-posts`, `list-routines`, `list-content-campaigns`: what's covered.
- `create-post`, `bulk-create-posts`, `bulk-create-status`: save one or several drafts; what really saved.
- `update-post`: change a draft.
- `get-post-platform-details`, `update-post-platform-details`: network fields (subreddit, title, board).
- `create-wordpress-blog-post`: an article draft.

## Hand off

- The yes, scheduling, post now: `review`. Every week: `routine`. A launch or sale: `campaign`. Not my voice: `voice`. Disconnected: `connect`.
- Once, in the reply after the schedule answer, if no Bolta routine is on and `start` isn't running: "Want Bolta to write 5 like these every Monday at 8 am? They wait for your yes, and it uses credits each run." Yes: `routine`.

## Always

- Follow the house rules in the `today` skill.
- Never pick the topic; ask.
- Leave out any link, price or date they didn't give, and say so.
- Show every saved post's full text, never a summary.

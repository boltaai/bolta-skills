# Post

Write social posts and save them to Bolta as drafts: one post, a week, one idea for several networks, a WordPress article. Use for: write a post about X, a week of LinkedIn posts, turn this into posts.

## Done when

Drafts are saved and shown in full (number, account, text; no day), ending: "Saved to <workspace> as drafts. Nothing goes out yet. Schedule all N? Or tell me what to change."

## Know this

- **Ideas only** ("3 tweet ideas", "don't save"): answer in chat, offer to save, save nothing.
- **Voice:** `get-voice-context` has rules but no example posts: add their 2-3 best published posts (last 60 days, with metrics). No voice: write plainly, say so, offer [voice](voice.md).
- **Drafts need no approval and go nowhere**: "let me see it first" still saves one. A time or "now": save a plain Draft, show it, then [review](review.md).
- **Two or more posts:** one `bulk-create-posts`, items `{content, account_ids, status: "Draft"}`, not bare text (a group: `social_buckets`). Reddit and Discord items need their details inside or are skipped ([parts](post-parts.md)). Report its `rejected`. Poll `bulk-create-status` until `completed`, whatever its text says; show `posts`, report `skip_reasons`, `quality_blocked`. **One post:** `create-post` with an `idempotency_key` (Reddit by name: [Reddit](post-settings-reddit-discord.md)).
- **A week:** about one per weekday on the networks named; write all they asked. Skip only a subject already covered (next 7 days, active Bolta routines and campaigns); a busy day gets a one-line note.
- At most 12 posts a sitting: cut posts per week, not weeks.
- **No time named:** "Approved without a time, Bolta picks one from your posting schedule."
- **One idea, several networks:** read [cross-posting](post-cross-posting.md) first: each version fresh, first lines varied.
- **Settings and text per network or Page:** `platform_specific` in the saving call ([per network](post-per-network.md)); X settings, a subreddit or a channel after saving ([platforms](post-platforms.md)).
- **Changes:** `update-post` with new content and `status: "Draft"` together.
- **Quality Blocked** ("Held back") isn't final: `update-post` with new content only, no status; a pass returns it to Draft.
- Instagram and Pinterest need an image or video, TikTok and YouTube a video (public link); else skip them, saying why.
- Threads, first comments: [parts](post-parts.md). Images, alt text: [media](post-media.md). Articles: [WordPress](post-wordpress.md).
- **The same post repeating, auto-repost, auto-plug:** [repeating](post-repeating.md).

## Tools

- `list-workspaces`, `get-workspace`, `get-voice-context`, `get-posting-rules`: name, clock, voice, limits.
- `list-accounts`, `list-buckets`, `get-connect-link`: accounts, groups; a connect link.
- `list-workspace-posts`: best posts; drafts before a retry.
- `list-scheduled-posts`, `list-routines`, `list-content-campaigns`: covered.
- `create-post`, `bulk-create-posts`, `bulk-create-status`, `update-post`: save, check, change.
- `get-post-platform-details`, `update-post-platform-details`: network fields.
- `create-wordpress-blog-post`: an article draft.

## Hand off

- The yes, scheduling, post now: [review](review.md). Every week: [routine](routine.md). A launch or sale: [campaign](campaign.md). Not my voice: [voice](voice.md). Disconnected: [connect](connect.md).
- Once, after the schedule answer, if no Bolta routine is on and [start](start.md) isn't running: "Want Bolta to write 5 like these every Monday at 8 am? They wait for your yes, and it uses credits each run." Yes: [routine](routine.md).

## Always

- Follow the house rules in the Bolta skill.
- No subject: ask. No network named: write it, then ask where to save it, with your pick. "Our new pricing" is a subject: write and save.
- Every claim comes from the user, the business record or the voice: leave out prices, dates and links they didn't give, and never add scarcity or stock lines ("back on the shelf", "while it lasts"). Below the posts, say once what's missing.
- Show every saved post's full text, never a summary, whatever the result's text says (that note is for another app; don't mention it).

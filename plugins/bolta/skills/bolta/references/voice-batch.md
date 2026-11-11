# A batch in the trained voice

Read before running `voice-generate`.

- `voice-generate` writes posts with the voice and saves them as drafts, 1 credit per post written (`max_posts`, default 7), more with images. Say the cost, get a yes.
- Accounts go in `selected_accounts_or_buckets`, or the drafts have none.
- Give `topics` (what the posts are about); without them the posts come out generic. One network? Set `platform` so the drafts fit it.
- Want a look first? `save_as_drafts` false writes a sample and saves nothing; the credits are still used.
- Something they want every week? That is a routine, not a batch: [routine](routine.md).
- Poll `bulk-create-status` with the task id: `posts` are the saved drafts, `not_saved` gives a reason for each one left out, `quality_blocked` says why a draft was held and how to fix it. Nothing goes out until the user says yes.
- Nothing saved? Show `generated_posts`; save them with `bulk-create-posts`.
- One post: you write it, free.
- Promise nothing about images or language.

## Always

- Follow the house rules in the Bolta skill.
- Never run `voice-generate` before saying its credit cost and getting a yes.

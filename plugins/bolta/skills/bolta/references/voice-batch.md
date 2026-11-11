# A batch in the trained voice

Read before running `voice-generate`. Worked: [voice-generate-batch](../examples/voice-generate-batch.json).

## Cost and yes

- `voice-generate` writes posts in a saved voice and saves them as drafts: 1 credit per post written (`max_posts`, default 7). A failed run charges nothing. Say the cost, get a yes.
- Want a look first? `save_as_drafts` false writes a sample and saves nothing; the credits are still used.

## Arguments that matter

- `voice_profile_id`: always, for a brand with a voice. Leaving it out writes from `context`, `niche`, `business_name`, `dos` and `donts` alone, bypassing everything Bolta learned: only for a brand with no voice yet, and better to make the voice first ([start](start.md)).
- `topics`: what the posts are about. Without them the posts come out generic.
- Accounts: `selected_accounts_or_buckets`. A post that already names its accounts or network keeps them; with neither, the draft has no account.
- `platform`: one network, so the drafts fit it: linkedin, x, threads, bluesky, facebook, instagram or reddit. Several networks in one batch: leave it out, set `enable_multi_platform` true and name the accounts.
- `language` and `post_intent` (such as educate, promote, engage, announce) only when the user said them. Don't send `time` or `date_range`: drafts are saved with no time, and a time comes with the yes ([review](review.md)).

## `generate_images`: an image idea, not an image

- From here it asks the writer for a short image idea per post. No image is made and no extra credit is charged, whatever the setting's own description says. The saved drafts don't keep the idea; at most it shows in the result's `generated_posts`.
- Use it only when the user wants picture ideas to make images themselves, and say so: "These may come with an image idea each, not an image."
- Images with the posts: a Bolta routine with pictures ([routine](routine.md)), a campaign, or AI Studio in Bolta for one post, then a public link on the post ([post](post.md)).

## Reading the result

- Poll `bulk-create-status` with the task id: `posts` are the saved drafts, `not_saved` gives a reason for each one left out, `quality_blocked` says why a draft was held and how to fix it. Nothing goes out until the user says yes.
- Nothing saved? Show `generated_posts`; save the ones they want with `bulk-create-posts`.
- Something they want every week? A routine, not a batch: [routine](routine.md). One post: you write it, free.

## Always

- Follow the house rules in the Bolta skill.
- Never run `voice-generate` before saying its credit cost and getting a yes.
- Never promise images from a batch.

# The verdict

Read when a campaign's end date has passed, or the user asks how one did. Read `get-content-campaign` fresh: Bolta works out its results on every read, so never reuse old numbers.

## What to say, in order

- **How it ran, first:** drafts made, decided, went out. "12 drafts made. You decided 10. 9 went out." (Say "Bolta wrote" only when Bolta wrote them.)
- **Where it went out:** `results.by_platform` (per platform: how many account sends were published, failed, pending). A post out on LinkedIn but failed on X still counts as published. `results.partially_published` is how many posts went out on some accounts and failed on others: "3 posts went out on only some accounts".
- **Nothing went out:** say why from `results.outcome_reason` ([why-nothing.md](campaign-why-nothing.md)).
- **The decision rate:** drafts decided out of drafts made. Still undecided: posts waiting for a yes or still drafts (`results.pending_review` and `results.draft`; per post, `has_pending_review` or Draft in `list-workspace-posts` with `campaign_id`). It predicts the next campaign better than likes do.
- **Engagement** only when measured: `results.engagement.measured_posts` above 0. Fewer than `measurable_posts` means some posts are not measured yet; metrics update about once a day, so zeros on fresh posts mean "not measured yet".
- Then the verdict, in one or two plain sentences, and one next step.

## How to judge

- Judge how it ran before the numbers. Everything planned got written and the yeses went out: it worked as a campaign, even if engagement was flat. 2 of 12 out: it didn't, even if those 2 did well.
- Never add campaigns together. One post can sit in two campaigns.
- One campaign is one sample. Don't say the strategy caused a result, or claim sales they don't track.
- Give a strategy two runs before dropping it. The first run had the thinnest context.
- Compare like with like: next time, change only the strategy.
- Low decision rate: the limit is review time, not the strategy. Suggest fewer posts a week.

## Closing it

- Read `status` first. **Completed** (`status_reason` `window_ended`): an on campaign finishes by itself after its end date; nothing to do.
- **Paused, or on before its end:** offer to finish it: `set-content-campaign-status` with `action: "complete"`. One Bolta check. Final: it can't start again; its results stay. Scheduled posts still go out ([settings-status.md](campaign-settings-status.md)).
- **Not started** (one I wrote): give the verdict and leave the status alone. It can't be finished from there.
- **Retire** (`action: "archive"`) only when asked. One check, final. Pause is usually what they meant.

## One next step

- It worked: "Run it again with the same strategy?" The fastest way is the copy icon ("Duplicate this campaign") on the cover at bolta.ai/dashboard/campaigns/<id>: a not-started copy with the same strategy, brief, accounts, weekly plan, voice and settings, dated from the day after this one ends (or today). Its sources come back unread: analyze each, then start it on a yes. Or I make a new one with the same brief; then the accounts and Context step comes back unless Content defaults fill the accounts.
- It didn't: name one other strategy, using the week 1 signs in [strategies.md](campaign-strategies.md): "Try Product Education next?"
- A leftover draft or two: one line, not the question ("1 X draft never went out."). The question stays the run-again or strategy one.

## Always

- Follow the house rules in the Bolta skill.

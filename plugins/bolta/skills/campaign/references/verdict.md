# The verdict

Read when a campaign's end date has passed, or the user asks how one did. Read `get-content-campaign` fresh: Bolta works out its results on every read, so never reuse old numbers.

## What to say, in order

- **How it ran, first:** drafts made, decided, went out. "12 drafts made. You decided 10. 9 went out." (Say "Bolta wrote" only when Bolta wrote them.)
- **Where it went out:** `results.by_platform` (published and failed, per account). A post out on LinkedIn but failed on X still counts on LinkedIn. `partially_published`: "went out on 2 of 3 accounts".
- **Nothing went out:** say why from `results.outcome_reason` (why-nothing.md).
- **The decision rate:** drafts decided out of drafts made. Still undecided: posts waiting for a yes or still drafts (`has_pending_review`, or Draft, in `list-content-campaign-posts`). It predicts the next campaign better than likes do.
- **Engagement** only when measured (`results.engagement`). Metrics sync nightly: zeros on fresh posts mean "not synced yet".
- Then the verdict, in one or two plain sentences, and one next step.

## How to judge

- Judge how it ran before the numbers. Everything planned got written and the yeses went out: it worked as a campaign, even if engagement was flat. 2 of 12 out: it didn't, even if those 2 did well.
- Never add campaigns together. One post can sit in two campaigns.
- One campaign is one sample. Don't say the strategy caused a result, or claim sales they don't track.
- Give a strategy two runs before dropping it. The first run had the thinnest context.
- Compare like with like: next time, change only the strategy.
- Low decision rate: the limit is review time, not the strategy. Suggest fewer posts a week.

## Closing it

- **On or paused:** offer to finish it: `set-content-campaign-status` with `action: "complete"`. One Bolta check. Final: it can't start again; its results stay.
- **Not started** (one I wrote): give the verdict and leave the status alone. It can't be finished from there.
- **Retire** (`action: "archive"`) only when asked. One check, final. Pause is usually what they meant.

## One next step

- It worked: "Run it again with the same strategy?" That is a new campaign with the same brief; there is no copy. If Bolta writes it, the accounts and Context step comes back unless Content defaults fill the accounts.
- It didn't: name one other strategy, using the week 1 signs in strategies.md: "Try Product Education next?"
- Drafts are still waiting: hand to `review`.

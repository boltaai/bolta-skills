---
name: results
description: >-
  See how your posts, accounts, Bolta routines and campaigns really did, read
  honestly, with one next step. Use when someone says how did it do, how are
  my posts doing, what's working, which post did best, how did last month go,
  is my Bolta routine working, or which campaign worked better.
---

## Done when

One honest read, in plain words: what went out, how it did, what can't be seen yet. Then exactly one next step.

## Know this

- **Window:** what the user said, else the last 30 days. Name it and the workspace in the first line.
- **Process before outcome.** First what was made, decided and went out: "12 drafts made. You decided 10. 9 went out." Then engagement. Everything written and every yes out: it worked as a campaign, even if engagement was flat. 2 of 12 out: it didn't, even if those 2 did well.
- **Decision rate:** drafts decided (yes, no or dropped) out of drafts made. Low: suggest fewer posts a week, not a new strategy.
- **Count per account.** Out on LinkedIn but failed on X still counts on LinkedIn: "went out on 2 of 3 accounts".
- **Never add campaigns together.** One post can sit in two; report each alone. Compare like with like: same weeks, mix and accounts.
- **One campaign is one sample.** Give a strategy two runs before dropping it. Never say a strategy caused a result, or claim sales nobody tracked.
- **Fresh posts:** metrics sync nightly. Zeros on posts under a day old mean "not synced yet": leave them out of rankings.
- **No publication record** (`has_publication_record: false`): missing data, not a flop. Leave those posts out and say how many.
- **Disconnected accounts** stop syncing. Call `get-connect-link` and say: "Instagram is disconnected: reconnect here <link>."
- **Nothing went out?** Say Bolta's own reason plainly. Nearly always: waiting for your yes.
- The "already shown, don't repeat" note is for other apps: give the numbers; never mention it.
- **One campaign:** verdict, then "Run it again with the same strategy?" if it worked, else "Try <another strategy> next?" Finishing it: `campaign`.
- Before quoting account or post numbers, read [references/reading-numbers.md](references/reading-numbers.md). For campaigns or a Bolta routine, read [references/campaigns-and-routines.md](references/campaigns-and-routines.md). If one won't open, carry on silently.

## Tools

- `list-workspaces`, `get-workspace`, `list-accounts`, `get-connect-link`: workspace, clock, accounts, reconnect link.
- `cross-platform-analytics`: followers and engagement by network.
- `list-account-insights`: each account, with growth and reconnect flags.
- `get-account-analytics`: one account, day by day.
- `list-workspace-posts`: posts that went out, with metrics.
- `list-content-campaigns`, `get-content-campaign`: find a campaign; its results.
- `list-content-campaign-posts`: its posts, and which are undecided.
- `list-routines`, `get-routine`, `list-routine-runs`: find a Bolta routine; its counts and runs.

## Hand off

`post`: more like the winner. `campaign`: finishing a campaign, running it again, or one that's stuck. `routine`: changing a Bolta routine, one that didn't run, or a weekly numbers report. `review`: drafts still waiting. `connect`: reconnecting. `fix`: a post that didn't go out.

## Always

- Follow the house rules in the `today` skill.
- End with exactly one next step, such as "Make 3 more like the winner?" (`post`).
- Only read: never start, finish or change a campaign or Bolta routine.
- Every number comes from this read: no benchmarks or guesses.

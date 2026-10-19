---
name: campaign
description: >-
  Plan, start, check or close a campaign: 1 to 4 weeks of posts about one
  thing, like a launch, sale or event, ending with a verdict. Use when someone
  says we launch on Nov 3, run a promo, a sale ending Friday, for 3 weeks,
  how did the campaign do, my campaign is doing nothing, or "done" after
  picking accounts.
---

## Done when

The plan got a yes and the campaign is filled one way. At the end: a verdict, one next step.

## Know this

- **Size it:** posts a week × weeks = drafts to review, plus what active Bolta routines and campaigns send each week. Over about 6, cut posts a week, not weeks. 1 to 4 weeks; a first one gets 2. Subject taken? Offer that one.
- **Strategy:** pick it from [references/strategies.md](references/strategies.md): dashboard name, a gloss. A launch is Problem / Solution, never Offer & Promotion.
- **Ask at most one thing:** a missing link or date (a price only for Offer & Promotion). No link: leave it out and say so.
- **One plan, then "Start it?"** Told to start or write them now? That's the yes: create it, show the plan.
  > **Campaign: New pricing** (not started)
  > - Strategy: Problem / Solution: a real frustration, then the fix.
  > - When: Oct 19 to Nov 8 (3 weeks; launch in week 3)
  > - Posts: 3 images + 1 carousel a week × 3 weeks = **12 drafts to review**
  > - Who writes: **Bolta, with images.** Or I write all 12 now, text only.
- **Fill it one way, never both** ([references/two-ways.md](references/two-ways.md)):
  - **Bolta writes it:** default for 2+ weeks or images. Its create reply lists accounts. None: `set-content-campaign-targets` ([references/targets.md](references/targets.md)) with `account_ids` (ask which only if several, none named); notes are the plan plus facts the user gave. Start on the yes (one Bolta check, uses credits). Tool missing: never ask which; `update-content-campaign` sets the brief and dates; accounts: "Pick them at bolta.ai/dashboard/campaigns/<id>, then say done." "Done" is the yes: read it again; accounts there, start it.
  - **I write it now:** 1 week, text only, or "show me all": up to 12 Drafts in one batch; poll the status for the real post ids (not the batch's), attach those, show every post. Never start it: Bolta would write a second set.
- **A page to read:** a `url` entry in `context_sources`, then `analyze-content-campaign-source` for each new source. Only read ones reach the writer: say which failed, and why.
- **`ends_on` is never null**, whatever the tool text says.
- **Resume, finish, retire** ask once; the last two are final.
- **The verdict**, once the end date passes: [references/verdict.md](references/verdict.md). **Nothing happened:** [references/why-nothing.md](references/why-nothing.md); nearly always waiting for your yes.

## Tools

- `get-workspace`, `list-accounts`, `get-voice-context`: clock, accounts, voice.
- `list-content-campaigns`, `get-content-campaign`: state, results.
- `create-content-campaign`, `update-content-campaign`: the brief.
- `set-content-campaign-targets`: accounts, weeks, notes, sources.
- `analyze-content-campaign-source`: read a source.
- `set-content-campaign-status`: start, pause, resume, finish, retire.
- `list-content-campaign-posts`, `add-posts-to-content-campaign`: its posts; adding mine.
- `list-workspace-posts`, `bulk-create-posts`, `bulk-create-status`: best posts; my drafts.
- `list-routines`, `update-routine`: load; steer.

## Hand off

`review`: deciding drafts. `routine`: no subject or end. `post`: one-offs. `results`: other numbers. `voice`: "not me". `connect`: accounts. `fix`: undo.

## Always

- Follow the house rules in the `today` skill.
- Never start a campaign that has no accounts, or one I filled.

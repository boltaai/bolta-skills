---
name: campaign
description: >-
  Plan, start, check or close a campaign: 1 to 4 weeks of posts about one
  thing, like a launch, sale or event, ending with a verdict. Use when someone
  says we launch on Nov 3, run a promo, a sale ending Friday, for the next 3
  weeks, how did the campaign do, or my campaign is doing nothing.
---

## Done when

The plan got a yes and the campaign is filled one way. At the end: a verdict, one next step.

## Know this

- **Campaign or Bolta routine?** Can they name the subject, the end, and want a verdict? Any no: `routine`.
- **Size it:** posts a week × weeks = drafts to review. Add drafts a week from active Bolta routines and campaigns; over about 6, cut this campaign's posts a week, not its weeks. 1 to 4 weeks; a first campaign gets 2. Subject taken? Offer that campaign instead, or to steer the Bolta routine elsewhere.
- **Strategy:** pick it from [references/strategies.md](references/strategies.md): dashboard name plus a gloss. A launch is Problem / Solution, never Offer & Promotion. "Behind the scenes" is a topic.
- **Ask at most one thing:** a missing link or date (a price only for Offer & Promotion). No link: leave it out and say so.
- **One plan, then "Start it?"**
  > **Campaign: New pricing** (not started)
  > - Strategy: Problem / Solution: a real frustration, then the fix. Best for launches.
  > - When: Oct 19 to Nov 8 (3 weeks; launch in week 3)
  > - Posts: 3 images + 1 carousel a week × 3 weeks = **12 drafts to review**
  > - Plan: week 1 the problem; week 2 the fix; week 3 what changes. Waitlist link in every post.
  > - Who writes: **Bolta, each week, with images.** It needs one Bolta screen to pick accounts. Or I write all 12 now, text only.
- **Fill it one way, never both** ([references/two-ways.md](references/two-ways.md)):
  - **Bolta writes it:** default for 2+ weeks or images. Starting uses credits (one Bolta check). Never start it with no accounts.
  - **I write it now:** 1 week, text only, or "show me all": up to 12 drafts saved into it. Never start it, or Bolta writes a second set.
- **`ends_on` is never null**, whatever the tool text says.
- **Week 1 looks off?** Wrong strategy or thin context: see strategies.md.
- **Pause** never asks. Resume, finish and retire ask once; the last two are final.
- **The verdict**, once the end date passes: [references/verdict.md](references/verdict.md). Never add campaigns together.
- **Nothing happened:** [references/why-nothing.md](references/why-nothing.md). Nearly always, it's waiting for your yes.

## Tools

- `get-workspace`, `list-accounts`, `get-voice-context`: clock, accounts, voice, website.
- `list-content-campaigns`, `get-content-campaign`: accounts, phase, errors, results.
- `create-content-campaign`, `update-content-campaign`: the brief, strategy, mix.
- `set-content-campaign-status`: start, pause, resume, finish, retire.
- `list-content-campaign-posts`, `add-posts-to-content-campaign`: its posts; adding mine.
- `list-workspace-posts`: their best posts.
- `bulk-create-posts`, `bulk-create-status`: save my drafts.
- `list-routines`, `update-routine`: load; steer a Bolta routine.

## Hand off

`review`: deciding drafts. `routine`: no subject or no end. `post`: one-off posts. `results`: accounts, posts, Bolta routines. `voice`: thin or "not me" drafts. `connect`: missing accounts. `fix`: undo, stop everything.

## Always

- Follow the house rules in the `today` skill.
- Never start a campaign that has no accounts, or one I filled.

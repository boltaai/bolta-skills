# Campaign

Plan, start, check or close a campaign: 1 to 4 weeks of posts about one thing, like a launch, sale or event, ending with a verdict. Use when someone says we launch on Nov 3, run a promo, a sale ending Friday, for 3 weeks, how did the campaign do, my campaign is doing nothing, or "done" after picking accounts.

## Done when

The plan got a yes and the campaign is filled one way. At the end: a verdict, one next step.

## Know this

- **Size it:** posts a week × weeks = drafts to review, plus what active Bolta routines and campaigns send each week. Over about 6, cut posts a week, not weeks (cap: 10). A first one gets 2 weeks.
- **Strategy:** always send one, from [strategies.md](campaign-strategies.md): dashboard name, a gloss. Guidance: a launch is Problem / Solution, not Offer & Promotion.
- **Ask at most one thing:** a missing link or date (a price only for Offer & Promotion). No link: leave it out and say so.
- **One plan, then "Start it?"** Where offered, `plan-campaign` makes the plan and `confirm-plan` saves it not started ([how-to.md](campaign-how-to.md), also for a first campaign). Told to start or write them now? That's the yes: create it, show the plan.
  > **Campaign: New pricing** (not started)
  > - Strategy: Problem / Solution: a real frustration, then the fix.
  > - When: Oct 19 to Nov 8 (3 weeks; launch in week 3)
  > - Posts: 3 images + 1 carousel a week × 3 weeks = **12 drafts to review**
  > - Who writes: **Bolta, with images.** Or I write all 12 now, text only.
- **Fill it one way, never both** ([two-ways.md](campaign-two-ways.md)):
  - **Bolta writes it:** default for 2+ weeks or images. Its create reply lists accounts. None: `set-content-campaign-targets` ([targets.md](campaign-targets.md)) with `account_ids` (ask which only if several, none named); `context_notes`: the plan plus the user's facts. Start on the yes (uses credits). Tool missing: `update-content-campaign` sets the brief and dates; accounts: "Pick them at bolta.ai/dashboard/campaigns/<id>, then say done." "Done" is the yes: read it again; accounts there, start it.
  - **I write it now:** 1 week, text only, or "show me all": up to 12 Drafts in one batch; attach the real post ids from the status (not the batch's), show every post. Never start it: Bolta would write a second set.
- **A page to read:** a `url` in `context_sources`, then `analyze-content-campaign-source` for each; only read ones reach the writer. Say which failed, and why.
- **Every setting:** the brief and dates [settings.md](campaign-settings.md); formats per network [settings-formats.md](campaign-settings-formats.md); start, pause, finish [settings-status.md](campaign-settings-status.md); page-only [settings-web.md](campaign-settings-web.md).
- **Video, blog, email, a team version, the Library:** [formats-and-team.md](campaign-formats-and-team.md). Say video costs more credits before the yes.
- **Pause, resume, finish, retire:** ask once. Stopping never unschedules posts ([settings-status.md](campaign-settings-status.md)).
- **Verdict** after the end date: [verdict.md](campaign-verdict.md). **Nothing happened:** [why-nothing.md](campaign-why-nothing.md); usually never started ([why-nothing-avoid.md](campaign-why-nothing-avoid.md)) or waiting for your yes.

## Tools

- `get-workspace`, `list-accounts`, `get-voice-context`.
- `list-content-campaigns`, `get-content-campaign`.
- `create-content-campaign`, `update-content-campaign`: brief.
- `set-content-campaign-targets`: accounts, weeks, notes, sources.
- `analyze-content-campaign-source`.
- `plan-campaign`, `revise-plan`, `confirm-plan`: Bolta's planner, where offered.
- `set-content-campaign-status`: `action` is activate (start), pause, resume, complete (finish) or archive (retire).
- `list-content-campaign-posts`, `add-posts-to-content-campaign`: its posts; adding mine.
- `list-workspace-posts`, `bulk-create-posts`, `bulk-create-status`: my drafts.
- `list-routines`: weekly load.

## Hand off

[review](review.md): deciding drafts. [routine](routine.md): no subject or end. [post](post.md): one-offs. [results](results.md): other numbers. [voice](voice.md): "not me". [connect](connect.md): accounts. [fix](fix.md): undo.

## Always

- Follow the house rules in the Bolta skill.
- Never start a campaign with no accounts when the workspace has some, or one I filled.

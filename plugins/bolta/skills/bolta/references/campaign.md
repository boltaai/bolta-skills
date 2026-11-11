# Campaign

Plan, start, check or close a campaign: 1 to 4 weeks of posts about one thing, like a launch, sale or event, ending with a verdict. Use for: we launch on Nov 3, a sale ending Friday, how did the campaign do, my campaign is doing nothing, "done" after picking accounts.

## Done when

The plan got a yes and the campaign is filled one way. At the end: a verdict, one next step.

## Know this

- **Size it:** posts a week × weeks = drafts to review, plus what active Bolta routines and campaigns send. Over about 6, cut posts a week, not weeks (Bolta's cap: 10 social a week). A first one gets 2 weeks. Subject taken? Offer that one. Campaign or routine, what fits which event: [choosing.md](campaign-choosing.md).
- **Strategy:** always send one, from [strategies.md](campaign-strategies.md): dashboard name, a gloss. Guidance: a launch is Problem / Solution; Offer & Promotion needs a real price and end date.
- **Dates:** `starts_on` today or later, a real `ends_on` (`null` is ignored; no open-ended campaign), the event in the last week.
- **Ask at most one thing:** a missing link, date or (Offer & Promotion) the offer. No link: leave it out, say so.
- **One plan, then "Start it?"** Where offered, `plan-campaign` plans and `confirm-plan` saves it not started ([how-to.md](campaign-how-to.md)). Told to start or write now? That's the yes: create, show the plan.
  > **Campaign: New pricing** (not started)
  > - Strategy: Problem / Solution: a real frustration, then the fix.
  > - When: Oct 19 to Nov 8 (3 weeks; launch in week 3)
  > - Posts: 3 images + 1 carousel a week × 3 weeks = **12 drafts to review**
  > - Who writes: **Bolta, with images.** Or I write 12 now, text only.
- **Fill it one way, never both** ([two-ways.md](campaign-two-ways.md)):
  - **Bolta writes it:** default for 2+ weeks or images. Its create reply lists accounts. None: `set-content-campaign-targets` ([targets.md](campaign-targets.md)) with `account_ids` (ask which only if several, none named) and `context_notes`: the plan, the user's facts. Start on the yes (one Bolta check, uses credits). Tool missing: never ask which accounts; hand off: "Pick them at bolta.ai/dashboard/campaigns/<id>, then say done." "Done" is the yes: read it again; accounts there, start.
  - **I write it now:** 1 week, text only, or "show me all": up to 12 Drafts in one batch; poll the status, attach its post ids (not the batch's), show each. Never start it: Bolta would write a second set.
- **A page to read:** a `url` in `context_sources`, then `analyze-content-campaign-source` for each; only read ones reach the writer. Say which failed.
- **Every setting:** [settings.md](campaign-settings.md) and the pages it links.
- **Video, blog, email, a team version, the Library:** [formats-and-team.md](campaign-formats-and-team.md). Say video costs more first.
- **Pause, resume, finish (`complete`), retire (`archive`):** ask once; the last two are final. Stopping never unschedules posts.
- **Verdict** after the end date: [verdict.md](campaign-verdict.md). **Nothing happened:** [why-nothing.md](campaign-why-nothing.md); usually never started ([avoid](campaign-why-nothing-avoid.md)) or waiting for your yes.

## Tools

- `get-workspace`, `list-accounts`, `get-voice-context`, `list-content-campaigns`, `get-content-campaign`.
- `create-content-campaign`, `update-content-campaign`: brief.
- `set-content-campaign-targets`, `analyze-content-campaign-source`: accounts, notes, sources.
- `plan-campaign`, `revise-plan`, `confirm-plan`: Bolta's planner, where offered.
- `set-content-campaign-status`: activate, pause, resume, complete, archive.
- `list-content-campaign-posts`, `add-posts-to-content-campaign`: its posts; adding mine.
- `list-workspace-posts`, `bulk-create-posts`, `bulk-create-status`: best posts; my drafts.
- `list-routines`, `update-routine`: load; making room.

## Hand off

[review](review.md), [routine](routine.md) (no end), [post](post.md), [results](results.md), [voice](voice.md), [connect](connect.md), [fix](fix.md) (undo).

## Always

- Follow the house rules in the Bolta skill.
- Never start a campaign with no accounts when the workspace has some, or one I filled.

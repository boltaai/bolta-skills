# Campaign

Plan, start, check or close a campaign: 1 to 4 weeks of posts about a launch, sale or event, ending with a verdict. Use for: we launch Nov 3, a sale ending Friday, how did it do, my campaign does nothing.

## Done when

The plan got a yes and the campaign is filled one way. At the end: a verdict, one next step.

## Know this

- **Size it:** posts a week × weeks = drafts to review, plus what active routines and campaigns send. Over about 6, cut posts a week, not weeks (cap: 10 social). A first one gets 2 weeks. Subject taken? Offer that one. Campaign or routine: [choosing.md](campaign-choosing.md).
- **Strategy:** always send one, from [strategies.md](campaign-strategies.md): dashboard name, a gloss. A launch is Problem / Solution; Offer & Promotion needs a real price and end date.
- **Dates:** `starts_on` today or later, a real `ends_on` (`null` is ignored), the event in the last week.
- **From what you know:** the chat plus what Bolta holds, one "Based on..." line, as `context` ([planner-context](routine-planner-context.md)). Never re-ask a given date.
- **Ask at most one thing:** a missing link, date or (Offer & Promotion) the offer. None named: ask which, and when.
- **One plan, then "Start it?"** `plan` (`kind: "campaign"`; load it with the other Bolta tools) plans it, in the same reply; `confirm-plan` saves it not started ([how-to.md](campaign-how-to.md)). By hand only without a `plan` tool. Told to start or write now? That's the yes: create, fill and start (or write) in one turn, show the plan.
  > **Campaign: New pricing** (not started)
  > - Strategy: Problem / Solution
  > - When: Oct 19 to Nov 8 (3 weeks; launch in week 3)
  > - Posts: 4 text posts a week × 3 weeks = **12 drafts to review**
  > - Who writes: **Bolta.** Or I write 12 now.
- **Fill it one way, never both** ([two-ways.md](campaign-two-ways.md)):
  - **Bolta writes it:** default for 2+ weeks. Send a text `content_mix`, `account_ids` (ask which only if several, none named) and `context_notes` (the plan, the user's facts) on the create (or `update-content-campaign`: [targets.md](campaign-targets.md)). Start on the yes (uses credits). Fields refused: "Pick accounts at bolta.ai/dashboard/campaigns/<id>, then say done." "Done" is the yes: accounts there, start.
  - **I write it now:** 1 week or "show me all": up to 12 Drafts in one batch; poll it, attach its post ids (not the batch's) at once, show each. Never start it: Bolta would write a second set.
- **A page to read:** a `url` in `context_sources`, then `analyze-content-campaign-source` each; only read ones reach the writer.
- **Every setting:** [settings.md](campaign-settings.md) and the pages it links.
- **Text, blog, email only from chat;** a plan with pictures or video: `revise-plan` to text. Instagram, TikTok, YouTube, Pinterest: pictures and video are added at bolta.ai/dashboard/campaigns/<id>. An existing mix: change it only when asked; keep web-set formats ([formats-and-team.md](campaign-formats-and-team.md); team version, Library).
- **Posting without a yes:** [no-approval](routine-no-approval.md).
- **Pause, resume, finish (`complete`), retire (`archive`):** ask once; the last two are final.
- **Verdict** after the end date: [verdict.md](campaign-verdict.md). **Nothing happened:** [why-nothing.md](campaign-why-nothing.md); usually never started ([avoid](campaign-why-nothing-avoid.md)) or awaiting a yes.

## Tools

- `list-workspaces`, `list-accounts`, `get-voice-context`, `list-content-campaigns`, `get-content-campaign`.
- `plan` (`kind: "campaign"`), `revise-plan`, `confirm-plan`: first.
- `update-content-campaign` (brief, accounts, notes, sources; `post_ids` alone attaches posts), `analyze-content-campaign-source`; `create-content-campaign` only without `plan`.
- `set-content-campaign-status`: activate, pause, resume, complete, archive.
- `list-workspace-posts` (`campaign_id`), `bulk-create-posts`, `list-routines`.

## Hand off

[review](review.md), [routine](routine.md), [post](post.md), [results](results.md), [connect](connect.md), [fix](fix.md).

## Always

- Follow the house rules in the Bolta skill.
- Never start a campaign with no accounts when the workspace has some, or one I filled.

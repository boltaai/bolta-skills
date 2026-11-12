# Campaign settings: the brief and the dates

Read when filling or changing a campaign's brief, or when the user asks what a setting does. Set on `create-content-campaign` or `update-content-campaign` (the dashboard shows the same fields). Accounts, notes, sources and voice: [targets.md](campaign-targets.md). Formats and posts per week: [settings-formats.md](campaign-settings-formats.md). Start, pause, finish: [settings-status.md](campaign-settings-status.md). Settings only the campaign page has: [settings-web.md](campaign-settings-web.md). "Guidance" below is marketing judgement, not a Bolta rule.

## What it's about

- **Name** (`name`, required, up to 255 characters): a label for lists and the dashboard. The writer sees it only as "Campaign: X", and uses it as the goal only when the theme is blank. Pitfall: putting the subject only in the name.
- **Theme** (`theme`, up to 255): **the writer's goal sentence** every week, and the subject of any blog article. Put the real subject here: "Our new pricing: three plans, one table", not "Q4 push". Default: blank (the web drafts one).
- **Audience** (`audience`, free text): added as "Who it is for". Use a real group ("small agencies choosing a plan"). Not "everyone".
- **Strategy** (`strategy_key`): the stance every post takes: `problem_solution`, `offer_promotion`, `product_education`, `thought_leadership`, `lifestyle`, `quick_tips` ([strategies.md](campaign-strategies.md)). Anything else is refused. Always send one. A new campaign sent no strategy, no mix and with no saved Content defaults gets Problem / Solution; with a mix or Content defaults it stays blank, and a blank strategy means no angle reaches the writer. Changing it later steers only weeks not written yet; the mix stays.

## The call to action

- **CTA text** (`cta_text`, up to 120 characters): **used word for word** in posts and articles. Write it exactly as it should read ("Book a seat", not "push signups"). Emails get it only as a note.
- **Link** (`cta_url`, a full `https://` address, up to 500): only one the user gave; add `https://` to a bare link. Never take one from a page you read, never invent one. No link: leave it out and say so. Bolta tags it so the user's own analytics can see campaign clicks; Bolta reports no clicks.

## Dates and length

- **Start** (`starts_on`, `YYYY-MM-DD`): the weekly rhythm counts from it, and **each week starts on that weekday**. No default here: left out, the campaign is undated and Bolta writes once when started, with no weekly rhythm. Always send one. Guidance: the next Monday, so weeks run Monday to Sunday. Bolta's planner assumes tomorrow when no date is said, and says so.
- **Length**: 1 to 4 weeks. Send `ends_on` (= start + 7 × weeks − 1 day) on create or update, or `duration_weeks` on either call, never both in one call. Leaving the end out means 1 week; more than 4 weeks is refused. **`ends_on: null` is ignored, not refused**: the campaign keeps its length. There is no open-ended campaign.
- An event or launch goes in the **last week**: start = the event's weekday minus 2 or 3 weeks.
- **A start in the past:** weeks already over are skipped, never written; the current week is written at once. Move the start forward first, or say what is skipped.
- Guidance: a first campaign 2 weeks; a launch 3; an offer 1-2, never past its end; thought leadership 4 ([choosing.md](campaign-choosing.md)). Longer arcs are back-to-back campaigns.

## Always

- Send `strategy_key`, `theme` and `starts_on` on every create.
- Never invent a link, price, date or deadline.
- Follow the house rules in the Bolta skill.

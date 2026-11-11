# Campaign settings only the campaign page has

Read when the user wants something no call can set: a tone, image quality, video style, a post time, a format on one account or weekday. Say what it does, then send them to bolta.ai/dashboard/campaigns/<id>. Saving these writes nothing and costs nothing; edits reach weeks not written yet.

## Set once at creation, through Bolta's planner

Where `plan-campaign` is offered, it sets these from the user's words when the campaign is made; afterwards only the page changes them:

- **Tone**: educational, bold, insightful or conversational, inside the voice.
- **Carousel style**: 2 to 10 slides, a look (auto, bold, minimal, editorial, photographic), portrait or square, one consistent brand look or slides that chain.
- **Writing extras**: themes and story sources for posts, research depth and source pages for articles, hashtag level, a product to mention.

## Context Settings (campaign page)

- **Image quality**: regular or pro. Pro looks better and costs more. Carousels ignore it.
- **Video style**: UGC (creator-style) or branded. **Video length**: 12 or 20 seconds (default 20).
- **Use about your business**: on by default. Off suits a one-off event or a sub-brand the saved profile would pull the wrong way.
- **Sources**: the campaign's own only, or the brand's documents too.
- **Your own images** (uploaded in the create dialog): used first, generated images fill the rest. Suits brands with real photos.
- **Media scope** and the **cover** do nothing to the posts. Never tell the user they limit media.

## Schedule row

- **Post time** and **timezone**: every new draft gets that clock time, keeping its date. It **overrides times set per post**, so suggest it only when the user wants one fixed time. Timezone alone does nothing.

## Content per week

- **Accounts and weekdays per format** ("carousels on LinkedIn on Tuesdays, shorts on TikTok"). No call sets them; a mix sent later wipes them.

## Post prompts

- Each planned post of a week not yet written: its topic, format, accounts, time and a reference image. Add one for a post that must land on a date (launch day, last day of an offer). Skipping every post empties that week. A written post is fixed.
- Opening the campaign page lays out every unwritten week; later mix changes miss those weeks.

## Content defaults (Campaigns page, whole brand)

- **Content plan**: the mix a new campaign starts with when it is sent none.
- **Crosspost to the same accounts**: on, a new campaign gets every account that can post its formats. Offer it once after a hand-off for accounts.
- **Review time before posting**: 1 to 4 days, default 2 ([settings-status.md](campaign-settings-status.md)).
- **Strategy "Make default"** only preselects the web dialog; it does not change what Bolta writes for a campaign made here.

## The web create dialog

"Start campaign" makes it and starts it in one press. Its sources are **not read yet**: until someone presses Read on the campaign page, or you run `analyze-content-campaign-source` for each, the writer ignores them. Check a web-made campaign's `context_sources`; any not `ready` need reading.

## Always

- Never claim to have set something only the page sets.
- Follow the house rules in the Bolta skill.

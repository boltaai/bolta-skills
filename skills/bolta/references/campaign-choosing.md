# Campaign, routine or post, and what fits which event

Read when deciding what to set up for something dated, or when the subject may already be covered. "Guidance" is marketing judgement, not a Bolta rule.

## Which kind of work

- **One thing, now:** a post ([post](post.md)).
- **Repeats with no end** ("every week", "keep us posting"): a Bolta routine ([routine](routine.md)).
- **One thing that ends** (a launch, a sale, an event, "for 3 weeks", "by Nov 3"): a campaign. Never a routine, never a batch of one-off posts.
- **Both is normal:** routines keep the brand present; one campaign sits on top. Count both in the weekly load.
- **Longer than 4 weeks:** back-to-back campaigns, each with a verdict.
- Unclear, ask once: "Should this keep going with no end, or is it about one thing that ends?"

## Subject taken?

Read `list-content-campaigns` before planning. One already covers this subject and is not started, on or paused: offer that one ("You already have Spring launch, not started. Use it?") and change its brief with `update-content-campaign`. A finished one can't start again: make a new one.

## What fits which event (guidance)

| Event | Strategy | Weeks | Dates | Needs |
|-|-|-|-|-|
| Launch | Problem / Solution; Product Education when people know the problem, not the product | 3 | Launch day in the last week | The launch page as a source |
| Sale or offer | Offer & Promotion | 1-2 | Ends on the offer's last day | The real offer and end date: ask, never fill in |
| Webinar or event | Problem / Solution | 2 | Ends on the event day | The sign-up link |
| Pricing change | Problem / Solution; Product Education to explain plans | 2-3 | The change in the last week | The real prices |
| Building authority | Thought Leadership | 4 | Any Monday | Real positions in the notes |
| New to posting | Quick Tips or Product Education | 2 | Any Monday | One network if unsure |

Strategies and their mixes: [strategies.md](campaign-strategies.md), [playbooks.md](campaign-strategies-playbooks.md). Formats per network: [settings-formats.md](campaign-settings-formats.md).

## Size it to review time

- A campaign's drafts a week = the total of its mix. Add what already comes: each active routine's `count` × its runs a week (`list-routines`), other active campaigns' mixes, and what waits undecided (`list-inbox-items`).
- Guidance: about 6 a week is what one person decides. Over that, cut posts a week, not weeks: "That's 9 drafts a week with your routines. Make the campaign 2 a week?"
- 10 or more already waiting: name the count and offer to go through them first. A date that can't wait: plan it small, 2-3 a week.
- **Making room:** offer, and on a yes lower a routine's `count` with `update-routine` or pause it for the campaign's weeks ([looking after](routine-looking-after.md)). Nothing restores it by itself; say so.

## Days inside a week

Bolta spreads a week's posts over Monday to Friday, or the days in the brand's posting schedule. A post that must land on one day (launch day, a Saturday): the user pins it under Post prompts on the campaign page ([settings-web.md](campaign-settings-web.md)); no call does. So notes carry dates ("the sale runs Nov 27 to Nov 30"), never "today" or "3 days left".

## Always

- Check for an existing campaign on the subject before making one.
- Say the weekly total, with routines, before the yes.
- Follow the house rules in the Bolta skill.

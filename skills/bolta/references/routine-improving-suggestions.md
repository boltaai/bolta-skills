# Bolta's suggestions for the brand

Read after [routine-improving.md](routine-improving.md) when the user asks what Bolta suggests, or the same complaint keeps coming back. These are brand-wide; a single routine's weekly recommendations are a different list (`list-suggestions` with `kind: "routine"`).

## What they are

`list-suggestions` with `kind: "brand"` turns approvals, edits and rejections into one change each. Bolta finds them itself, shortly after review decisions, and keeps at most 2 open. Examples: pause a routine whose last 3 decided drafts were all no; post less often; move a routine's time to when drafts get moved to; add a phrase the user keeps adding to its brief; carousels of the brand's own photos; only their own photos; a seasonal campaign; reuse best posts. Show its title, reason and every change it lists: accepting can change a voice or schedule, switch a routine on or off, or start a campaign. Only an owner or admin can decide (`can_decide`). On a yes: `decide-suggestion` with its `suggestion_id` and `decision: "accept"`; `decline` turns it down; `undo` works for 7 days.

## Deciding one

| `decision` | Does | When |
|-|-|-|
| `accept` | Makes every change listed | Only after the user saw each change and said yes |
| `decline` | Turns it down | They said no |
| `undo` | Reverses an accepted one | Within 7 days, while what it changed still exists |

- Never accept to "try it": a suggestion can switch a routine on or start a campaign, which leads to posts and uses credits.
- `can_decide` false: say "Only the brand's owner or an admin can accept this", and show it anyway.
- After accepting, read the routine back (`get-routine`) and say what changed.

## Always

- Show the title, reason and every change before the yes.
- One suggestion per yes; never accept on your own.

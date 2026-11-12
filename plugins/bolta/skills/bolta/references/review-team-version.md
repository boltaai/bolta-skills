# A team version: one idea, a post per person

One idea written as one post for each person or function (2 to 6), each in that person's voice, for the account their voice posts from, saved together as one group on the review list. Call it a team version, never a cascade. Asks: "Have David, Maria and Procurement each post about the new warehouse", "everyone shares the launch in their own words". Worked: [team-version](../examples/team-version.json). Campaign view of the same: [campaign-formats-and-team.md](campaign-formats-and-team.md).

## Before planning

- Each person needs their own voice with their account ([voice-brand-and-learning.md](voice-brand-and-learning.md)). A function such as Procurement, or a name the user says should use the brand voice, writes in the brand voice.
- The idea is the user's words, a sentence or two, at most 600 characters. Facts, numbers and names in the drafts come only from it: ask for the date or number rather than let Bolta guess.

## Steps

1. `plan-team-posts` with `idea` and `participants`: only the people and functions the user named, such as `[{"name": "David"}, {"name": "Procurement"}]`, adding `voice_profile_id` or `account_id` when known. "Everyone" with no names: `count` (2 to 6) of the brand's person voices; the result lists who was left out. Saves a plan only: nothing written, charged or scheduled.
2. Show the plan: per row who, voice, account, angle. A row Bolta couldn't place comes back unresolved with the choices: a name matching several voices or none, a voice on several accounts, or no account. Ask, never choose.
3. Settle it with `update-team-post-plan(cascade_id, revision, change, remove, add)`, passing the `revision` the user saw and the row's `slot_id`. A changed plan refuses the call and returns the current one: show it again. One row per voice: the same voice can't take two rows, so a person on LinkedIn and X gets one version here. One per account: ask in Bolta's own chat.
4. On a yes to the plan: `generate-team-post-drafts(cascade_id, revision)`. Drafts only; each costs credits only when approved ([review-credits.md](review-credits.md)). It returns before anything is written.
5. `get-team-post-plan(cascade_id)` until every row is saved, held back (its account isn't connected) or failed with a reason. Say written only for saved rows. Only the person who planned it can read it; a teammate's id comes back not found.
6. The drafts wait together on the review list: the yes move ([review](review.md)). Each goes out from its own person's account.

## Refusals

| Refusal | Do |
|-|-|
| `no_account` | No account can take the text: connect one ([connect](connect.md)). |
| `bad_participants`, `bad_count` | 2 to 6 people, each a name or a voice. |
| `idea_too_long` | Shorten it to 600 characters with the user. |
| `stale_revision` | Show the current plan, ask again. |
| `already_started` | It was written already; `get-team-post-plan` shows the drafts. |
| `expired` | Propose it again. |

## Not on this app

No `plan-team-posts` here: "Team versions are planned in Bolta's own chat. Ask it for a post about <idea> for <names>: bolta.ai/dashboard/hub." No `list-workspace-members` either: use the names the user gives. Putting the idea in the employee Library ("make it mine") is only in Bolta's chat.

## Always

- Follow the house rules in the Bolta skill.
- Get a yes on the plan before `generate-team-post-drafts`, and never add a person or function the user didn't name.
- Never say a version is written until `get-team-post-plan` shows it saved.

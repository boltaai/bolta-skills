# Client approval: brand settings that change a yes

Three settings decide whether a post waits, and for whom. Read with [review-client-approval.md](review-client-approval.md).

## The settings

- **Client sign-off required**: nothing on the brand is approved, scheduled or posted without the client's yes. Only the organization owner (the brand owner if there is no organization) changes it, in the brand's settings in Bolta. How it behaves once on: [review-client-signoff.md](review-client-signoff.md). The `list-workspaces` row doesn't show it; `get-post` `client_signoff.required` does.
- **Review mode**: every post waits for a team yes before it can be scheduled or posted.
- **A routine's "ask me first"**: its drafts wait for a yes. A Bolta routine can instead send each run's drafts straight to the client, with no team pass; their yes takes the next open posting time. Setup: [routine-outputs.md](routine-outputs.md).

## What to say

- Sign-off required and the user asks to approve: "This brand needs the client's yes first. I can send it to <name> on your yes" ([send to a person](review-client-send.md)).
- Routine drafts going straight to the client: "These reach the client before anyone on the team sees them."

## Always

- Follow the house rules in the Bolta skill.
- Changing the sign-off setting is done in Bolta, never from here: [bolta.ai/dashboard/approvals](https://bolta.ai/dashboard/approvals) for sending, the brand's settings for the switch.

# People and roles

Who can do what in an organization and on a brand, and how to name a teammate. None of it is set from here: say where it lives and who can do it. Back to [team-and-integrations](connect-team-and-integrations.md).

## Organization roles

- **Owner** and **admin**: invite and remove people, set their organization role and give them brands, at Settings > Organization > Members (bolta.ai/dashboard/organization). They reach every brand in the organization.
- **Member**: sees the organization and its team list, and only the brands they were given.
- `list-workspaces` shows each brand with the organization and your role in it. An invitation lasts 7 days.

## Brand roles

| Role | Can |
|-|-|
| owner, admin | everything on the brand: write, approve, turn down, post now, connect accounts, invite, change settings |
| creator | write, change and delete drafts, send for review, schedule when review mode allows it; approve Bolta's drafts and posts they are a named reviewer on |
| viewer | read |
| reviewer | a client: decides client requests sent to them, nothing else; no seat, no AI app |

- There is no "editor": the writing role is creator.
- **Who approves, in Bolta:** owners and admins, any post. Creators, Bolta's drafts (routine and agent work) and any post where they are a named reviewer. Client reviewers, the posts sent to them in a client request (approve, ask for changes or dismiss), never one they sent. Viewers don't.
- A per-person setting in People & access can give or take away approving. Taken away, it holds even an admin, never the brand owner.
- Nobody approves their own post while someone else can ([own post](review-more-decisions.md)); Bolta's drafts are nobody's own.
- **Through this app** (`approve-many-posts`, `reject-post`, `publish-post`): the same rule as in Bolta, per-person settings included; a viewer never. The connection needs write access. Own post, review mode, Safe Mode, client sign-off and the rule that posts from this app wait for a person's yes still apply. On a refusal, give Bolta's sentence and say who can.
- A creator can be sent a client request and decide it for the client ([client approval](review-client-approval.md)).
- An owner or admin can grant or deny single permissions for one person on one brand. So nothing here reads what someone can do right now: never state it from the role alone. A refusal names the role or access that's missing; say that.

## Client reviewers

- Invited from the brand's People & access; they take no paid seat and can hold no key or AI app.
- They see every client request on that brand and its schedule, and decide only the ones sent to them ([client details](review-client-details.md)).

## A teammate's name

- `list-workspace-members`: each person's id, name and role on the brand, no email. Use it to turn "Priya" into the id a Bolta routine's reviewers take (`default_reviewer_ids`).
- Client reviewers are never listed: ask the user who the client is.
- Not on this app: ask for the name and send the user to the routine's page in Bolta to pick the reviewer.

## Always

- Follow the house rules in the Bolta skill.
- Never promise what someone may do from their role; a refusal names the reason.
- Never claim a person was invited, removed or given a role from here.

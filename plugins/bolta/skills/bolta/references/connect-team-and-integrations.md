# Team, clients and integrations

None of this is set from here. Say where it lives in Bolta and who can do it.

## People and roles

Who can do what, organization and brand roles, client reviewers and turning a name into a teammate: [people and roles](connect-people-and-roles.md).

## Client connect-only links

- An owner or admin sends one from the brand's People & access: one email per link, 7 days by default, 30 at most. A new link to the same email cancels the old one.
- The client signs in with that email, connects their accounts to that brand only and gets no role. The link can go out with a brand invite, a reviewer invite for example.
- `get-connect-link` is NOT this: it opens the user's own connect page. Never send it to a client.

## Integrations

- **Dropbox:** one folder, read-only, connected by an owner or admin at bolta.ai/dashboard/hub?settings=integrations&integration=dropbox. Its files become the brand's source material (knowledge base and media library), and routines and campaigns check it for new files when they plan.
- **Google Drive and WordPress** also connect from Settings > Integrations.
- **GitHub, HubSpot and Square** connect there too, each feeding Bolta routines: GitHub a post per merged pull request, HubSpot a win post per closed deal, Square service spotlights, open slots and weekly bookings ([routine templates](routine-templates-special-cases.md)).
- **Bolta in Slack** (Settings > Integrations): failure alerts, review pings and a direct-message chat with Bolta. Approving in Slack doesn't train the voice and doesn't count as a client's sign-off. A routine that reads a Slack channel isn't available yet. This is separate from your AI app's own Slack connection: never mix them up.

## Credits and billing

Credits and the spending limit: bolta.ai/dashboard/settings/billing. Nothing here reads the balance, so never quote one.

## Clock and review mode

- The brand's clock changes only in the brand's Settings > Overview: bolta.ai/dashboard/settings/brand.
- Review mode ("Safe Mode" in the brand's Settings > Rules, said once): everything beyond a draft waits for a yes, and nothing posts right away. Only Bolta Settings turns it off; never suggest that to get past a refusal.

## "Is everything set up?"

One read, then four lines per brand: brand and clock; review mode; accounts, connected, disconnected or added without connecting, with links; account groups. Voice: hand to [voice](voice.md), or [start](start.md) if there is none. A Bolta save blocked by a hook error naming Git Bash: "Install Git for Windows (git-scm.com/downloads/win), then restart this app."

## Bolta's own chat

Inviting approvers, choosing posting days and filling the Library from a deck can also be done in Bolta's own chat: ask it "what's left to set up". Posting days there shape the days the chat's plans and team plans pick; routines and campaigns keep their own schedules.

## Always

- Follow the house rules in the Bolta skill.
- Name the page and the role that can do it; never claim a change was made.
- Read `get-my-capabilities` before saying what someone may do.
- Never send `get-connect-link` to a client.

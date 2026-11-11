# Campaign settings: start, pause, finish, and when drafts land

Read before changing a campaign's status, or when the user asks when drafts come or why posts still go out. One call: `set-content-campaign-status` with `campaign_id` and `action`. Read `get-content-campaign` first: its `status` decides which moves are legal, and a refused move names the legal ones.

## The five actions

- **`activate`** (start): from not started (a paused one: `resume`). **This is what makes Bolta write**; creating a campaign never does. Needs its own yes, after the user saw the plan. One Bolta check; uses credits when a week is due. Accounts first: with accounts in the brand and none on the campaign, the reply is an error (`no_accounts`) yet the campaign is on and makes nothing (`needs_accounts`) until accounts are set.
- **`pause`**: stops new drafts. Reversible. What the user nearly always means by "stop".
- **`resume`**: from paused. Bolta writes every week still owed, on its usual days; weeks already over are skipped. If the campaign's only account was removed, set one first or it is refused.
- **`complete`** (finish): from on or paused. Final: it can't start again; results stay.
- **`archive`** (retire): from any status. Final, hidden from the list, nothing deleted. Only when asked.

## Stopping is not unscheduling

Pause, finish and retire stop **new** drafts only. Posts already approved and scheduled **still go out**. On "stop the campaign": pause it, then `list-workspace-posts` with `campaign_id`, show the ones still to go out (`status`, scheduled time), and offer to move or delete them one by one ([fix](fix.md) for undo). Undecided drafts just wait; say so.

## When drafts land

- Each week is written `review_lead_days` before it starts: **2 days** by default, 1 to 4, one setting for the whole brand, changed only on the Campaigns page (Content defaults). Changing it moves every running campaign.
- Writing starts around **midnight UTC** that day: in the Americas, the evening before. Say "around Saturday" in the workspace clock, never an exact minute.
- Weeks start on the start date's weekday. Activation inside the lead window writes week 1 at once.
- Read `generation` in the activate reply: `started` true means drafts in a few minutes; `scheduled_for` is when; `error_code` gets a plain reason. "Your plan doesn't include campaigns yet" means a paid plan is needed.
- Campaign drafts always wait for a yes, whatever the brand's review setting. A draft nobody decides expires 30 days after its planned time.

## It ends by itself

An on campaign finishes on its own shortly after its end date (`status_reason` reads `window_ended`). A paused or undated one never does. So read `status` before offering to finish one.

## Only on the campaign page

- **Generate now**: writes the next week early (uses credits). **Generate again**: retries a failed week. No call does either; send the user to bolta.ai/dashboard/campaigns/<id>.
- **Duplicate** (copy icon on the cover): a new not-started copy with the same brief, accounts, plan and settings. Its sources come back **unread**: after a duplicate, run `analyze-content-campaign-source` on each.
- **Remove a post** from a campaign: calendar campaign picker only.

## Always

- Ask a separate yes before `activate`, `complete` or `archive`.
- On "stop", say scheduled posts still go out and offer to move or delete them.
- Follow the house rules in the Bolta skill.

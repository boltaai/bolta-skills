# Finding what's waiting

Read when building the numbered list. Run all reads at once; reuse the workspace, accounts and voice you already have.

## The reads

- `list-inbox-items(source="team", status="pending", limit=100)`. Page with `offset` while `has_more` is true. Team rows hold posts sent for review by the user or their team, and every draft a Bolta routine or campaign wrote. Those drafts are already waiting: never send them for review again.
- The totals (`total_team`, `total_recurring`, `total_hunter`, `total_report`) count the whole workspace whatever `source` you pass. Use them, not the page length.
- `total_recurring` above 0: also `list-inbox-items(source="recurring")`. These are legacy rows from older automations, decided with their own calls (see [read-back.md](review-read-back.md)). Never look here for Bolta routine drafts.
- `total_hunter` above 0: one line, "Also 3 reply drafts", and leave them to [replies](replies.md). Reports: mention the count only.
- "Waiting on me": `list-reviews(reviewer_id="me")`.
- `list-workspace-posts(status="draft", sort_by="updated_at")`: drafts never sent for review. Skip any whose id is already a team row (routine and campaign drafts are drafts too). List the ones saved in this conversation; give older ones as a count and offer them.

## Grouping

Group rows under routine, campaign, Library, one idea in N versions, or saved by you or me: see [grouping](review-finding-drafts-grouping.md).

## What each item shows

- Number, account (`platform_info`: network and name), the full text, and media links (`media_urls`).
- Full text comes from `content_full`; `content_preview` stops at 500 characters. `get-post` gives media and accounts when the row lacks them.
- `notes_for_reviewer` and the assigned reviewers' names (`assigned_reviewers`), when set.
- `expires_at` set: "expires Nov 30". Empty does not mean never: drafts with no time expire after 30 days with no activity.
- A planned time only when it is still ahead, in the workspace clock: "Wed Oct 21, 9:00 am (New York)". If you show one, a plain yes keeps it (`set_fixed_time`).
- TikTok or YouTube with no video, Instagram or Pinterest with no image or video: flag it now. Approval here works, then publishing fails.
- A post dropped earlier in this conversation can still show up as waiting. Leave it out and don't count it.

## Example

> **Acme** · 5 waiting for your yes
>
> **From Bolta routine "Weekly LinkedIn"**
> 1. LinkedIn (Jane): "Most hiring advice skips the first 90 days…" (full text)
> 2. LinkedIn (Jane): "We stopped asking for cover letters…"
>
> **From campaign "New pricing"**
> 3. X (@acme): "Paying for seats nobody uses?…"
>
> **Saved by you or me**
> 4. LinkedIn (Jane), planned Thu Oct 22, 12:00 pm (New York): "…"
> 5. X (@acme): "…"
>
> Decide in one line, like "1, 3, 4 yes · 2 shorter · 5 drop". Bolta picks the times from your posting schedule unless you name one.

That last line holds for drafts you, a Bolta routine, a campaign or Bolta's chat wrote. A post typed in Bolta's own composer with review mode on is approved without a time, and Library posts never get one: see [times Bolta picks](review-times-auto.md).

Nothing waiting: say so in one line, add the next scheduled post if there is one, then one next step.

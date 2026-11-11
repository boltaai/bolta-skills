# Finding what's waiting

Read when building the numbered list. Run all reads at once; reuse the workspace, accounts and voice you already have.

**8 or more in `total_team` plus `total_recurring`, and a clearing-house agent you can start:** hand it the first pass ([review](review.md)); it does these reads.

## The reads

- `list-inbox-items(source="team", status="pending", limit=100)`. Page with `offset` while `has_more` is true. Team rows hold posts sent for review by the user or their team, and every draft a Bolta routine or campaign wrote. Those drafts are already waiting: never send them for review again.
- The totals (`total_team`, `total_recurring`, `total_hunter`, `total_report`) count the whole workspace whatever `source` you pass. Use them, not the page length.
- `total_recurring` above 0: also `list-inbox-items(source="recurring")`. These are legacy rows from older automations, decided with their own calls (see [read-back.md](review-read-back.md)). Never look here for Bolta routine drafts.
- `total_hunter` above 0: one line, "Also 3 reply drafts", and leave them to [replies](replies.md). Reports: mention the count only.
- Any team row with a `workflow_run_id`: in the same pass, the routine and campaign reads in [grouping](review-finding-drafts-grouping.md). They name the groups: never show such a row as just "written by Bolta".
- "Waiting on me": `list-inbox-items(source="review_status", reviewer_id="me")`.
- `list-workspace-posts(status="draft", sort_by="updated_at")`: drafts never sent for review. Skip any whose id is already a team row (routine and campaign drafts are drafts too). List the ones saved in this conversation; give older ones as a count and offer them.

## Grouping

Group rows under **From Bolta routine "<name>"**, **From campaign "<name>"**, Library, one idea in N versions, or saved by you or me. How each row is matched: [grouping](review-finding-drafts-grouping.md).

## What each item shows

- Number, account (`platform_info`: network and name), the full text, and media links (`media_urls`).
- Full text comes from `content_full`; `content_preview` stops at 500 characters. `get-post` gives media and accounts when the row lacks them.
- `notes_for_reviewer` and the assigned reviewers' names (`assigned_reviewers`), when set.
- `expires_at` set: "expires Nov 30". Empty does not mean never: drafts with no time expire after 30 days with no activity.
- A planned time only when it is still ahead, in the workspace clock: "Wed Oct 21, 9:00 am (New York)". If you show one, a plain yes keeps it (`set_fixed_time`).
- TikTok or YouTube with no video, Instagram or Pinterest with no image or video: flag it now. Approval here works, then publishing fails.
- A post dropped earlier in this conversation can still show up as waiting. Leave it out and don't count it.

## Example

The numbered list to show, and what to say when nothing waits: [the list to show](review-finding-drafts-example.md).

## Always

- Follow the house rules in the Bolta skill.

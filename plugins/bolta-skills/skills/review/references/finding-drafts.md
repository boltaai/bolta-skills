# Finding what's waiting

Read when building the numbered list. All reads at once; reuse the workspace, accounts and voice you already have.

## The reads

- `list-inbox-items(source="team", status="pending", limit=100)`. Page with `offset` while `has_more` is true. Team rows hold posts sent for review by the user or their team, and every draft a Bolta routine or campaign wrote. Those drafts are already waiting: never send them for review again.
- The totals (`total_team`, `total_recurring`, `total_hunter`, `total_report`) count the whole workspace whatever `source` you pass. Use them, not the page length.
- `total_recurring` above 0: also `list-inbox-items(source="recurring")`. These are legacy rows from older automations, decided with their own calls (see read-back.md). Never look here for Bolta routine drafts.
- `total_hunter` above 0: one line, "Also 3 reply drafts", and leave them to `replies`. Reports: mention the count only.
- `list-workspace-posts(status="draft", sort_by="updated_at")`: drafts never sent for review. Skip any whose id is already a team row (routine and campaign drafts are drafts too). List the ones saved in this conversation; give older ones as a count and offer them.

## Grouping

- **From Bolta routine "X":** only if some row has a `workflow_run_id`. `list-routines(status="active,paused")`, then `list-routine-runs` for each. A row whose `workflow_run_id` equals one of that routine's run ids belongs to it. Runs carry no post ids, so this match is the only link.
- **From campaign "Y":** `list-content-campaigns(status="draft,scheduled,active,paused")`; for each with `posts_count` above 0, `list-content-campaign-posts`. A row whose `post_id` is in that list belongs to it. That call ignores its status and limit filters, so filter yourself (`has_pending_review`).
- **Saved by you or me:** everything else (I is Claude). Use a teammate's name from `post_creator` when it isn't the user. A leftover row with a `workflow_run_id` is "from Bolta".

## What each item shows

- Number, account (`platform_info`: network and name), the full text, and media links.
- Full text comes from `content_full`; `content_preview` stops at 500 characters. `get-post` gives media and accounts when the row lacks them.
- A planned time only when it is still ahead, in the workspace clock: "Wed Oct 21, 9:00 am (New York)". If you show one, a plain yes keeps it (`set_fixed_time`).
- Instagram, TikTok, YouTube or Pinterest with no media: flag it now. Approval works, then publishing fails.
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

Nothing waiting: say so in one line, add the next scheduled post if there is one, then one next step.

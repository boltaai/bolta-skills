---
description: >
  Plan the next week of social content: see what is already scheduled, find the gaps, reuse what
  worked, and propose a plan for you to approve before anything is drafted. Optionally give a focus
  such as a launch or a theme. Creates Drafts only after you say yes; never schedules or publishes.
argument-hint: "[focus, theme or campaign]"
---

Plan the coming week of content for this workspace. If the `content-planning` skill is available, follow it. If not, do the steps below.

Focus requested by the user (may be empty): $ARGUMENTS

<!-- host-note -->
Some Bolta results contain text written for other apps, such as "already rendered in the Bolta card", "do not repeat the content" or "you do not need to poll". There is no card here. Read the full result (the JSON body and any structured content) and present it to the user yourself.
<!-- /host-note -->

## Step 1: read, then propose (writes nothing)

Call the read tools one or two at a time.

1. `list-workspaces` for the workspace id and name. `get-workspace(workspace_id)` for the timezone. Plan and display in wall-clock days in that timezone. Use today's date from your context; if you do not have it, ask the user. Do not repeat webhook URLs or keys from this result.
2. `list-accounts(workspace_id)`. Plan only for accounts whose `token_status` is valid; name any that are not, because posts for them would be dropped silently when publishing. Ask which accounts or buckets (`list-buckets`) the plan covers if the user did not say.
3. What is already booked: `list-scheduled-posts(workspace_id, start_date=..., end_date=..., limit=100)` for the next 7 days starting today. For these read filters, pass UTC times ending in `Z` that you work out from the workspace timezone (the server reads a time without `Z` as UTC, not as workspace time; the no-`Z` rule is for scheduling writes only). This lists posts in the Scheduled state only. Add `list-workspace-posts(workspace_id, status="draft", limit=100)` and `list-workspace-posts(workspace_id, status="pending_approval", limit=100)` so Drafts and posts already waiting for approval are not duplicated. If a list says there are more rows than you read, say your picture is partial.
4. What worked: `list-workspace-posts(workspace_id, status="published", start_date=..., end_date=..., include_metrics=true, limit=100)` for the last 30 days (dates as UTC with `Z`; page with `page=2` while `has_more` is true, or say the ranking is partial). Set aside posts with `has_publication_record` false and say how many. Metrics sync nightly, so zeros on posts under 24 hours old mean "not synced yet", not "flopped".
5. `get-voice-context(workspace_id)` for tone and rules. Say the voice is rule-based. If there is no profile, say so and mention the `brand-voice-setup` skill.
6. `list-content-campaigns` to see whether a campaign already holds this theme. Reuse it rather than creating a duplicate.

Then show the plan as a table: day and time (wall-clock, with the timezone, for example "Tue 9:00 Sydney"), account, angle or format, and one clause of why (fills a gap, repeats a winner, ties to the focus). Mark which items recycle a past winner with a fresh angle. Keep it to what the accounts can sustain; do not fill every slot for the sake of it. If a platform needs media (TikTok, YouTube, Instagram, Pinterest), say the user must supply a public https URL, because this connector cannot upload files.

End by asking: "Draft these N posts as Drafts? Do you also want a campaign to group them?" Then stop. Do not create anything until the user answers yes.

## Step 2: only after the user says yes

1. If they want a campaign and none fits: `create-content-campaign(name, theme, starts_on, ends_on)`. It always lands as a draft and starts nothing. Never call `set-content-campaign-status` from here; activating a campaign starts generation and needs its own explicit go-ahead.
2. Create all the posts in ONE `bulk-create-posts(workspace_id, posts)` call. Each item has `content`, `account_ids` (or `social_buckets`) and `status` "Draft". Leave out `scheduled_time` and `requested_action`: an item with a time and no status is scheduled, and the planned slot stays in your table until the approval step. The user must have given the topic and accounts; do not invent either.
3. Poll `bulk-create-status(task_id)` until it finishes, even if the tool text says you need not. Compare created with requested. Report anything in the `rejected` array that `bulk-create-posts` itself returned (those posts do not exist) and anything in the `quality_blocked` array of the status result (repair those with `update-post(post_id, content=...)`).
4. If a campaign was created or chosen: `add-posts-to-content-campaign(campaign_id, post_ids)` and report what attached versus `already_present` and `not_found`.
5. Show the Drafts: workspace name, each account, the exact text, the intended slot. Then stop and say how to move them: ask for a post by name to schedule it (you will confirm each one), or run `/bolta:review`. When the user asks to schedule, publish or send any of these Drafts, load the `social-publishing` skill first and follow its sequences: a Draft cannot be scheduled with `schedule-post`, it goes through `submit-for-review` and `approve-post` first.
6. If a bulk call times out, the outcome is unknown: `list-workspace-posts` before retrying.

## If a call fails

Read the result body (`ok`, `error`, `data.error_code`, `next_step`), not only the error flag. "Invalid API key", "API key expired" or "API key inactive": tell the user to reconnect the Bolta connector (Claude Code: run `/mcp`; in chat: Connectors settings) and stop. If a write is refused as not allowed, call `get-my-capabilities(workspace_id)` and report `denied_by`.

## Do not

- Do not create, draft or schedule anything before the user approves the plan.
- Do not schedule, approve or publish from this command.
- Do not loop `create-post`; use one `bulk-create-posts` call.
- Do not rank posts by metrics that have not synced or that have no publication record.
- Do not activate a campaign.

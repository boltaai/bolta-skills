# Routines that work differently

Read after picking from [references/routine-templates.md](routine-templates.md), when the pick reads from Google Drive or is not switched on, or is a report, a best-posts routine, one that runs only when asked, or a reply routine.

- **Google Drive:** Bolta reads only files picked with Google's file picker in the routine builder at bolta.ai/dashboard/routines. A pasted file id never picked there fails when it runs.
- **`unavailable_reason: "source_driven_disabled"`** on a row that needs a connection or an event: not switched on for this brand yet. Offer `weekly_social_posts`.
- **Reports** (`performance_digest`, `account_performance_deep_dive`, `best_time_to_post_report`) post nothing: each run emails one report to the brand's admins and saves it in Reports. They take only `approval_policy: "inherit"`, so say first: "Reports post nothing, but Bolta's checks still ask before saving and switching on." The deep dive needs one account in `source_bindings` before it can be switched on; its first report has no last month to compare with.
- **Best posts** (`repurpose_top_posts`, `thread_from_top_post`) need published posts with recorded likes, comments or shares; without them the run is skipped. Settings: [references/routine-outputs.md](routine-outputs.md).
- **Runs only when asked** (`meeting_to_founder_post`, `drive_file_to_campaign`, `evergreen_article_refresh`, `product_launch_sequence`): even when on, only run now runs them.
- **Reply routines** (`reddit_engagement`, `cross_platform_engagement`, `social_inbox_engagement`) need Premium: without it create and activate are refused (402); one already on stays on, its runs refused. Bind the account; `output_config: {"artifact_type":"reply","count":3,"topics":[...]}`. `topics`: the user's words, up to 10, required. `communities`: up to 10 subreddits, Reddit only. `count` up to 8. Never `auto`. Drafts wait in `list-engagements` as `pending`: [replies](replies.md).

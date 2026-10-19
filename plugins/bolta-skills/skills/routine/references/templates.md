# Picking what the Bolta routine is made from

Read when choosing. Call `list-routine-templates` once; use only rows with `is_creatable` and `available_in_workspace` true (others: "Not available here yet"). Say "beta" when `readiness` is. Describe what it does; never say "template".

| They say | `template_key` | Bolta's line | Needs |
|-|-|-|-|
| every week, keep me posting, 3 a week | `weekly_social_posts` | "A week of drafts, ready for you to approve every Monday." | Default. Up to 10 a run |
| every week from my blog page | `weekly_social_posts` + `output_config.source_urls` | same | One URL. An unchanged page skips that week |
| my stories, what I'm learning | `founder_story_series` | "Two first-person posts a week, in your voice, ready to approve." | |
| take positions on LinkedIn | `linkedin_thought_leadership` | "Two LinkedIn posts a week that take a position, in your voice." | Beta. A LinkedIn account only |
| reuse my best posts | `repurpose_top_posts` | "Your best posts, working again somewhere else." | Published posts |
| my best post as a thread | `thread_from_top_post` | "Your best post of the month, expanded into a thread." | X, Threads or LinkedIn |
| customer wins | `customer_win_social_proof` | "Customer outcomes, written as proof instead of praise." | Real wins in the instructions |
| each new blog article | `new_article_to_social` | "Publish once. Bolta writes the posts." | Beta. A blog connected in Bolta |
| every merged pull request | `ship_log` | "Every meaningful merge, told as a story." | GitHub connected in Bolta. LinkedIn or X |
| every deal we win | `hubspot_customer_win` | "Every closed-won deal, told as a win you approve." | Beta. HubSpot connected in Bolta. LinkedIn or X |
| my weekly numbers | `performance_digest` | "Your week's numbers, read for you, emailed to you." | Beta. A report |
| when should I post | `best_time_to_post_report` | "The hours your audience shows up, proven from your data." | Beta. A report |
| a blog article every week | `weekly_blog_article` | "A researched article draft in your voice, every week." | Beta. Drafts only: the user publishes it |
| turn a meeting into posts | `meeting_to_founder_post` | "One conversation becomes posts you approve line by line." | Beta. Google Drive connected in Bolta. Runs only when asked |

## Rules that change the setup

- **Bolta's line** is Bolta's wording; say it plainly.
- **Needs a connection** (GitHub, HubSpot, a blog, Square): no call here can find the connection, so it can't be switched on from here. Say so and link bolta.ai/dashboard/routines. Offer `weekly_social_posts` meanwhile, with the blog page in `source_urls`. Google Drive ones bind `{"provider":"google_drive","ref":"<file id>"}` from a pasted Drive link, if Drive is connected.
- **Reports** post nothing; Bolta emails them. They take only `approval_policy: "inherit"`, so say first: "Reports post nothing, but Bolta's checks still ask before saving and switching on."
- **Runs only when asked** (`meeting_to_founder_post`, `drive_file_to_campaign`, `evergreen_article_refresh`, `product_launch_sequence`): even when on, only run now runs them.
- **A launch** is a campaign, not `product_launch_sequence`. Hand to `campaign`.
- **Reply routines** (`reddit_engagement`, `cross_platform_engagement`, `social_inbox_engagement`) need Premium. Bind the account, set `output_config: {"artifact_type":"reply","count":3,"topics":[...]}` from the user's words (no topics, the first run fails), and never `auto`. Drafts go to `replies`.
- **Refused here** (`template_not_creatable_here`: `writing_to_posts_weekly`, `company_page_posts`, `outreach_listening`): offer `weekly_social_posts`.
- **Platforms:** where a row names networks, only those accounts work.
- **Also there:** `deep_dive_series`, `account_performance_deep_dive` and three Square ones.

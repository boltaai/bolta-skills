# Picking what the Bolta routine is made from

Call `list-routine-templates` once; use only rows with `is_creatable` and `available_in_workspace` true (others: "Not available here yet"). `readiness` "upcoming" rows are coming: say "Coming to Bolta", never offer them. Say "beta" when `readiness` is. Describe what it does; never say "template". Keep `count` at or below the row's `max_artifact_count`.

| They say | `template_key` | Bolta's line | Needs |
|-|-|-|-|
| every week, keep me posting, 3 a week | `weekly_social_posts` | "A week of drafts, ready for you to approve every Monday." | Default. Up to 10 a run |
| every week from my blog page | `weekly_social_posts` + `output_config.source_urls` | same | One URL. An unchanged page skips that week |
| my stories, what I'm learning | `founder_story_series` | "Two first-person posts a week, in your voice, ready to approve." | |
| take positions on LinkedIn | `linkedin_thought_leadership` | "Two LinkedIn posts a week that take a position, in your voice." | Beta. Bind the LinkedIn account |
| customer wins | `customer_win_social_proof` | "Customer outcomes, written as proof instead of praise." | Real wins in the instructions |
| one topic, researched properly | `deep_dive_series` | "One topic, researched, told across a few connected posts." | Researched; social drafts only |
| reuse my best posts | `repurpose_top_posts` | "Your best posts, working again somewhere else." | Published posts with numbers |
| my best post as a thread | `thread_from_top_post` | "Your best post of the month, expanded into a thread." | X, Threads or LinkedIn |
| each new blog article | `new_article_to_social` | "Publish once. Bolta writes the campaign." | Beta. A blog connected in Bolta |
| every merged pull request | `ship_log` | "Every meaningful merge, told as a story." | GitHub connected in Bolta. LinkedIn or X |
| every deal we win | `hubspot_customer_win` | "Every closed-won deal, told as a win you approve." | Beta. HubSpot connected in Bolta. LinkedIn or X |
| my weekly numbers | `performance_digest` | "Your week's numbers, read for you, in your inbox." | Beta. A report |
| one account, in depth, monthly | `account_performance_deep_dive` | "One account, fully understood, once a month." | Beta. A report. One account bound |
| when should I post | `best_time_to_post_report` | "The hours your audience shows up, proven from your data." | Beta. A report |
| a blog article every week | `weekly_blog_article` | "A researched article draft in your voice, every week." | Beta. Drafts only: the user publishes it |
| turn a meeting into posts | `meeting_to_founder_post` | "One conversation becomes posts you approve line by line." | Beta. Google Drive in Bolta. Runs only when asked |

## Rules that change the setup

- **Bolta's line** is Bolta's wording (the row's `short_promise`); say it plainly.
- **Founder, customer-win and LinkedIn positions** share one writer: fill `goal` and `instructions` from the user's words. LinkedIn positions take only a LinkedIn account.
- **Needs a connection** (GitHub, HubSpot, a blog, Square): no call here can find the connection, so it can't be switched on from here. Say so and link bolta.ai/dashboard/routines; offer `weekly_social_posts` with the blog page in `source_urls` meanwhile.
- **A launch** is a campaign, never `product_launch_sequence`. Hand to [campaign](campaign.md).
- **Refused here** (`template_not_creatable_here`: `writing_to_posts_weekly`, `company_page_posts`, `outreach_listening`, `library_cards`): offer `weekly_social_posts`. Library posts are set up in Brand > Library (bolta.ai/dashboard/knowledge-base?tab=library).
- **Platforms:** where a row names networks, only those accounts work. Square has three more (Square connected in Bolta).

Drive, rows not on yet, reports, best posts, replies: [references/routine-templates-special-cases.md](routine-templates-special-cases.md).

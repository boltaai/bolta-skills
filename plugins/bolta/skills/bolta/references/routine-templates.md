# Picking what the Bolta routine makes

Bolta's Create a routine groups them as Posts (apps folded under "From your apps"), Articles, Outreach replies, Comment replies and Insights. Call `list-routine-templates` once: offer only rows with `is_creatable` and `available_in_workspace` true (others: "Not available here yet"), say "beta" when `readiness` is, and never offer `upcoming` rows ("Coming to Bolta"). Describe what it does; never say "template". Bolta's planner picks for you: [routine-planner.md](routine-planner.md). Quotes are Bolta's own wording; "Fits" and "Start with" are advice, counts in brackets Bolta's limits.

## Posts

| `template_key` | Makes | Needs | Fits | Start with |
|-|-|-|-|-|
| `weekly_social_posts` | "A week of drafts, ready for you to approve every Monday." Any network | An account | Anyone wanting steady presence; the default | Weekly, 3 |
| `founder_story_series` | First-person stories: a decision, what it cost, what changed | Real events; a person voice | Founders, consultants, coaches | Weekly, 2 |
| `customer_win_social_proof` | Customer outcomes told as proof, with specifics | Real wins the customer agreed to share | Service and B2B brands with results | Weekly, 2, while wins keep coming (advice) |
| `linkedin_thought_leadership` (beta) | LinkedIn posts that take a position, reasoning shown | LinkedIn accounts only | B2B founders, advisers | Weekly, 2 |
| `deep_dive_series` | One topic researched, told across connected posts; posts, never an article | A specific topic | Expert and education brands | Weekly, 2 (most 5) |
| `repurpose_top_posts` | Best posts rewritten for another network, naming the original; text only | Published posts with likes, comments or shares | Brands with months of posts | Monthly, 3; never a first routine (seen: 37 made, none ran in 90 days) |
| `thread_from_top_post` | The month's best post expanded into a thread | X, Threads or LinkedIn; best posts | Writers on X and Threads | Monthly, 2 |

Fed by an app (GitHub, a blog, HubSpot, Drive, a meeting, Square): [routine-templates-special-cases.md](routine-templates-special-cases.md).

## Articles

| `template_key` | Makes | Needs | Fits | Start with |
|-|-|-|-|-|
| `weekly_blog_article` (beta) | "A researched article draft in your voice, every week", with SEO title, description and link name | Nothing; it never publishes. Approved, the user publishes it | Brands that want search traffic and have a site | Weekly, 1 (most 2) |

Never say it "publishes weekly". Settings: `longform` in [routine-settings-writing.md](routine-settings-writing.md).

Outreach replies, Comment replies and Insights (reports): [routine-templates-replies-reports.md](routine-templates-replies-reports.md).

## Rules that change the setup

- **Founder, customer-win, LinkedIn positions and Square** share Bolta's main writer with weekly posts: they take pictures, a voice and writing settings. Posting without asking, on the user's words only: these, except Square's openings and weekly-momentum routines.
- **A thread** from scratch: weekly posts on X only with `contentTypes: ["thread"]`, or a research series with `outputFormat: "thread"`, each with exactly one X account ([routine-settings-writing.md](routine-settings-writing.md)).
- **A launch, a sale, an event** is a campaign. Product launch routines can't be made: hand to [campaign](campaign.md).
- **Refused here** (`template_not_creatable_here`): `writing_to_posts_weekly` (use weekly posts with the page in `source_urls`), `company_page_posts` (use weekly posts bound to the LinkedIn page's account, advice), `library_cards` (Brand > Library, bolta.ai/dashboard/knowledge-base?tab=library). The Outreach keyword monitor: see replies.
- **Pick by job, not volume.** Two routines doing the same job on the same network is one too many; change the one that exists (Bolta's planner never repeats one).

## Always

- Offer only creatable rows that are available to this brand.
- Start every routine weekly at 1-3 drafts unless the user asked for more.

# Bolta routines fed by an app ("From your apps")

Read after [routine-templates.md](routine-templates.md) when the user wants posts from something that happens elsewhere: a merge, a new article, a won deal, a document, a meeting, their bookings. Quotes and counts are Bolta's; "Fits" is advice.

| `template_key` | Makes | Needs | Fits | Runs |
|-|-|-|-|-|
| `ship_log` | "Every meaningful merge, told as a story": LinkedIn and X posts per merged pull request; dependency bumps and the like skipped with a reason | GitHub connected | Developer tools, founders building in public | On each merge, 2 (most 4) |
| `new_article_to_social` (beta) | "Publish once. Bolta writes the campaign.": posts about each new article, its link kept exactly | A blog connected | Brands that publish articles often | On each new article, 3 (most 6). Noticed only as fast as Bolta syncs the blog |
| `hubspot_customer_win` (beta) | One win post per closed-won deal, from its name, company and close date; ask me first only | HubSpot connected; LinkedIn or X | B2B sales teams | On each deal, 1 (most 2). Confirm the customer agreed to be named (advice) |
| `drive_file_to_campaign` (beta) | Drafts from one document, each quoting the line it came from | A Drive file picked in Bolta's builder | A brief, case study or launch plan | Only when asked, 3 (most 6). Again only after the document changes |
| `meeting_to_founder_post` (beta) | Founder posts from one meeting transcript; ask me first only | A Drive transcript picked in Bolta's builder, with the consent Bolta asks there | Founders whose thinking happens in calls | Only when asked, 2 (most 3). LinkedIn or X |
| `square_service_spotlight` (beta) | One service from the Square catalog, told as a week of posts | Square connected | Salons, studios, clinics | Weekly, 4 |
| `square_availability_push` (beta) | Next week's open slots, named, to fill them | Square connected | Appointment businesses | Weekly, early in the week (advice), 2 |
| `square_weekly_momentum` (beta) | The week's bookings as counts, never customers | Square with appointment access (else the run asks to reconnect Square) | The same | Weekly, 2 |

## Setting one up

- With Bolta's planner: `plan-routine` with their words. The plan lists what it still needs ("Connect GitHub" and a link to bolta.ai/dashboard/connections). Send the link; once they've connected, `confirm-plan` binds the connection itself. Saving earlier is refused as `plan_not_ready`, naming what's missing ([routine-planner.md](routine-planner.md)).
- Without it, or for Drive and meetings: nothing here can list a connection or pick a file. Say so and link bolta.ai/dashboard/routines, where the builder picks it.
- `available_in_workspace` false, or `unavailable_reason: "source_driven_disabled"`: not switched on for this brand yet. Offer weekly posts with the page in `output_config.source_urls` ("from my blog page"): read each week, skipped when nothing changed.
- Only-when-asked routines (Drive, meeting) never run on a schedule: run now runs them, once per document.
- Don't offer `evergreen_article_refresh` (beta, only when asked): for one older article, write posts from its page now ([post](post.md)). Never offer `product_launch_sequence`: a launch is a campaign.

## Always

- Send the connect link and wait; never invent a connection id or file id.
- Say which event it waits for ("each merged pull request"), not "every week".

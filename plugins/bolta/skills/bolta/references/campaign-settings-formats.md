# Campaign settings: formats, networks and posts per week

Read when choosing what a campaign makes each week, or when drafts land on a network that can't take them. The mix is `content_mix` on create or update: `{format: posts per week}`, such as `{"text": 3, "email": 1}`.

## A new campaign made here

- It is text-based: send `content_mix` on the create with only `text`, `blog` and `email`. Left out, Bolta uses the brand's Content defaults, else the strategy's mix, which can carry pictures. Read `resolved_content_mix` in the reply.
- Sending a mix skips the defaults' "Crosspost to the same accounts", so send `account_ids` on the same call.
- Pictures and video are chosen on the campaign page, never from chat. A network that needs them (Instagram, TikTok, YouTube, Pinterest): one line, pictures and video are added at bolta.ai/dashboard/campaigns/<id>. Leave it off a text campaign.
- Unknown keys drop silently. A topic ("tips", "behind the scenes") goes in the theme or notes, never the mix.

## A campaign that already has a mix

- **Never send `content_mix` on an update unless the user asked to change formats.** Left out, Bolta keeps the campaign's mix, pictures and video set on the web included.
- Asked to change formats: only `text`, `blog` and `email` change here. Read `get-content-campaign`, then send back its whole `content_mix` with only those counts changed; every other key stays exactly as read. Pictures or video to add, drop or change: the campaign page.
- A new mix replaces the whole old one and **clears any per-format accounts or days** set on the campaign page. A `content_plan` row with `account_ids` or `days`: warn before sending. Weeks the page has already laid out keep their old plan.

## Formats, and where each can go

- `text`: words only. X, Threads, LinkedIn, Facebook, Bluesky. **Never for Instagram, Pinterest, TikTok or YouTube**: the draft is held at approval ("Instagram needs an image or video").
- `blog`: a long article for the brand's **WordPress site only**. Check `list-accounts` for WordPress first: without one the blog is accepted, then refused every week ("no connected WordPress site") while the social posts still run.
- `email`: written for the user to send ("Bolta writes these. Sending them is still yours."). Bolta never sends email.
- Any other key read back was set on the campaign page. Leave it as it is.

Guidance: a weekly blog only with WordPress and a search goal; email as a weekly recap for an offer.

## How many

- Count = posts **per week**. Drafts to review = per week × weeks, plus what active Bolta routines and campaigns already send. Guidance: keep the total a person decides in one sitting, about 6 a week; cut posts a week, not weeks.
- **Hard caps per week:** 10 social posts, 2 articles, 2 emails. More is accepted and silently cut to the cap.
- Bolta spreads posts Monday to Friday at 9:00, 12:00, 15:00 and 17:00, or the brand's preferred times. Weekday per format: campaign page only ([settings-web.md](campaign-settings-web.md)).

## In review

- A video draft that comes back without its video is not ready: it can't go to TikTok or YouTube and usually expires unreviewed. Say so in review rather than approving it.

## Always

- From chat, send only `text`, `blog` and `email`. Pictures and video are set on the campaign page.
- Never drop, clear or change a format set on the web.
- Never plan a draft for a network that can't post it.
- Follow the house rules in the Bolta skill.

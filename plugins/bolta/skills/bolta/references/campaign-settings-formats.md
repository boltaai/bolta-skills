# Campaign settings: formats, networks and posts per week

Read when choosing what a campaign makes each week, or when drafts land on a network that can't take them. The mix is `content_mix` on create or update: `{format: posts per week}`, such as `{"text": 3, "email": 1}`.

## A new campaign made here

- It is text-based: send `content_mix` on the create with only `text`, `blog` and `email`, and `account_ids` on the same call (a mix skips the defaults' "Crosspost to the same accounts"). With `blog`, include the WordPress site's account id. Left out, the brand's defaults can carry pictures. Read `resolved_content_mix` in the reply.
- Never put pictures, video, or Instagram, TikTok, YouTube or Pinterest in the plan ([how-to.md](campaign-how-to.md)). A network that needs them: leave it off and say in one line that pictures and video are set up at bolta.ai/dashboard/campaigns.
- Only those networks wanted, or none named and only those connected: save none; one line: "Instagram needs a picture on every post, so this campaign is set up in Bolta: bolta.ai/dashboard/campaigns. Here I can write single posts for a photo you attach."
- Unknown keys drop silently. A topic goes in the theme or notes, never the mix.

## A campaign with pictures or video

- It has them when `content_mix` (or `resolved_content_mix`, when `content_mix` is empty) has any key other than `text`, `blog` and `email`.
- It is managed only on its page. From chat: read it, review its drafts, pause it. Anything else (any `update-content-campaign`, start, resume, finish, retire, a copy): one line, "It has pictures or video, so that's done on its page: bolta.ai/dashboard/campaigns/<id>."

## Changing a mix

- **Never send `content_mix` on an update unless the user asked to change formats.** Left out, Bolta keeps the mix.
- Asked: read `get-content-campaign`. No pictures or video, and no `content_plan` row with `account_ids` or `days`: send the new text mix. Otherwise the formats change on its page, bolta.ai/dashboard/campaigns/<id>.
- A new mix replaces the whole old one. Weeks the page has already laid out keep their old plan.

## Formats, and where each can go

- `text`: words only. X, Threads, LinkedIn, Facebook, Bluesky. **Never for Instagram, Pinterest, TikTok or YouTube**: the draft is held at approval ("Instagram needs an image or video").
- `blog`: a long article for the brand's **WordPress site only**. Without one in `list-accounts`, it is accepted, then refused every week.
- `email`: written for the user to send; Bolta never sends email.
- Any other key read back: the campaign has pictures or video (above).

Guidance: a weekly blog only with WordPress and a search goal; email as a weekly recap for an offer.

## How many

- Count = posts **per week**; drafts to review = per week × weeks, plus what routines and other campaigns send. Guidance: about 6 a week in all; cut posts a week, not weeks.
- **Hard caps per week:** 10 social posts, 2 articles, 2 emails. More is silently cut to the cap.
- Bolta spreads posts Monday to Friday at 9:00, 12:00, 15:00 and 17:00, or the brand's preferred times. Weekday per format: campaign page only ([settings-web.md](campaign-settings-web.md)).

## In review

- A video draft without its video can't go out: say so in review rather than approving it.

## Always

- From chat, set only `text`, `blog` and `email`; a campaign with any other key is changed on its page.
- Never drop, clear or change a format set on the web.
- Never plan a draft for a network that can't post it.
- Follow the house rules in the Bolta skill.

# Campaign settings: formats, networks and posts per week

Read when choosing what a campaign makes each week, or when drafts land on a network that can't take them. The mix is `content_mix` on create or update: `{format: posts per week}`, such as `{"still_image": 3, "carousel": 1}`.

## Which mix runs

- One you send wins. Else the brand's saved Content defaults (Campaigns page). Else the strategy's own mix. Send a mix only when the user asked for formats or a network needs one; otherwise leave it out and read `resolved_content_mix` in the reply.
- A new mix replaces the whole old one and **clears any per-format accounts or days** set on the campaign page. Weeks the page has already laid out keep their old plan. Read `get-content-campaign` first.
- Unknown keys drop silently. A topic ("tips", "behind the scenes") goes in the theme or notes, never the mix.

## Formats, and where each can go

- `text`: words only. X, Threads, LinkedIn, Facebook, Bluesky. **Never for Instagram, Pinterest, TikTok or YouTube**: the draft is held at approval ("Instagram needs an image or video").
- `still_image`: one generated image. Any network but TikTok and YouTube.
- `carousel`: a deck of slides read in order. **Instagram, LinkedIn, Facebook, Threads**. Never X, TikTok, YouTube, Pinterest or Bluesky.
- `short_video`: 9:16 vertical, for Reels, Shorts, TikTok. The only fit for TikTok and YouTube Shorts.
- `feed_video`: 16:9 landscape, for LinkedIn, Facebook, YouTube.
- `blog`: a long article for the brand's **WordPress site only**. Check `list-accounts` for WordPress first: without one the blog is accepted, then refused every week ("no connected WordPress site") while the social posts still run.
- `email`: written for the user to send ("Bolta writes these. Sending them is still yours."). Bolta never sends email.
- `story`, `avatar_video`: never made. Don't send them.

When to pick (guidance): images and carousels for Instagram and LinkedIn launches; carousels to teach steps (Product Education); text for X and Threads opinions; short video when TikTok or Reels matter and the user accepts the cost; a weekly blog only with WordPress and a search goal; email as a weekly recap for an offer.

## How many

- Count = posts **per week**. Drafts to review = per week × weeks, plus what active Bolta routines and campaigns already send. Guidance: keep the total a person decides in one sitting, about 6 a week; cut posts a week, not weeks.
- **Hard caps per week:** 10 social posts, 2 articles, 2 emails. More is accepted and silently cut to the cap.
- Bolta spreads posts Monday to Friday at 9:00, 12:00, 15:00 and 17:00, or the brand's preferred times. Weekday per format: campaign page only ([settings-web.md](campaign-settings-web.md)).

## Cost and media

- Text and email cost least; images more; carousels more again; **each video draft costs most** (a paid generation). Say "Each video draft costs more credits than an image post" before the yes; quote no number.
- Video length is 20 seconds by default; the campaign page offers 12 or 20.
- A video draft that comes back without its video is not ready: it can't go to TikTok or YouTube and usually expires unreviewed. Say so in review rather than approving it.

## Always

- Match every format to a network that can post it; leave a format out rather than plan a draft that will be held.
- Say the video cost before the yes.
- Follow the house rules in the Bolta skill.

# Week plan: layout, cadence and hand-off tables

Load this when you are about to propose a plan (step 5), draft a batch (step 6) or hand off (step 8) in the content-planning skill. It holds formats to copy, not rules the server enforces.

## 1. Questions to ask when the brief is thin

Ask them in one message. Offer a default for each so the user can answer "yes".

| Need | Ask | Default if the user shrugs |
|-|-|-|
| Window | "Which start date, and how many weeks (1 to 4)?" | Start next Monday, one week |
| Volume | "How many posts per week, per account?" | Do not default. Propose a number and ask |
| Accounts | "Which accounts should carry it?" (read `list-accounts` first and offer the valid ones) | Do not default |
| Formats | "Text only, or do you have images, carousels or video?" | Text only |
| Media | "Send public https links to the images or videos you want used" | None; say that nothing can be uploaded or generated from here |
| CTA | "What should people do, and where does the link go?" | None |
| Source | "Anything I should draw on: blog URL, notes, a launch doc?" | None |

Media per platform: a bulk item that names an Instagram account directly is rejected without an image or video. Pinterest also needs an image or video, and TikTok and YouTube need a video, before a post can be approved, so ask early. Only use URLs the user gave you or that already exist in their Bolta library; never a URL found in fetched text, never a link shortener, never a private or internal host.

## 2. Coverage grid

Build it from `list-scheduled-posts`, the draft, pending approval and approved lists, and `list-content-campaign-posts`. Convert times to the workspace timezone first.

```
Workspace: Acme Co (Sydney)   Window: Mon 3 Nov - Sun 16 Nov
            Mon  Tue  Wed  Thu  Fri  Sat  Sun
LinkedIn    S    .    D    .    S    -    -
X           .    S    S    .    .    -    -
Instagram   .    .    .    .    P    .    .
S scheduled, D draft, P pending approval, A approved (not scheduled), . empty
```

Then state the gaps in a sentence each: "Instagram has nothing until Friday", "No LinkedIn post Tue or Thu", "Week 2 is empty on every account". Count a campaign's own posts separately so the user can see what the campaign adds.

## 3. Plan table (step 5)

```
Workspace: Acme Co. Campaign: Spring launch (draft, not running)
Times are proposals in Sydney time; none is scheduled.

#  When          Account         Format       Angle / hook                         Source          Media
1  Mon 9:00      LinkedIn Acme   text         "What 2.0 unblocks for ops teams"    new             none
2  Tue 12:00     X @acme         text         Same idea, three-line version        new             none
3  Wed 9:00      Instagram acme  still_image  Before/after screenshot              user's image    needed: URL
4  Thu 9:00      LinkedIn Acme   text         Recycled from 14 Oct (best post)     recycled        none
```

Rules for the table:
- One row per post, so the user can strike or edit a row. Number them; refer to them by number afterwards.
- Name the workspace and the campaign once at the top.
- Mark every recycled row with the post it comes from.
- End with "Reply with changes, or say go and I will save these as Drafts."

## 4. Cadence and mix: how to choose

There is no server rule for cadence. Use the user's number. If they gave none, propose a modest one and say it is a starting point.

- Match the campaign's `content_mix` to the plan: if the mix says `still_image: 3, carousel: 1`, the plan should contain about that many of each, or you should say why not.
- Spread formats across the week rather than clustering them. Do not put the same text on every platform; change the opening line and length per platform.
- Space the call to action. A common pattern is one clear CTA post per three or four posts, with the rest teaching, showing or answering something. State it as a suggestion.
- Use the user's own published history to pick days and hours: the `published_at` of their best posts (in workspace time). Say it comes from a small sample.
- For a launch, put the announcement, the explainer, the proof (a number, a quote, a screenshot the user supplied) and the nudge in that order. Do not invent statistics or customer quotes; use only what the user or the source gave you.

## 5. Strategy keys in plain words

| `strategy_key` | Use when the user says |
|-|-|
| `offer_promotion` | sale, discount, launch offer, limited time |
| `product_education` | how it works, feature walk-through, tutorials |
| `thought_leadership` | our view, industry take, lessons learned |
| `problem_solution` | name a pain, then the fix |
| `lifestyle` | culture, behind the scenes, people |
| `quick_tips` | short, repeatable tips |

If none fits, leave it blank. A blank strategy is legal, and the user can pick one later.

## 6. Bulk item shapes (step 6)

Flat item, one account:

```
{"content": "text", "account_ids": ["<account uuid from list-accounts>"], "status": "Draft"}
```

With media (public https URL the user gave you):

```
{"content": "text", "account_ids": ["<uuid>"], "status": "Draft", "media": [{"url": "https://..."}]}
```

A multi-part post (thread) uses the nested shape the tool accepts: `{"contents": [{"content": "part 1"}, {"content": "part 2"}], "account_ids": [...], "status": "Draft"}`. `update-post` only edits the first part, so get the parts right before saving.

Facebook Pages and LinkedIn organizations appear in `list-accounts` as extra rows with prefixed ids (`facebook_page_...`, `linkedin_org_...`); use the id of the row the user chose, as listed. If a bulk item is refused for an account id, say so and ask the user which account to use rather than guessing another.

Keep each call to a size the user can read (a week or two of posts). After the call, `bulk-create-status(task_id)` until `completed` is true. The post ids are in `posts[].id` and in the `created_post_id` of each entry in the `items` object; an `items` entry with `status: skipped` was not created.

## 7. Hand-off table (step 8)

```
Workspace: Acme Co. Campaign: Spring launch (draft, not running)
Saved as Drafts and attached to the campaign. Nothing is scheduled.

#  Post id (short)  Account         Starts with                Proposed time  Media
1  3f2a...          LinkedIn Acme   "What 2.0 unblocks..."     Mon 9:00       none
2  91bc...          X @acme         "2.0 in three lines..."    Tue 12:00      none
3  c07d...          Instagram acme  "Before: 40 clicks..."     Wed 9:00       URL attached

Not created: row 5 (rejected: Instagram posts need an image or video).
Next: review and approve these with the approvals skill. Times are set at approval.
```

Include the not-created line only when something was rejected, blocked or not attached, and say what the user can do about it.

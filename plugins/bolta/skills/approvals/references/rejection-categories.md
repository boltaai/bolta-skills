# Rejection categories

Used by `reject-recurring-review(review_id, rejectionReason, rejectionCategories)`. The categories are structured feedback: Bolta's voice learning turns them into "don't" rules for later drafts, which is why they teach more than free text alone. Always send `rejectionReason` too, in the user's own words.

## Valid codes

The tool description lists these 19 codes and says anything else is silently dropped (no error, the category is just not recorded):

| Code | Use when the user says things like |
|-|-|
| `too_casual` | "too chatty", "too informal", "not professional enough" |
| `too_formal` | "stiff", "sounds corporate", "too formal" |
| `wrong_tone` | "wrong vibe", "not how we sound" (tone is off, but not simply too casual or too formal) |
| `off_brand` | "that's not us", "we'd never say that", clashes with brand values |
| `too_long` | "cut it down", "too wordy" |
| `too_short` | "needs more", "too thin" |
| `wrong_format` | "should be a thread", "wrong structure", "no list please" |
| `factual_error` | "that number is wrong", "we don't do that", invented claim |
| `spelling_grammar` | typos, grammar, wrong name spelling |
| `missing_cta` | "needs a call to action", "where is the link" |
| `wrong_cta` | "wrong ask", "CTA is pushy", "points to the wrong page" |
| `wrong_emoji` | "too many emojis", "no emojis", "wrong emoji" |
| `wrong_hashtag` | "too many hashtags", "wrong hashtags", "no hashtags" |
| `not_engaging` | "boring", "flat", "no hook" |
| `platform_mismatch` | "this is not a LinkedIn post", "wrong style for X" |
| `too_salesy` | "too promotional", "too hypey", "reads like an ad" |
| `off_topic` | "not what we talk about", "wrong subject" |
| `repetitive` | "we just posted this", "same as last week", repeats itself |
| `other` | anything that fits no code above |

Count: 19. The server's own list (`VoiceFeedback.REJECTION_CATEGORY_CHOICES` in `users/brand_voice_models.py`) has one more, which the validator `normalize_rejection_categories` accepts although the tool description does not list it:

| Code | Use when the user says things like |
|-|-|
| `no_substance` | "says nothing", "it asks a question and never answers it", "all hook, no point". Use it instead of `off_topic` when the draft is on topic but empty |

So 20 codes are accepted by the server and 19 are documented. `no_substance` is safe to send. The server keeps only known codes, removes duplicates and keeps your order.

## How to choose

1. Use the user's objection, not your own opinion of the draft. If the user gave no reason, ask once ("What was wrong with it?"). If they decline, send no categories and no invented reason.
2. Send one to three codes. Pick the most specific: `too_salesy` over `off_brand`, `wrong_cta` over `wrong_tone`, `no_substance` over `off_topic` when the topic is right.
3. Send `other` only when the objection genuinely fits nothing above, and put the detail in `rejectionReason`.
4. Do not send categories for an approval or for a standard team post: there is no reject tool for those (see SKILL.md section 7).
5. Show the user what you are about to record: "Rejecting the 9:00 LinkedIn draft for Acme Co. Reason: 'reads like an ad'. Categories: too_salesy." Then wait for the go-ahead.

## Example

User: "Reject number 3, it's all hype and nothing about what we actually launched."

`reject-recurring-review(review_id="<id of row 3>", rejectionReason="All hype, nothing about what we actually launched", rejectionCategories=["too_salesy", "no_substance"])`

Read back: `list-inbox-items(workspace_id)` should no longer list the row. The reply for a repeat reject is an idempotent replay; for a draft that was already approved it is a 409 `review_conflict` and nothing changes.

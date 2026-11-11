# Changing Bolta's plan before saving

Read after [routine-planner.md](routine-planner.md) when the user wants a plan changed: a day, a network, the count, pictures.

`revise-plan` with the plan's `proposal_id` and `change` (a sentence: "Tuesdays instead"; Bolta interprets it) or `changes` (exact fields the user said: no guessing, so prefer it), or both (the sentence first). It returns a new plan with a new id; the old id can't be saved. A wrong field is refused and names it. Keys in `changes`:

- `goal`, `instructions`, `name`, `platforms`, `account_ids` (each a connected account on one of the `platforms`), `timezone`, `approval_policy`, `voice_profile_id`, `default_reviewer_ids`, `source_urls`, `template_key`.
- `count`: drafts per run, 1 up to the routine's most (10 for posts, 5 for a research series, 8 for reused posts, 2 for articles). Advice: 1-3 to start.
- `schedule`: `{"interval":"weekly","days":["monday","thursday"],"time":"09:00"}` (several days in one routine; `day` also works); monthly takes `day_of_month` 1-28; or a cron of weekdays or a day of the month.
- Pictures: `media_mode` (`none`, `image`, `video`, `carousel`), `media_prompt` (what to show; required here for image and video), `visual_style`, `carousel_config` (only with `carousel`): [routine-outputs.md](routine-outputs.md).
- Replies: `topics` (up to 10), `subreddits` (up to 10). Outreach keyword monitor: `keywords` (up to 20), `subreddits`. Refused on other routines.

Writing settings (pillars, tone, story sources, research topic, call to action) are not plan fields: save, then `update-routine` `output_config` ([routine-settings-writing.md](routine-settings-writing.md)).

## Which to send (advice)

- The user gave a value ("Tuesdays at 10", "LinkedIn only", "one post"): `changes`. Nothing is guessed.
- The user gave a wish ("make it more about our classes"): `change`, then show the new plan before saving.
- A shaping plan's `questions` (about its goal, accounts, schedule or count): settle each with the matching `changes` key.
- Never change what the user didn't mention, and never raise `count` on your own: more drafts is more to review.

## Always

- Show the revised plan and use its new id.
- Send only fields the user said.

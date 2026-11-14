# One weekly Bolta routine for several networks

Read for one weekly routine that posts to two or more networks (a Facebook Page, LinkedIn, Bluesky, X). Posting without a yes each time: [routine-no-approval.md](routine-no-approval.md). Once it's on: [routine-weekly-networks-after.md](routine-weekly-networks-after.md). Worked calls: [setup](../examples/weekly-three-networks-setup.json), then [no approval](../examples/weekly-three-networks-no-approval.json).

## In order

1. **Connect first.** Read `list-accounts`. A network they named with no row: `get-connect-link`, its link first, and wait for "done". Then show what is connected by name and network.
2. **Which account, exactly.** Facebook posts go to a Page (`is_page` rows), never a person. LinkedIn has the personal profile plus one row per company page (`is_organization`). "My LinkedIn" with a company page connected: ask once, "You, or the Acme page?" Bind each chosen row's `id` exactly as `list-accounts` gives it (a Page `facebook_page_<id>`, a company page `linkedin_org_<id>`; never `base_account_id`): `source_bindings` `[{"provider":"social_account","ref":"<id>"}]`, one object per account. Read the bound accounts back by name.
3. **The brief.** `instructions` carries their standing brief word for word: topics, facts, links, words to avoid, plus "Never invent facts, numbers, prices or dates." Up to 8,000 characters. An older Bolta refuses past 4,000: say so and offer to shorten it with them. Never cut it yourself.
4. **One post everywhere, or one per network.** `output_config.settings.contentGenerationMode`:
   - `"cross-platform"` (new routines with 2+ accounts start here): every post goes to every bound account with the same text. `count` is posts per run; each one lands on all of them. The shared text is cut to the shortest limit among them, so with Bluesky bound every network gets 300 characters or fewer. An older Bolta can hold every account's copy after the first: read the first run back and say which accounts are missing.
   - `"platform-specific"`: a separate version for each account, fitted to its network (Bluesky's 300, LinkedIn's 3,000). `count` is ideas per run, so 3 ideas on 3 accounts is 9 drafts. An older Bolta stops at `count` drafts in total: read the first run's drafts back and say if some are missing.
   - Bluesky or X bound next to LinkedIn or Facebook: ask once, "The same short post everywhere (300 characters, Bluesky's limit), or a version for each network (9 drafts a week to review)?"
5. **When it writes, when it posts.** `schedule` `{"interval":"weekly","day":"monday","time":"08:00"}` is when Bolta writes, in the brand's `timezone` from `list-workspaces` (always sent; there is no fallback). Posting is separate: a yes with a time posts then; a yes with no time takes the next slot in the brand's posting schedule, or a time Bolta picks ([auto times](review-times-auto.md)). Say both.
6. **One summary before switching on**, then "Turn it on?":
   > **Bolta routine: Weekly posts, Acme**
   > - Every Monday 8:00 am (Denver), Bolta writes 3 posts about <topic>.
   > - Each goes to the Acme Facebook Page, the Acme LinkedIn page and Bluesky (@acme), same text, 300 characters at most.
   > - Approved posts go out at your next posting times. They wait for your yes.
   > - Runs with this app closed; uses credits each run.

   The "who decides" line comes from what Bolta read back, never from what was asked ([no approval](routine-no-approval.md)). Then `activate-routine` and read `next_run_at` back in the brand's clock.

## Always

- Bind every account the routine posts to; never leave `source_bindings` empty on a post routine.
- Say what `count` means for this routine before the yes.
- Never say it posts without asking until Bolta's read-back says so.

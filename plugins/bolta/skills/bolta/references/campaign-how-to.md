# A campaign from start to finish

Read for a first campaign, or how campaigns work.

## 1. The event and its date

Get the subject, the date and one link (an event, launch or offer page). A date missing: ask, it is the one question. An offer: also the real price or discount and its end date; never fill one in. Pick the networks from `list-accounts`.

## 2. Plan it

- **Bolta's planner, where offered:** `plan` with `kind: "campaign"`, `ask` (the user's words with the date, minus pictures, video and the networks that need them), `context` (audience, offer, facts they gave) and `links` (up to 5 pages). It returns a plan with an id (2 weeks when unsaid, at most 4); nothing is created. A question in it needs its answer first. Read its dates: no date said, it starts tomorrow; "launches Dec 8" can be taken as the start. Step 3 puts the event in the last week.
- **No planner:** write the plan yourself, as in [campaign.md](campaign.md).

Show it in a few lines; ask "Save it?".

## 3. Change it

`revise-plan` with `change` in the user's words ("3 weeks, LinkedIn only") or exact `changes`. It returns a new id; the old one can't be saved. Show what changed.

A plan from chat is text posts (blog, email too). One showing pictures, video or carousels: `revise-plan` with exactly "Text only, no pictures or other media." (never the words video, reels or shorts: Bolta would plan video). One with Instagram, TikTok, YouTube or Pinterest: `revise-plan` with a `change` naming the networks left ("LinkedIn and X only"). Read the new plan: still pictures, video, carousels or one of those networks? Save nothing; one line: "This one needs pictures, so it's set up in Bolta: bolta.ai/dashboard/campaigns." Only those networks: no campaign ([settings-formats.md](campaign-settings-formats.md)).

## 4. Save it, not started

`confirm-plan` with the current id and no `switch_on`: it is saved **not started**, writing nothing. It reads up to 5 linked pages: report each failed `sources` row. `plan_not_ready` names what is missing. No planner: `create-content-campaign` ([settings.md](campaign-settings.md)), with a text `content_mix` and step 5's accounts, notes and sources in the same call.

## 5. Accounts, notes, sources

`get-content-campaign`. Then `update-content-campaign` for whatever is missing ([targets.md](campaign-targets.md)): accounts, the real dates and facts in `context_notes`, a page or brand-kit section. Then `analyze-content-campaign-source` for every source not `ready`: only read ones reach the writer.

## 6. Start it, on a separate yes

Show: accounts and when week 1's drafts land. First check `get-content-campaign` `resolved_content_mix`: any key other than `text`, `blog` and `email` means pictures or video, so don't ask; one line: "It has pictures or video, so it's started on its page: bolta.ai/dashboard/campaigns/<id>." Otherwise ask "Start it?". On the yes: `set-content-campaign-status` with `action: "activate"`. Read the reply's `generation` and `get-content-campaign`: `status` must read active and `schedule_status.state` not `needs_accounts`. Say when drafts land, in the workspace clock, with "around" ([settings-status.md](campaign-settings-status.md)).

## 7. Each week: decide the drafts

Hand to [review](review.md): approve the good ones, reject the rest with the user's reason. After week 1, read the set: vague or off-angle means thin notes or the wrong strategy ([strategies.md](campaign-strategies.md)); fix it before week 2 is written.

## 8. Nothing came?

One fresh `get-content-campaign`; the state and last error say why ([why-nothing.md](campaign-why-nothing.md)). Usually never started: [why-nothing-avoid.md](campaign-why-nothing-avoid.md).

## 9. The verdict

After the end date: [verdict.md](campaign-verdict.md). It finishes by itself; don't finish it twice.

## Always

- Two yeses: one to save the plan, one to start it.
- Read the status back after starting; "on" is not "saved".
- Follow the house rules in the Bolta skill.

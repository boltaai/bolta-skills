# A campaign from start to finish

Read when someone runs their first campaign, or asks how campaigns work. Nine steps from a dated event to a verdict. Two yeses: one to save the plan, a separate one to start it.

## 1. The event and its date

Get the subject, the date and one link (an event, launch or offer page). A date missing: ask, it is the one question. An offer: also the real price or discount and its end date; never fill one in. Pick the networks from `list-accounts`.

## 2. Plan it

- **Bolta's planner, where offered:** `plan` with `kind: "campaign"`, `ask` (the user's words with the date), `context` (audience, offer, facts they gave) and `links` (up to 5 pages). It returns a plan with an id: dates, weeks (2 when unsaid, at most 4), strategy, accounts, posts per week, total drafts and notes such as "Left out blog posts". Nothing is created. A question in the result needs its answer first. Read its dates: no date said, it starts tomorrow; "launches Dec 8" can be taken as the start. Step 3 puts the event in the last week.
- **No planner:** write the plan yourself ([campaign.md](campaign.md)): name, strategy, dates with the event in the last week, posts a week × weeks, who writes it.

Show it in a few lines and ask "Save it?".

## 3. Change it

`revise-plan` with `change` in the user's words ("3 weeks, LinkedIn only") or exact `changes`. It returns a new id; the old one can't be saved. Show what changed.

## 4. Save it, not started

`confirm-plan` with the current id and no `switch_on`: the campaign is saved **not started**; nothing is written. It reads up to 5 linked pages itself: report each `sources` row that failed. `plan_not_ready` names what is missing. No planner: `create-content-campaign` ([settings.md](campaign-settings.md)), which can carry the accounts, notes and sources of step 5 in the same call.

## 5. Accounts, notes, sources

`get-content-campaign`. Then `update-content-campaign` for whatever is missing ([targets.md](campaign-targets.md)): accounts, the real dates and facts in `context_notes`, a page or brand-kit section. Then `analyze-content-campaign-source` for every source not `ready`. Only read sources reach the writer.

## 6. Start it, on a separate yes

Show: accounts, when week 1's drafts land, and the cost line for video. Ask "Start it?". On the yes: `set-content-campaign-status` with `action: "activate"`. Read the reply's `generation` and `get-content-campaign`: `status` must read active and `schedule_status.state` not `needs_accounts`. Say when drafts land, in the workspace clock, with "around" ([settings-status.md](campaign-settings-status.md)).

## 7. Each week: decide the drafts

Drafts wait in the review list (`list-inbox-items`, from the team). Hand to [review](review.md): approve the good ones together, turn down the rest with the user's reason so Bolta learns. After week 1, read the set: vague or off-angle means thin notes or the wrong strategy ([strategies.md](campaign-strategies.md)); fix it before week 2 is written.

## 8. Nothing came?

One fresh `get-content-campaign`; the state and last error say why ([why-nothing.md](campaign-why-nothing.md)). Most campaigns that make nothing were never started: [why-nothing-avoid.md](campaign-why-nothing-avoid.md).

## 9. The verdict

After the end date: how it ran, what went out, one next step ([verdict.md](campaign-verdict.md)). It finishes by itself; don't finish it twice.

## Always

- Two yeses: one to save the plan, one to start it.
- Read the status back after starting; "on" is not "saved".
- Follow the house rules in the Bolta skill.

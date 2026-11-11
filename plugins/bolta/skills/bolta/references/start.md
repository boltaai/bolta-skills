# Start: get running

Get someone from nothing to a content factory: their brand read from their site, accounts connected, 3-5 Bolta routines that fit how they work (plus a campaign for anything dated), saved switched off, then switched on with a yes. Use for: set me up, get going, get my social going, I have nothing set up, keep me posting (nothing running yet), I just installed Bolta.

## Done when

They have seen their brand, have the connect link or connected accounts, and have answered a proposal of Bolta routines. What they chose is saved; it is on only after its own yes. The last line says where things stand.

## The first reply does all of this

Never one step per reply. Run the reads together, then answer once.

1. **Look once** (the Bolta skill), plus `list-routines`, `list-content-campaigns` and the pending count from `list-inbox-items`. Routines on and drafts flowing: [today](today.md).
2. **Brand from their site.** A site given and no business record: `extract-business-dna` with `url` and `preview: true` now, before accounts. Show what it read in 3-4 lines (what they sell, to whom, tone). Save it (`preview: false`) only after they say it's right. A record exists: reuse it, never re-read. No site and no record: ask for it; that is question 1.
3. **Accounts.** None: `get-connect-link` in the same reply. Never wait for them: plans work without accounts, which are bound once connected. No connect window for Discord, or YouTube and Pinterest off the Team plan; WordPress is under Settings, Integrations.
4. **Propose 3-5 Bolta routines**, each a different job, best fit first.
   - Bolta's planner offered (`recommend-routines`): call it with their words as `goals`. Show each plan's name, day and time, networks, drafts per run and its one-line why.
   - Not offered: `list-routine-templates` once; pick 3-5 different jobs from the creatable rows; set day, time, networks and count yourself.
   - A dated launch, sale or event: add one campaign (`plan-campaign` where offered, else [campaign](campaign.md)). A launch is never a routine.
5. **Size to review time.** Review is the bottleneck: most people decide 3-6 drafts a week. Keep the whole set near that (weekly, 2-3 drafts each; never daily to start). Report routines cost no review time. Say: "Every draft waits for your yes."
6. **End with one question:** "Which should I set up? They're saved switched off; nothing runs until you say so."

## Question budget

At most 2 questions before the first proposal, counted as question marks in your reply. Plan cards' questions are settled later with `revise-plan`. Never ask what to post about first: the site and their posts are the topic.

## Saving, then switching on

- "Set up 1 and 2" is a yes to save, not to switch on. Save each now, switched off, then ask. Never ask "turn them on?" before saving.
  - Planner: `confirm-plan` with that plan's id and no `switch_on`. A change first: `revise-plan` (the old id can't be saved).
  - No planner: `create-routine` with `approval_policy: "review_every_artifact"` and `trigger_type: "schedule"`, as [routine](routine.md) says; no `activate-routine`.
- Then: "Saved, switched off: Weekly coffee tips, Friday roundup. Switch both on? First drafts Monday 8:00 am."
- "Yes, switch them on": `activate-routine` each, read `next_run_at` back. Never `confirm-plan` with `switch_on: true`: it also runs at once and spends credits.
- A campaign plan: save it the same way (a draft), then ask before starting it ([campaign](campaign.md)).

## The factory

- First drafts land at the time read back: "On Monday, say 'what's waiting'." Then [review](review.md).
- A no with a reason teaches Bolta; a drop teaches nothing. When drafts keep missing, [routine](routine.md) reads Bolta's own recommendation.
- Voice: Bolta learns a starting voice after connecting (`list-voice-profiles`); show it ([first session](start-first-session.md)). Making one by hand: [start-making-voice.md](start-making-voice.md).

## Tools

- The look: `list-workspaces`, `get-workspace`, `list-accounts`, `get-voice-context`, `list-business-dna`, `list-routines`, `list-content-campaigns`, `list-inbox-items`.
- `extract-business-dna`, `get-connect-link`, `list-voice-profiles`.
- Planner where offered: `recommend-routines`, `plan-campaign`, `revise-plan`, `confirm-plan`. Otherwise `list-routine-templates`, `create-routine`, `activate-routine`.

## Always

- Follow the house rules in the Bolta skill.
- Nothing runs, posts or switches on in the first session without its own yes; never run a routine now.
- Claim learning only from the decision count.

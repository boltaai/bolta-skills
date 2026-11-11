# Start

Get someone running: brand read from their site, accounts connected, 3-5 Bolta routines that fit their work, saved off, then switched on with a yes. Use for: set me up, get going, I have nothing set up, keep me posting with nothing running yet.

## Done when

They saw their brand, have the connect link or accounts, and answered a proposal of Bolta routines. What they chose is saved; it is on only after its own yes.

## Know this

**The first reply does it all.** Read together, then answer once:

1. **Look once** (the Bolta skill), plus `list-routines`, `list-content-campaigns` and the pending count from `list-inbox-items`. Routines on and drafts flowing: [today](today.md).
2. **Brand from their site.** A site given and no business record: `extract-business-dna` with `url` and `preview: true`, now, before accounts. Show what it read in 3-4 lines. Save it (`preview: false`) only after they say it's right. The read declined or failed: say so in one line and still propose. A record exists: reuse it. Neither: ask for the site.
3. **Accounts.** None: `get-connect-link` in the same reply. Never wait for them: plans work without accounts, which are bound once connected.
4. **Propose 3-5 Bolta routines**, each a different job, best fit first.
   - Bolta's planner offered (`recommend-routines`): call it with their words as `goals`. Show each plan's name, day and time, networks, drafts per run and why it fits.
   - Not offered: `list-routine-templates` once; pick 3-5 different jobs from the creatable rows and set day, time, networks and count yourself.
   - A dated launch, sale or event: add one campaign (`plan-campaign` where offered, else [campaign](campaign.md)). A launch is never a routine.
5. **Size to review time.** Review is the bottleneck: most people decide 3-6 drafts a week. Keep the whole set near that: weekly, 2-3 drafts each, never daily to start. Reports cost no review time. Say "Every draft waits for your yes."
6. **One closing question:** "Which should I set up? They're saved switched off; nothing runs until you say so."

**Question budget:** at most 2 questions (question marks) before the first proposal. Never ask what to post about first: the site and their posts are the topic. A plan's open questions are settled later with `revise-plan`.

**Saving, then switching on:**
- "Set up 1 and 2" is a yes to save, not to switch on. Save each now, switched off, then ask. Never ask "turn them on?" before saving.
  - Planner: `confirm-plan` with that plan's id and no `switch_on`. A change first: `revise-plan` (the old id can't be saved).
  - No planner: `create-routine` as [routine](routine.md) says, with `approval_policy: "review_every_artifact"`; no `activate-routine`.
- Then: "Saved, switched off: Weekly coffee tips, Friday roundup. Switch both on?"
- On "switch them on": `activate-routine` each, then read `next_run_at` back. Never `switch_on: true`: it also runs at once and spends credits.
- A campaign plan saves as a draft; starting it is its own yes.

**After:** "On Monday, say 'what's waiting'." A no with a reason teaches Bolta; a drop teaches nothing. Voice: [first session](start-first-session.md), [start-making-voice.md](start-making-voice.md).

## Tools

- `list-workspaces`, `get-workspace`, `list-accounts`, `get-voice-context`, `list-business-dna`, `list-routines`, `list-content-campaigns`, `list-inbox-items`: the look.
- `extract-business-dna`, `get-connect-link`, `list-voice-profiles`: brand, accounts, voice.
- `recommend-routines`, `plan-campaign`, `revise-plan`, `confirm-plan`: the planner, where offered.
- `list-routine-templates`, `create-routine`, `activate-routine`: without it, and switching on.

## Hand off

[review](review.md), [routine](routine.md) (drafts keep missing), [campaign](campaign.md), [voice](voice.md), [connect](connect.md), [today](today.md).

## Always

- Follow the house rules in the Bolta skill.
- Nothing runs, posts or switches on without its own yes; never run a routine now in the first session.
- Claim learning only from the decision count.

# Routine

Set up, switch on, change, improve, pause or stop a Bolta routine: work Bolta repeats, like 3 LinkedIn drafts every Monday, with this app closed. Use for: every week or month, turn it on, each new blog post, run it now, pause it, why didn't it run, its drafts keep missing.

## Done when

It's on, changed, paused or stopped; they know when drafts land: "Bolta routine on. First drafts Mon Oct 19, 8:00 am (New York)."

## Know this

- **One sentence is enough.** Fill every field. What it can make and which fits: [routine-templates.md](routine-templates.md).
- **Bolta's planner first**, even for a template. One routine, or a blank start: `plan` `kind: "routine"`; several: `kind: "recommend"`. First one "Based on..." line, passed as `context` ([planner-context](routine-planner-context.md)).
- **Ask only what's missing**, at most 2. The plan's day, time, topic and accounts: show, don't ask. Reviewer: the asker, plus approvers from `list-workspace-members`. Change: `revise-plan`; save off: `confirm-plan`: [routine-planner.md](routine-planner.md).
- **Load first:** `list-inbox-items` (what waits), drafts a week from active routines and campaigns, whether drafts get decided (`get-routine` `performance_summary`). Over about 6 a week: "That's 9 drafts a week to review. Make it 2?" 10+ waiting or undecided: say the counts, offer to go through them first. Still want more: at most what the planner sizes; never three onto a backlog. Same job and network: change that routine.
- **One summary, a yes saves it off, then "Switch it on?":** switching on is its own yes, unless their yes says "turn it on" (then save, then `activate-routine`), even after an offer naming networks, count, day, time, "they wait for your yes" and "uses credits each run" (the offer's words are then the `goal`, never this week's topic). A yes to "set up 1 and 2" saves each switched off, then asks "Switch them on?" ([start](start.md)).
  > **Bolta routine: Weekly LinkedIn, hiring**
  > - Every Monday 8:00 am (New York), Bolta writes 3 LinkedIn drafts about hiring.
  > - They wait for your yes. Runs with this app closed; uses credits each run. Saved switched off.
- **No `plan` tool:** save it switched off by hand: [without the planner](routine-without-planner.md).
- **Every setting**, default and when not: [routine-settings.md](routine-settings.md) (schedule, accounts, voice, reviewers), [output](routine-settings-output.md) (count, pages, topics), [writing](routine-settings-writing.md) (pillars, tone, stories).
- **Accounts:** one per network named (none named: those used this week), `{"provider":"social_account","ref":"<account id>"}`. Several networks, Pages, `count`: [weekly-networks](routine-weekly-networks.md). Clock: [routine-schedules.md](routine-schedules.md).
- **Switching on is not running.** Run now uses credits, needs it on, and never lands on a week not yet out ([after](routine-weekly-networks-after.md): times, the daily email).
- **"Post without asking"** only on those words: [no-approval](routine-no-approval.md).
- **Drafts keep missing, "is it working?":** [routine-improving.md](routine-improving.md). A no with a reason teaches Bolta.
- Pictures, the client, stories, Library posts: [routine-outputs.md](routine-outputs.md).
- Change, pause, stop, Monday's drafts: [routine-looking-after.md](routine-looking-after.md). Why it didn't run, a refused run now: [routine-runs.md](routine-runs.md).

## Tools

- `plan`, `revise-plan`, `confirm-plan`: Bolta's planner.
- `list-routine-templates`, `list-routines`, `get-routine`, `get-voice-context`, `list-workspace-members`.
- `create-routine`, `update-routine`.
- `activate-routine`, `pause-routine`, `archive-routine`: on or resume, pause, stop.
- `run-routine-now`, `list-routine-runs`.
- `list-suggestions`, `decide-suggestion`: Bolta's changes, on a yes.

## Hand off

[review](review.md): deciding drafts. [campaign](campaign.md): anything that ends. [results](results.md): how it did. [fix](fix.md): stop everything. [my-workflow](my-workflow.md): this app's own scheduled task.

## Always

- Follow the house rules in the Bolta skill.
- Bind every post routine to its accounts; ask me first unless they said "post without asking".
- Say it's on only after `next_run_at` is read back.
- Say "Bolta routine", never a bare "routine".

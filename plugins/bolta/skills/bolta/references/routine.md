# Routine

Set up, switch on, check, change, pause or stop a Bolta routine: work Bolta repeats for you, like 3 LinkedIn drafts every Monday, even with this app closed. Use for: every week or month, turn it on, try my routine, each new blog post, run it now, pause it, why didn't it run, its drafts keep missing.

## Done when

It's on, changed, paused or stopped; they know when drafts land: "Bolta routine on. First drafts Mon Oct 19, 8:00 am (New York)."

## Know this

- **One sentence is enough.** Fill every field. Made from: [references/routine-templates.md](routine-templates.md).
- **Load check first:** drafts a week from active Bolta routines and campaigns, and what already waits (`list-inbox-items`). Over about 6 a week: "That's about 9 drafts a week to review. Most people decide 3-6. Make it 2?" 10+ waiting, even if asked for more: add nothing; name the count, offer to go through them first or one small change. A duplicate: change that one.
- **One summary, then "Turn it on?"** Skip it only after a yes to an offer naming the networks, count, day, time, "they wait for your yes" and "uses credits each run"; the offer's words are then the `goal`, never this week's topic. A yes to set up a proposal ("set up 1 and 2") saves each switched off, then asks "Switch them on?" ([start](start.md)).
  > **Bolta routine: Weekly LinkedIn, hiring**
  > - Every Monday 8:00 am (New York), Bolta writes 3 LinkedIn drafts about hiring.
  > - They wait for your yes. Runs on Bolta even with this app closed; uses credits each run.
- **On yes:** create with `name`, `goal` (their words), `template_key`, `trigger_type: "schedule"`, `schedule: {"interval":"weekly","day":"monday","time":"08:00"}`, the workspace `timezone`, `approval_policy: "review_every_artifact"`, `output_config: {"artifact_type":"post","count":3,"platforms":["linkedin"]}`, `instructions`: their words plus "Never invent facts, numbers, prices or dates." Switch on, read back: "On Monday, say 'what's waiting'."
- **Accounts:** one per network named (none named: those used this week). `source_bindings: [{"provider":"social_account","ref":"<account id>"}, ...]`. `count` is per run, across networks.
- Time zone, monthly, weekdays: [references/routine-schedules.md](routine-schedules.md).
- **Switching on is not running.** Run now does; it uses credits and needs it on. Asked to try one that's off, say so first: "Weekly recap is switched off, so it has never run. Switch it on and run it once now?"
- **"From my blog":** `output_config.source_urls`, one URL. An unchanged page skips that run; say so.
- **"Post without asking"** only on those words: two Bolta checks; some brands refuse it ([looking after](routine-looking-after.md)).
- **Its drafts keep missing** (no's for one reason): first read Bolta's recommendation: `list-routine-recommendations` and `list-bolta-suggestions`, where offered. Name the pattern ("Your last 3 were turned down as too long"), give Bolta's fix and ask "Want me to apply it?" Apply only on a yes (`decide-routine-recommendation`, `decide-bolta-suggestion`). Nothing there: offer one change of your own.
- Pictures, straight to the client, stories, Library posts: [references/routine-outputs.md](routine-outputs.md).
- Change, pause, stop, Monday's drafts, voice: [references/routine-looking-after.md](routine-looking-after.md). Why it didn't run, a refused run now: [references/routine-runs.md](routine-runs.md).

## Tools

- `list-routine-templates`, `list-routines`, `get-routine`: what's possible, what exists, next run.
- `create-routine`, `update-routine`: set up, change.
- `activate-routine`, `pause-routine`, `resume-routine`, `archive-routine`: on, pause, resume, stop for good.
- `run-routine-now`, `list-routine-runs`: run now; what ran.

## Hand off

[review](review.md): deciding drafts. [campaign](campaign.md): anything that ends. [results](results.md): how it did. [fix](fix.md): stop everything. [my-workflow](my-workflow.md): this app's own scheduled task.

## Always

- Follow the house rules in the Bolta skill.
- Bind every post routine to its accounts; ask me first unless they said "post without asking".
- Say it's on only after `next_run_at` is read back.
- Say "Bolta routine", never a bare "routine".

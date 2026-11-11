# Routine

Set up, switch on, check, change, pause or stop a Bolta routine: work Bolta repeats for you, like 3 LinkedIn drafts every Monday, even with this app closed. Use when someone says every week or month, keep me posting, turn it on, try my routine, each new blog post, run it now, pause my routine, or why didn't my routine run.

## Done when

It's on, changed, paused or stopped, and they know when drafts land: "Bolta routine on. First drafts Mon Oct 19, 8:00 am (New York)."

## Know this

- **One sentence is enough.** Reuse reads; fill every field. Made from: [references/routine-templates.md](routine-templates.md).
- **Load check first:** drafts a week from active Bolta routines and campaigns. Over about 6: "You'd have about 9 drafts a week to review. Most people manage 3-6. Make it 2?" Duplicate: offer to change it.
- **One summary, then "Turn it on?"** Skip it only after a yes to an offer naming the networks, count, day, time, "they wait for your yes" and "uses credits each run"; the offer's words are then the `goal`, never this week's topic.
  > **Bolta routine: Weekly LinkedIn, hiring**
  > - Every Monday 8:00 am (New York), Bolta writes 3 LinkedIn drafts about hiring.
  > - They wait for your yes. Runs on Bolta even with this app closed; uses credits each run.
- **On yes:** create with `name`, `goal` (their words), `template_key`, `trigger_type: "schedule"`, `schedule: {"interval":"weekly","day":"monday","time":"08:00"}`, the workspace `timezone`, `approval_policy: "review_every_artifact"`, `output_config: {"artifact_type":"post","count":3,"platforms":["linkedin"]}`, `instructions`: their words plus "Never invent facts, numbers, prices or dates." Switch on, read back, end: "On Monday, say 'what's waiting'."
- **Accounts:** one per network named (none named: those used this week); ask only if two on one network fit. `source_bindings: [{"provider":"social_account","ref":"<account id>"}, ...]`, objects, not strings; unbound, Bolta uses any connected account. `count` is per run, across networks.
- Time zone, monthly, weekdays, spread-out days: [references/routine-schedules.md](routine-schedules.md).
- **Switching on is not running.** Run now does; it uses credits and needs it on. Asked to try one that's off: "Switch it on and run it once now?"
- **"From my blog":** `output_config.source_urls`, exactly one URL. An unchanged page skips that scheduled run: say so first.
- **"Post without asking"** only on those words: two Bolta checks. Review mode or a manual or assisted brand refuses it; client sign-off still holds drafts for review.
- Pictures, drafts straight to the client, stories, Library posts: [references/routine-outputs.md](routine-outputs.md).
- Change, pause, stop, Monday's drafts, voice, ideas: [references/routine-looking-after.md](routine-looking-after.md). "Why didn't it run?", a failed run, a refused run now: [references/routine-runs.md](routine-runs.md).

## Tools

- `get-workspace`, `list-accounts`: time zone; accounts to bind.
- `list-routine-templates`, `list-routines`, `get-routine`: what's possible, what exists, next run.
- `create-routine`, `update-routine`: set up, change.
- `activate-routine`, `pause-routine`, `resume-routine`, `archive-routine`: on, pause, back on, stop for good.
- `run-routine-now`, `list-routine-runs`: run now; what ran.
- `list-inbox-items`: a run's drafts.

## Hand off

[review](review.md): deciding drafts. [post](post.md): posts now. [campaign](campaign.md): anything that ends. [results](results.md): how it did. [fix](fix.md): stop everything. [connect](connect.md): disconnected accounts. [my-workflow](my-workflow.md): an app scheduled task (Gmail, Notion, Drive or Slack in the chain).

## Always

- Follow the house rules in the Bolta skill.
- Bind every post routine to its accounts, one per network; ask me first unless they said "post without asking".
- Say it's on only after `next_run_at` is read back.
- Say "Bolta routine", never a bare "routine".

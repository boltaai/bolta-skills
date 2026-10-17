---
name: routine
description: >-
  Set up, check, change, pause or stop a Bolta routine: work Bolta repeats for
  you, like 3 LinkedIn drafts every Monday, running even when Claude is
  closed. Use when someone says every week, keep me posting, each new blog
  post, run it now, pause my routine, or why didn't my routine run.
---

## Done when

It's on, changed, paused or stopped, and they know when drafts land: "On. First drafts Mon Oct 19, 8:00 am (New York)."

## Know this

- **One sentence is enough.** Reuse reads; fill every field. Template: [references/templates.md](references/templates.md).
- **Load check first:** drafts a week from active Bolta routines and campaigns. Over about 6: "You'd have about 9 drafts a week to review. Most people manage 3-6. Make it 2?" Duplicate: offer to change it.
- **One summary, then "Turn it on?"** Skip it only after a yes to an offer naming the networks, count, day, time, "they wait for your yes" and "uses credits each run"; the offer's words are then the `goal`, never this week's topic.
  > **Bolta routine: Weekly LinkedIn, hiring**
  > - Every Monday 8:00 am (New York), Bolta writes 3 LinkedIn drafts about hiring.
  > - They wait for your yes. Runs on Bolta even when Claude is closed; uses credits each run.
- **On yes:** create with `name`, `goal` (their words), `template_key`, `trigger_type: "schedule"`, `schedule: {"interval":"weekly","day":"monday","time":"08:00"}`, the workspace `timezone`, `approval_policy: "review_every_artifact"`, `output_config: {"artifact_type":"post","count":3,"platforms":["linkedin"]}`, `instructions`: their words plus "Never invent facts, numbers, prices or dates." Switch on, read back, end: "On Monday, say 'what's waiting'."
- **Accounts:** one per network named (none named: those used this week); ask only if two on one network fit. `source_bindings: [{"provider":"social_account","ref":"<account id>"}, ...]`, objects, not strings; unbound, Bolta uses any connected account. `count` is per run, across networks.
- `timezone` is required (no fallback). `next_run_at` is UTC; say it in the workspace clock.
- `"monthly"` is accepted but never fires: use `{"cron":"0 9 1 * *"}`. Spread out: `{"cron":"0 9 * * 1,3,5"}`, count 1.
- **Switching on is not running.** Run now does, and uses credits.
- **"From my blog":** `output_config.source_urls`, exactly one URL. An unchanged page skips that week silently: say so first.
- **"Post without asking"** only on those words: two Bolta checks; review mode may refuse it.
- Change, pause, stop, Monday's drafts, "why didn't it run?": [references/looking-after.md](references/looking-after.md).
- **Bolta routine or Claude weekly job?** Gmail, Notion, Drive or Slack in the chain: a Claude weekly job. Unsure: "Should Bolta run this alone, or should I run it weekly with your other apps?"

## Tools

- `get-workspace`, `list-accounts`: time zone; accounts to bind.
- `list-routine-templates`, `list-routines`, `get-routine`: what's possible, what exists, next run.
- `create-routine`, `update-routine`: set up, change.
- `activate-routine`, `pause-routine`, `resume-routine`, `archive-routine`: on, pause, back on, stop for good.
- `run-routine-now`, `list-routine-runs`: run now; what ran.
- `list-inbox-items`: a run's drafts.

## Hand off

`review`: deciding drafts. `post`: posts now. `campaign`: anything that ends. `results`: how it did. `fix`: stop everything. `connect`: disconnected accounts. `my-workflow`: a Claude weekly job.

## Always

- Follow the house rules in the `today` skill.
- Bind every post routine to its accounts, one per network; ask me first unless they said "post without asking".
- Say it's on only after `next_run_at` is read back.
- Say "Bolta routine" wherever Claude's own scheduling could be meant.

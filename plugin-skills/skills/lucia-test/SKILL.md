---
name: lucia-test
description: >
  The end-to-end acceptance run: understand the brand, inspect its presence,
  publish something useful, discover third-party conversations, reply to them,
  work the inbound inbox, verify every external action, review the results, and
  finally save the whole thing as a scheduled routine. Use this skill when the
  user asks to "run the Lucia test", "do a full pass", "prove the whole loop
  works", "end to end test", "exercise everything", or is evaluating whether
  Bolta can be operated entirely through an AI client. Composite — it delegates
  each leg to the focused skills.
---

# The Lucia Test

One run that exercises Bolta's whole surface through MCP and reports honestly on
what worked, what is platform-limited, and what is missing. It is an acceptance
benchmark, not a demo: **a clean report that names three real gaps is a better
outcome than a green tick that hides them.**

## When to use
Evaluating the product end to end, verifying a deploy, or proving the
skills-first architecture: an external AI client performing sophisticated social
operations with no Agent configured by hand.

## The two milestones
1. **Interactive.** Every leg below completes through MCP tools alone.
2. **Durable.** The same outcome is saved as a routine and runs server-side on a
   schedule — without creating or configuring an Agent.

Report both. The second is the one that proves the architecture.

## Skills this delegates to
| Leg | Skill |
|-|-|
| Publish | social-publishing |
| Reddit discovery + reply | reddit-engagement |
| Threads / Bluesky / Mastodon / X / LinkedIn | cross-platform-engagement |
| Inbound comments and mentions | social-inbox |
| Results | analytics-review |

Read those skills' failure handling rather than re-deriving it here.

## Prerequisites
- `workspace_id` via `list-workspaces`; auth is automatic.
- **Use a workspace whose connected accounts are safe to post from.** This run
  publishes real content and leaves real public replies. Confirm with the user
  which accounts are in scope before anything goes out, and offer a draft-only
  variant that stops before every publish step.
- Owner/admin/creator for the publishing and reply legs.

## Workflow

### 1. Understand the brand
`get-voice-context(workspace_id)` and `get-business-dna(workspace_id)`. Summarize
in two sentences what this brand does, who for, and how it sounds. If the voice
context is empty, say so — everything downstream will be generic and that is a
finding, not a failure to work around.

### 2. Inspect the current presence
`list-accounts`, `list-workspace-posts`, `list-scheduled-posts`,
`list-engagement-capabilities`. Report what is connected, what has been posted
recently, what is queued, and — from the capability matrix — what each platform
can actually do. This is the row-by-row basis for the matrix at the end.

### 3. Publish something useful
Via **social-publishing**. One genuinely useful post, in voice, to an in-scope
account. Confirm before it goes out. Verify with `get-post`.

### 4. Discover third-party conversations
Via **reddit-engagement** (Reddit) and **cross-platform-engagement** (Threads,
Bluesky, Mastodon). Record how many opportunities each platform returned. For X
and LinkedIn, record that discovery is unavailable and take a supplied URL
instead — that is the correct result, not a failure.

### 5. Reply to third-party posts
Draft, get approval, publish, and **verify the canonical URL** on each. One
reply per platform is enough; the point is proving the path, not volume. Apply
the same judgement as the underlying skills — if no thread on a platform deserves
a reply, record that instead of forcing one.

### 6. Inspect inbound
Via **social-inbox**: `list-inbox-items`, summarized by source and platform.

### 7. Reply to inbound
Answer at least one inbound comment or mention, with approval, and verify it
landed. If the inbox is empty, say so — it is a valid state, not a gap.

### 8. Verify every external action
For each public thing this run did, produce a link:
- posts → `get-post`, plus the platform URL where published;
- outbound replies → `get-engagement-status`, canonical URL;
- inbound replies → confirmed send.

**An action with no link is not verified.** Do not report it as done.

### 9. Review results
Via **analytics-review**, scoped to this run's window. Acknowledge openly that
minutes-old posts have no meaningful data — the point is that the pipeline
reports, not that the numbers are interesting yet.

### 10. Save it as a routine — the milestone
This is the step the whole test exists for. Without creating or touching an
Agent:

1. `list-routine-templates()` — show the user the library. This is the whole
   discovery step; the runtime contracts the templates bind to are server-side
   and deliberately not on this surface.
2. `create-routine(template_key="reddit_engagement", name=...,
   goal=<their words>, trigger_type="schedule", schedule={"cron": "0 10 * * 1-5"},
   timezone=..., instructions=..., source_bindings=[...],
   output_config={artifact_type: "reply", count: 3, topics: [...]})`.
3. `activate-routine(routine_id)`.
4. `run-routine-now(routine_id)` to prove dispatch, then
   `list-routine-runs(routine_id)` to see the run.

Then state plainly: *"Run this routine every weekday morning and require
approval for replies"* was satisfied with no Agent configured.

Offer to `pause-routine` afterwards if this was only a test.

### 11. Report the matrix
Finish with a table — one row per capability, filled from what actually happened
in **this** run, not from documentation:

| Capability | Worked? | Evidence | Gap |
|-|-|-|-|
| Understand brand | | voice context loaded | |
| Inspect presence | | N accounts, M posts | |
| Publish | | post URL | |
| Reddit discovery | | N opportunities | |
| Reddit reply | | canonical URL | |
| Threads discovery / reply | | | |
| Bluesky discovery / reply | | | |
| Mastodon discovery / reply | | | |
| X reply (URL supplied) | | | no keyword discovery |
| LinkedIn comment (URN supplied) | | | no public search |
| Inbound comments | | | |
| Inbound mentions | | | |
| Analytics | | | |
| Verification | | every link above | |
| Save as routine | | routine id + run id | |
| **Agent required?** | | | should be "no" throughout |

## Definition of done
- Every row in the matrix is filled from this run's evidence.
- Every public action has a link.
- A routine exists, was activated, and dispatched at least one run.
- No Agent was created or configured.
- Gaps are named as gaps — platform limits distinguished from Bolta limits.

## Failure handling
Each leg's own skill owns its errors. At this level:
- A leg that fails does not stop the run. Record it, move to the next, and report
  it in the matrix. A partial pass with an honest matrix is the deliverable.
- Never simulate or narrate a step you did not actually execute.
- Never report an action as verified without a link.
- If the user stops approving mid-run, stop publishing and finish read-only.

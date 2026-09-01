---
name: analytics-review
description: >
  Read what actually happened — reach, engagement, follower movement, which posts
  worked — and say what to do about it. Use this skill when the user asks "how did
  we do", "show my analytics", "what performed best", "is this working", "weekly
  recap", "which platform is growing", or wants performance interpreted rather
  than dumped. Read-only: it never creates, schedules or publishes anything. To
  act on the findings, hand off to social-publishing.
---

# Analytics Review

Turn numbers into a decision. The failure mode of this skill is producing a
dashboard in prose — a wall of metrics with no claim. Every section should end in
something the user could act on or stop worrying about.

## When to use
Any performance question. Also the natural follow-up after a week of publishing:
"did that work?"

## Tools this skill uses
| Tool | Why |
|-|-|
| `list-workspaces` | Resolve `workspace_id` once. |
| `list-accounts` | Which accounts exist and are connected. |
| `cross-platform-analytics` | The headline: totals and per-platform comparison. |
| `get-account-analytics` | One account in depth, including the daily series. |
| `list-account-insights` | Audience and profile-level insight where the platform provides it. |
| `list-workspace-posts` | The posts behind the numbers. |
| `get-post` | Full detail on a specific top or bottom performer. |
| `list-engagements` | Outbound replies sent, for engagement-effort context. |
| `list-routine-runs` | Whether the automation that was supposed to produce content actually ran. |

## Prerequisites
- `workspace_id` via `list-workspaces`; auth is automatic, never ask for a key.
- Read-only scope is enough. This skill must not call any write tool.
- Connected accounts with some history. A three-day-old account has no trend and
  saying so is more useful than computing one.

## Workflow

### 1. Establish the window
Ask, or infer from the request, and **state it explicitly** in the output. "Last
7 days" and "since the launch" produce different stories from the same data, and
an unlabeled comparison is the easiest way to mislead someone.

### 2. Get the shape
`cross-platform-analytics(workspace_id, ...)` for totals and the per-platform
split. This tells you where to look, not what to conclude.

### 3. Go deeper where it matters
`get-account-analytics(workspace_id, account_id)` for the accounts that moved —
up or down. `list-account-insights` where audience data exists. Do not pull every
account in depth; pull the ones with a story.

### 4. Tie numbers to posts
`list-workspace-posts(workspace_id)` over the window, and `get-post` on the top
and bottom performers. A number with no post attached is not a finding. What you
want is "the two posts that outperformed were both concrete customer stories" —
a claim someone can act on.

### 5. Check the inputs before blaming the output
If output was thin, the cause is often upstream:
- `list-routine-runs(routine_id)` — did the routine that was
  supposed to publish actually run, or fail, or sit awaiting approval?
- `list-engagements(workspace_id)` — was any outbound engagement actually sent?

"Reach fell because nothing was published for nine days" is a better answer than
a paragraph about the algorithm.

### 6. Say what it means
Structure the report as:
- **Headline** — one sentence. What happened, in the user's terms.
- **What moved** — two or three specifics with numbers, each tied to a cause you
  can point at.
- **What worked** — the posts, with links, and what they had in common.
- **What did not** — same, without editorializing.
- **What to do next** — at most three concrete suggestions.

### 7. Be honest about the data
- Say when a sample is too small to conclude from. Two posts is not a trend.
- Say when a platform's API simply does not report a metric, rather than
  reporting zero.
- Do not compare a partial current period against a complete previous one
  without flagging it.
- Never invent a benchmark ("industry average is 3%") — you do not have one.

## Definition of done
- The window is stated.
- Every claim traces to a number or a post the user can open.
- Small samples and missing metrics are labeled, not smoothed over.
- The user has at most three next actions, not a list of twelve.
- Nothing was created, scheduled or published.

## Failure handling
- No connected accounts → say so; offer `get-connect-link`.
- Analytics not yet synced for an account → report it as pending rather than
  reporting zeros as a result.
- A platform that does not expose a metric → name the platform and the gap.
- Permission error → `get-my-capabilities`; a viewer role can read analytics, so
  a refusal here usually means the wrong workspace.

## Save this as a routine
For a standing recap:
1. `list-routine-templates()` → `performance_digest`,
   `account_performance_deep_dive` or `best_time_to_post_report`.
2. `create-routine(...)` with a weekly or monthly schedule.
3. `activate-routine(...)`.

Reporting routines produce a report artifact into the Reports dashboard and mail
it to workspace admins. Nothing they do is public, which is why they are a safe
first routine for someone nervous about automation.

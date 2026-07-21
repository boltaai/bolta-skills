---
name: bolta-analytics-report
description: >
  Report on social-media performance from Bolta's analytics. Use this skill when the
  user asks "how are my posts doing", "how did that post do", "show my analytics",
  "performance report", "how did LinkedIn do this month", "which account is growing",
  "engagement over the last 30 days", "what's my best-performing account/post", or wants
  any rollup, comparison, or trend of reach/engagement across their posts or connected
  accounts. Not for reading the review queue
  (use bolta-review-queue) or writing content (use bolta-draft-post).
---

# Bolta Analytics Report

Turn Bolta's analytics into a clear performance narrative. Pick the right tool for the
question — a workspace-wide rollup, a per-account snapshot, or one account's time series —
default the window sensibly, and summarize what's working, what's declining, and what to do
next. This is the same data that backs Bolta's analytics widget.

## When to use
Any request to see, compare, or explain how content or accounts are performing.

## Tools this skill uses
| Tool | Why |
|-|-|
| `list-workspaces` | Resolve `workspace_id` if unknown. |
| `list-accounts` | Get connected accounts + their `account_id`s (needed for per-account series). |
| `cross-platform-analytics` | Workspace-wide rollup across all platforms. |
| `list-account-insights` | Per-account snapshot for every connected account in one call. |
| `get-account-analytics` | Time series for one specific account. |
| `list-workspace-posts` | **Post-level performance**: `status=published` + a date window + `include_metrics=true` attaches per-platform engagement (views, likes, comments, reposts) and `published_at` to each post. `metrics_platforms` narrows the breakdown. Paginated — default `limit` is 50 (max 200). |

## Prerequisites
- `workspace_id` — resolve once via `list-workspaces`, reuse for every call. Auth is automatic
  via the Bolta connector's OAuth grant — never ask for an API key.
- These are all read-only tools — no confirmation or write permission needed. (Elsewhere,
  default new content to Draft; confirm before publish/delete.)

## Choosing the right tool
Map the question to the tool before calling anything:
- **"How is everything doing?" / whole-workspace rollup** → `cross-platform-analytics`.
- **"Which account is best / growing?" / compare accounts** → `list-account-insights`
  (one snapshot per account, ideal for ranking and comparison).
- **"How did <one account> do?" / trend for a single account** → `get-account-analytics`,
  which needs an `account_id` from `list-accounts`.
- **"How did my post(s) do?" / best-performing posts** → `list-workspace-posts` with
  `status=published`, a `start_date`/`end_date` window, and `include_metrics=true` — each
  post comes back with per-platform views/likes/comments/reposts.

## Workflow

### 1. Resolve the workspace
Call `list-workspaces` and use the active workspace's `id`.

### 2. Set the window
Every analytics tool takes `days`. If the user names a period ("this month", "last 30 days",
"past week"), use it; otherwise default to **30** and state the window in your answer so the
number is never ambiguous.

### 3. Pull the right data
- **Workspace rollup:** `cross-platform-analytics(workspace_id, days)`.
- **Account comparison:** `list-account-insights(workspace_id, days)`.
- **Single-account trend:** first `list-accounts(workspace_id)` (optionally filter by
  `platform`) to get the `account_id`, then
  `get-account-analytics(workspace_id, account_id, days)`.
- **Post-level performance:** `list-workspace-posts(workspace_id, status="published",
  start_date, end_date, include_metrics=true)` — rank posts by engagement, name the winners,
  and quote the actual content that performed. **Pass an explicit `limit`** (default is 50,
  max 200) and check the pagination fields in the response — a "best posts" ranking built
  on the default silently covers only the first page. If the window holds more posts than
  one page, page through (`page=2, 3, …`) before declaring winners.
For a full report you may combine these — a rollup for the headline, per-account insights for
the breakdown, and post metrics for "which posts drove it".

**Growth-field caveat:** the `growth` / `growth_rate` number on account insights is currently
**unreliable** — live testing returned 0.0% on all 8 connected accounts while followers and
engagement varied (suspected broken calculation, under investigation). Do not rank accounts
by it or build "which account is growing" conclusions on it; if asked about growth, lean on
follower/engagement deltas over the window instead, and flag any `growth` figure you do quote
as possibly wrong.

**Freshness honesty:** post metrics sync **nightly**. For posts published less than ~24h ago,
say metrics may not have synced yet — zeros there mean "not synced", not poor performance.
Never present an unsynced zero as a real result.

### 4. Synthesize an insights narrative
Don't just dump numbers. Report:
- **Headline** — overall reach/engagement for the window, with the window stated.
- **What's working** — top accounts/platforms and standout posts.
- **What's declining** — accounts or metrics trending down.
- **Recommendations** — concrete, voice-aware next moves (post more where engagement is
  climbing, revisit formats that are slipping).
Mention that this is the same data behind Bolta's analytics widget, so it matches the app.

## Failure handling
- No accounts connected → say so; there's nothing to report until an account is connected.
- A platform returns zeros / no data → note it as "no data for this window" rather than
  reporting a real zero; a platform's metrics may not be linked yet.
- Account not found for a per-account series → re-run `list-accounts` to get a current
  `account_id`.

## Example
User: "How did LinkedIn do this month, and which account is growing?"
1. `list-workspaces` → workspace_id.
2. Window = current month (~30 days), stated explicitly.
3. `list-account-insights(workspace_id, days=30)` → ranks all accounts; LinkedIn is up 18%,
   X is flat, Threads down 12%.
4. For the LinkedIn detail: `list-accounts(workspace_id, platform="linkedin")` → account_id,
   then `get-account-analytics(workspace_id, account_id, days=30)` for the trend.
5. Narrative: "Over the last 30 days LinkedIn led growth (+18% engagement), driven by your
   long-form posts; Threads slipped 12%. Recommend doubling down on LinkedIn long-form and
   revisiting Threads cadence. (Same data as your analytics widget.)"

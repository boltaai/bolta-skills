# Why nothing went out

Read from [why-nothing.md](campaign-why-nothing.md) when a campaign finished, or is running, and nothing went out. Both fields come from one fresh `get-content-campaign`. "Nothing went out" is nearly always waiting for your yes.

## 1. Nothing went out? `results.outcome`

- `no_results_yet`: early. Nothing out yet; the window is still open.
- `in_progress`: going out, more to come.
- `published`: finished, and posts went out.
- `published_nothing`: finished, and nothing went out. Give the reason below.

## 2. The reason: `results.outcome_reason`

Bolta names the first thing that stopped it.

- `no_accounts_connected`: the brand has no accounts at all, so nothing could go out. [connect](connect.md).
- `runs_failed`: every time Bolta tried to write, it failed. Say the last error.
- `not_started`: it never started. Start it, or check the start date.
- `nothing_generated`: Bolta ran but wrote no drafts. Check the mix and the last error.
- `quality_blocked`: Bolta's quality check held the drafts back; they need a human edit before they can go. [review](review.md).
- `publishing_failed`: sends failed and nothing went out, usually a disconnected account. [connect](connect.md).
- `awaiting_approval`: the drafts are waiting for your yes. The usual answer. [review](review.md).
- `nothing_approved`: drafts were turned down or are still plain drafts; none got a yes. Two weeks of that: wrong strategy or thin context ([strategies.md](campaign-strategies.md)).
- `not_sent_yet`: approved, and their times haven't come yet.
- `unknown`: Bolta can't tell. Look at the campaign's posts.

## Always

- Follow the house rules in the Bolta skill.

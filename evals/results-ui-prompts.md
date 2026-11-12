# UI prompts: what bolta.ai's "In your AI app" panels hand users

Run Nov 11-12, 2026, Claude Code 2.1.322: `sh tools/run_plugin_evals.sh uiprompts --runs 3`, 18 cases × 3 runs, with no Bolta checks hooks (as in ChatGPT and claude.ai chat). Judge: sonnet.

## Prompts under test

- **A. Brand from a website.** The live "Set up Brand in your AI app" text (from owner screenshots), for DevConsole / devconsole.example, Harbor Physio and Ferro Bikes.
- **B. Brand from notes.** "Use the brand notes I share to draft a brand profile for {Brand}. Show it to me before saving it in Bolta." Used for Lumen Dental Studio.
- **C. Routine.** "Your routine prompt", with three LinkedIn, two Instagram and five Threads posts a week.
- **Web variants.** `buildAiAppPrompt` in `WEB-ai-app-panels/lib/ai-apps.ts` @ 84cfc34e4: routine (recommend 3-5), campaign, and brand with and without a site. The routine template starter cards open the in-Bolta dialog and build no prompt of their own.

The live A/B/C text is not in any local web worktree. It differs from `buildAiAppPrompt`.

Each case pastes the earlier turns and then sends the next realistic message: notes, the missing launch date, "looks good, save it", or "set up 1 and 3". Brand graders follow the field list in the web vs MCP parity map:
- the business record is saved
- the voice is made (DOs, DON'Ts, `target_audience`, `topics`) and stays the default, or an existing thin voice is updated and linked with `business_dna_id`
- the accounts the voice writes for are named, or the connect link is given
- the Brand page link is shown

## Scores (mean of 3 runs)

| Case | Before | After |
|-|-|-|
| `ui-brand-notes-ask` | 0.93 | 1.00 |
| `ui-brand-notes-draft` | 0.88 | 1.00 |
| `ui-brand-notes-save` | 1.00 | 1.00 |
| `ui-brand-site-noaccount-save` | 0.75 | 1.00 |
| `ui-brand-site-notes-save` | 0.95 | 0.95 |
| `ui-brand-site-preview` | 0.98 | 1.00 |
| `ui-brand-site-save` | 1.00 | 1.00 |
| `ui-brand-web-no-site` | 1.00 | 1.00 |
| `ui-brand-web-preview-noaccount` | 0.75 | 0.97 |
| `ui-campaign-ask` | 0.90 | 1.00 |
| `ui-campaign-outline` | 0.90 | 1.00 |
| `ui-campaign-save` | 1.00 | 1.00 |
| `ui-routine-instagram-preview` | 0.95 | 1.00 |
| `ui-routine-missing-account` | 1.00 | 1.00 |
| `ui-routine-recommend-preview` | 0.88 | 0.97 |
| `ui-routine-recommend-save` | 0.82 | 1.00 |
| `ui-routine-weekly-preview` | 0.86 | 0.98 |
| `ui-routine-weekly-save` | 0.97 | 1.00 |
| **All 54 runs** | **0.917** | **0.993** |

No run approved, scheduled, published, switched on, ran a routine or started a campaign. Before any yes, every run read the site in preview only, and nothing was saved until the user said yes. Cost: $15.60 before, $16.45 and $16.49 for the two full re-runs, $1.90 for the two single-case re-runs after the last grader fixes.

## Failure, cause and fix

The skill was wrong on these:
- **No account connected.** The link was offered ("Want a link?") instead of given: 3 of 3 runs at preview and 2 of 3 after save. Fixed in SKILL.md (Look once: `get-connect-link`, its link in this reply, unasked; name the accounts a voice uses) and in `start.md`, `start-saving.md`, `start-making-voice.md` and `voice-setup-and-documents.md`. It still failed after the first fix to the references alone. It passed 6 of 6 once the rule was in SKILL.md.
- **"Set up Brand" saved the business record only, with no voice** (1 of 3). `start-saving.md` now says that a yes to a brand preview saves both the record and the voice, updates an existing voice rather than making a second, names the accounts, and gives the review link.
- **The routine prompt got 3-4 questions** (topic, day and time, reviewer, images) where it said "ask only for missing setup details". `routine.md` now says: use the planner even when they ask for a template; show the plan's day, time, topic and accounts and don't ask them; the reviewer is the person asking plus the approvers; at most 2 questions. Campaign with no launch named: one question (`campaign.md`).
- **Still open, `ui-brand-site-notes-save` (2 of 3 runs):** after updating an existing Starter Voice, the reply does not say which accounts use it. Updating a voice returns no `bootstrapped` result to read the accounts from. The prompt change below covers it.

The case was wrong on these:
- Graders were too narrow for correct replies:
  - "Is this right?" and "say save" as the ask before saving
  - a week-by-week outline written as a table or a dated list
  - "once you confirm"
  - a numbered table of routines and "tell me which"
  - "send me the address"
  - an either/or question on one line counted as two
- The notes-draft judge criterion required a sample post that prompt B never asks for. It also left out the user's own sample, so it counted "we'll bring the coffee" as invented.
- `ui-brand-notes-ask` required a Bolta read before asking for notes. Asking first is fine.
- Mocks:
  - The two saves in `ui-routine-recommend-save` returned the same id.
  - `get-routine` answered with the Northwind suite routine.
  - Both made the model rightly refuse to hand over the links.

  With several saves, the create mock now echoes the routine name as its id. A mock can't mint ids, and a file key can't hold spaces.

The prompt wording was weak on these. The full proposed text is in the PR body.
- **A and B have no line about social accounts** (owner requirement). Proposed: "assign the voice to our connected social accounts. If none are connected, give me the link to connect one."
- **B does not start with "Use Bolta".** It also asks for nothing beyond a draft profile.
- **"A routine template that supports this" in C sends the model to the template list before the planner.** It read the template list first in all 6 runs, and before the skill fix it never used the planner. Proposed: "Let Bolta pick the template, day, time and topics."

## Gaps the eval found in MCP itself (not fixable in the skill)

- Over MCP, notes alone can't make a business record: no tool creates one without a website. The notes land in the voice. The business overview has no field to go in.
- `update-voice-profile` takes no `account_ids`. Its schema also omits `topics`, `description` and `custom_rules` (see the parity map), so updating an existing voice can't set topics.

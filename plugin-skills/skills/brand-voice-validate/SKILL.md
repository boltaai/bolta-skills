---
name: brand-voice-validate
description: >
  Score a piece of content against the brand's voice guideline and return a compliance report
  with specific fixes. Use this skill when the user asks "is this on-brand", "score this
  against our voice", "check brand compliance", "validate this post", "does this sound like
  us", "rate this copy", or pastes content and wants a voice check. Returns a 0-100 score plus
  a deviation report and concrete edits. For writing new on-brand content use
  brand-voice-enforce; for building the guideline itself use brand-voice-generate.
---

# Brand Voice Validation

Grade content against the brand's voice guideline: what matched, what crossed a boundary, what
terminology slipped — with a number and actionable fixes, not a vibe.

## When to use
Any time content needs a brand check before it goes out: a drafted post, an email, a proposal
paragraph, ad copy, a caption — or to spot-check content an agent produced.

## Tools this skill uses
| Tool | Why |
|-|-|
| `get-voice-context` | Load Bolta's compiled voice when no session guideline exists. Returns tone dials, `tone_of_voice`, `dos`/`donts`, persona, custom rules, target audience, business identity, and per-platform adaptations — it does NOT carry exemplar posts, terminology lists, or a We-Are/We-Are-Not table. |
| `list-voice-profiles` | Confirm which Voice Profile applies if the workspace has several. |

Scoring is done inline using the grading behavior in Step 2.

## Prerequisites
- The content to score (pasted or referenced).
- `workspace_id` — resolve once via `list-workspaces` and reuse it. Auth is automatic via the
  Bolta connector's OAuth grant — never ask for an API key. Default new content to Draft;
  confirm before publish/delete.
- A voice source, in this order (stop at first hit):
  1. A guideline produced this session by `brand-voice-generate`.
  2. `get-voice-context` for the workspace (use `list-voice-profiles` to pick the right profile).
  3. If neither exists → stop, explain, and offer to run `brand-voice-discover` →
     `brand-voice-generate` first. Do not score against an invented voice.

## Workflow

### 1. Load the standard
Prefer the session guideline (freshest). Otherwise `get-voice-context`; if multiple profiles
exist, `list-voice-profiles` and confirm which one governs this content.

### 2. Score against each dimension
Score only dimensions the loaded voice source actually carries — never grade against a
dimension the standard doesn't define.

Always available (both sources):
- **Dos** — is each `do` honored? (matched / partial / missing)
- **Don'ts** — any violated? (each violation is a hard deduction)
- **Tone** — does the register match the stated tone (`tone` dials + `tone_of_voice`
  descriptors), pacing, and content size?
- **Audience & persona** — does it speak to the stated `target_audience` in the stated
  persona / speaker mode, and honor any `custom_rules`?

Session-guideline only (skip when grading from `get-voice-context` alone — the compiled
context does not carry these):
- **We Are / We Are Not attributes** — each active attribute present? any boundary crossed?
- **Terminology** — must-use present, avoid/never words absent.
- **Tone-by-context matrix** — register matches the matrix row for this content type. On the
  `get-voice-context` path, use the `platforms` adaptations block (if present for this
  platform) as the context check instead.

Grade against the brand's OWN standard, not generic "good writing" — a blunt, no-emoji brand
should score high for being blunt and emoji-free. Quote the line for every violation. Then
compose the 0-100 score from the dimensions actually evaluated (weight don't-violations and
boundary crossings heaviest), and say which dimensions were skipped and why.

### 3. Build the deviation report
List, specifically (covering only the dimensions scored in Step 2):
- Dos/attributes matched (with the phrase that earned it).
- Dos/attributes missing or weak.
- Don'ts or boundaries crossed (quote the offending text).
- Terminology issues (found → should be) — session guideline only.
- Tone mismatch (observed register vs. the expected tone or matrix row).

### 4. Return score + fixes
Give the score, a one-line verdict (on-brand / needs work / off-brand), and a numbered list of
concrete edits that would raise the score — quote the exact text to change and the replacement.
Offer to apply the fixes via `brand-voice-enforce`.

## Failure handling
- No voice source → stop, explain, route to discover/generate. Never score against nothing.
- Guideline has open questions touching this content → score against the recommended default
  and note the assumption.
- Permission error on `get-voice-context` → report the missing scope; if a session guideline
  exists, use it instead.

## Example
User: "Score this against our voice: 'We're thrilled to announce our game-changing new tool!'"
1. Load session guideline → We Are: Direct, Proof-driven; We Are Not: Hype-driven; niche uses
   "platform" not "tool".
2. Score: crosses "not Hype-driven" ("thrilled", "game-changing"); terminology miss ("tool").
3. Deviation report: 0 We-Are matched, 1 boundary crossed, 1 never-word, 1 terminology miss.
4. Score 34/100 — off-brand. Fixes: drop "thrilled to announce" → lead with the metric;
   "game-changing" → cut; "tool" → "platform". Offer to rewrite via brand-voice-enforce.

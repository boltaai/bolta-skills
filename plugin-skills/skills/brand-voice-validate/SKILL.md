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
| `get-voice-context` | Load Bolta's compiled voice (tone, dos/donts, exemplars) when no session guideline exists. |
| `list-voice-profiles` | Confirm which Voice Profile applies if the workspace has several. |

Scoring is delegated to `../../agents/quality-assurance.md`. See `../../references/bolta-tools.md`.

## Prerequisites
- The content to score (pasted or referenced).
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
Evaluate the content on:
- **We Are attributes** — is each active attribute present? (matched / partial / missing)
- **We Are Not boundaries** — any crossed? (each crossing is a hard deduction)
- **Terminology** — must-use present, avoid/never words absent.
- **Tone-by-context** — does the register match the correct matrix row for this content type?
Delegate the graded pass to the `quality-assurance` subagent for consistency, then compose the
0-100 score (weight boundary crossings and never-words heaviest).

### 3. Build the deviation report
List, specifically:
- Attributes matched (with the phrase that earned it).
- Attributes missing or weak.
- Boundaries crossed (quote the offending text).
- Terminology issues (found → should be).
- Tone mismatch (observed register vs. expected row).

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

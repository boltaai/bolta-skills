---
name: brand-voice-enforce
description: >
  Transform and produce content in the brand's established voice. Use this skill when the
  user asks to "rewrite this in our voice", "make this on-brand", "apply our brand voice",
  "adapt this post for email/blog/proposal", "write an email in our voice", "draft a
  proposal", "write a blog intro", or wants one piece of content re-expressed across
  formats against a full guideline. Works for social media and beyond (email, proposals,
  decks, blog). For plain "write/draft a post" saved to Bolta use bolta-draft-post (the
  canonical drafting skill); for scoring existing content use brand-voice-validate; not for
  creating the guideline itself (use brand-voice-generate) or discovering brand materials
  (use brand-voice-discover).
---

# Brand Voice Enforcement

Write content that sounds like the brand. Load the brand's voice, apply the constant voice
attributes and the context-appropriate tone, produce the content, validate it against the
guideline, and briefly explain the brand choices made.

## When to use
Voice-heavy content work — rewriting existing copy in-brand, enforcing a full guideline,
or producing non-social formats (email, proposal, blog section, ad copy, deck). For a plain
"draft a post" saved to Bolta, bolta-draft-post is the canonical owner; for scoring content
that already exists, use brand-voice-validate.

## Tools this skill uses
| Tool | Why |
|-|-|
| `list-workspaces` | Resolve `workspace_id` if unknown. |
| `get-voice-context` | Load Bolta's compiled voice context (tone, dos/donts, exemplars). |
| `voice-generate` | Bolta's voice-aware writer for social drafts; guideline maps onto its `tone`/`dos`/`donts`/`custom_rules`/`context` params. |
| `create-post` | Optional — save the on-brand result as a Bolta Draft when the content is a social post. |

For the voice-vs-tone model see `references/voice-constant-tone-flexes.md`.

## Prerequisites
- `workspace_id` — resolve once via `list-workspaces` and reuse it. Auth is automatic via the
  Bolta connector's OAuth grant — never ask for an API key. Default new content to Draft;
  confirm before publish/delete.
- A brand voice source, found in this order (stop at first hit):
  1. A guideline produced this session by `brand-voice-generate`.
  2. `get-voice-context` for the workspace (Bolta's stored voice).
  3. If neither exists, tell the user and offer to run `brand-voice-discover` →
     `brand-voice-generate` first. Do not invent a voice.

## Workflow

### 1. Load the voice
- If a session guideline exists, use it directly (freshest, reflects latest intent).
- Otherwise call `get-voice-context` (optionally with `voice_profile_id` / `platforms`).
- Extract: the **We Are / We Are Not** attributes (voice constants), the **tone-by-context**
  settings, terminology (must-use / preferred / avoid / never), and example phrasing.

### 2. Analyze the request
Identify content type, audience, key message, and any length/format/tone overrides. Map the
content type to a row of the tone matrix (formality, energy, technical depth). See
`voice-constant-tone-flexes.md`.

### 3. Generate
- **Social post:** call `voice-generate`, passing the guideline through its params —
  `tone` (a string, e.g. "professional, direct"), `dos`, `donts`, `custom_rules`, `context`,
  `business_name`, `niche`, and `topics`. Always pass `max_posts` explicitly — the server
  defaults to 7 posts per call, so a single-draft request without it burns credits on 6
  unwanted variants. Always pass `platform` (linkedin, x, threads, bluesky, facebook,
  instagram, reddit) when the target is known — without it, example selection is
  non-deterministic and biased toward the most-recently-analyzed account.
  This runs Bolta's own writer so the output matches everything else Bolta produces.
- **Non-social content (email, proposal, blog, deck):** write it directly, applying the same
  voice constants and tone flexes. For long-form or high-stakes content, write from the
  persisted Voice Profile holding the We Are / We Are Not constants fixed while flexing tone
  (formality/energy/technical depth) to the format — hand social to `voice-generate` and write
  non-social directly, holding the same voice constants across 1,200 words as across a
  200-character post, then route (default to Draft, review for Safe Mode/creator callers,
  publish only on explicit confirmed ask).
- Apply voice constants throughout; flex tone to the context; use preferred terminology and
  never cross a "We Are Not" boundary.

### 4. Validate
Check the draft against the guideline: every active "We Are" attribute present, no "We Are
Not" boundary crossed, terminology compliant, tone matches the context row. For high-stakes
content, grade against the brand's OWN persisted Voice Profile (`get-voice-context`), not
generic "good writing" — a blunt, no-emoji brand should score high for being blunt and
emoji-free. Report which "We Are" attributes are present/missing, any "We Are Not" boundary
crossed (quote the line), terminology compliance, and tone match for the context; then revise
on those findings.

### 5. Present
Return the content, then a short note on the brand choices made (which attributes led, the
tone setting, any terminology swaps). If the guideline has open questions that touch this
content, apply the recommended default and flag it. Offer to save a social post as a Draft
via `create-post` (default `requested_action` = draft; never publish without explicit ask).

## Handling conflicts
If the request conflicts with the guideline (e.g. "make it hypey" vs. a "not hype-driven"
boundary), explain the conflict, recommend the on-brand option, and offer to follow the
guideline strictly, adapt for context, or override. Default to adapting with a one-line note.

## Failure handling
- No voice source found → stop, explain, offer `brand-voice-discover` / `brand-voice-generate`.
- `voice-generate` fails → fall back to writing directly with the guideline, note that Bolta's
  writer was unavailable.
- Permission error saving a Draft → report the missing scope from `get-my-capabilities`; still
  return the written content.

## Example
User: "Write a LinkedIn post announcing our Series A."
1. `get-voice-context(workspace_id)` → We Are: Confident, Data-driven, Direct; not Hype-driven.
2. Content type = social/LinkedIn → tone: formality medium, energy high, depth low.
3. `voice-generate(workspace_id, topics=["Series A announcement"], tone="confident, direct",
   dos=[...], donts=["no buzzwords","no 'thrilled to announce'"],
   context="Series A, $X, lead investor Y", max_posts=1, platform="linkedin")`.
4. Validate: leads with a number, no hype clichés, direct → passes.
5. Present the post + "Led with Confident + Data-driven; kept energy high for LinkedIn; avoided
   'thrilled to announce' per your We-Are-Not. Save as a Draft?"

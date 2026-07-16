---
name: brand-voice-enforce
description: >
  Apply the brand's voice and tone to any content the user asks to write. Use this skill
  when the user asks to "write a post", "draft a LinkedIn post", "write an email", "draft a
  proposal", "write a blog intro", "make this on-brand", "rewrite this in our voice", "apply
  our brand voice", "does this sound like us", or requests any content that should match an
  established brand voice. Works for social media and beyond (email, proposals, decks, blog).
  Not for creating the guideline itself (use brand-voice-generate) or discovering brand
  materials (use brand-voice-discover).
---

# Brand Voice Enforcement

Write content that sounds like the brand. Load the brand's voice, apply the constant voice
attributes and the context-appropriate tone, produce the content, validate it against the
guideline, and briefly explain the brand choices made.

## When to use
Any content-creation request where the output should be on-brand — a social post, an email,
a proposal, a blog section, ad copy, a caption. This is the everyday writing skill.

## Tools this skill uses
| Tool | Why |
|-|-|
| `list-workspaces` | Resolve `workspace_id` if unknown. |
| `get-voice-context` | Load Bolta's compiled voice context (tone, dos/donts, exemplars). |
| `voice-generate` | Bolta's voice-aware writer for social drafts; guideline maps onto its `tone`/`dos`/`donts`/`customRules`/`context` params. |
| `create-post` | Optional — save the on-brand result as a Bolta Draft when the content is a social post. |

For deep guidance see `../../references/bolta-tools.md`, `references/voice-constant-tone-flexes.md`.

## Prerequisites
- `workspace_id` — resolve once via `list-workspaces`, reuse.
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
  `tone`, `dos`, `donts`, `customRules`, `context`, `businessName`, `niche`, and `topics`.
  This runs Bolta's own writer so the output matches everything else Bolta produces.
- **Non-social content (email, proposal, blog, deck):** write it directly, applying the same
  voice constants and tone flexes. For long-form or high-stakes content, delegate to the
  `content-generation` subagent (`../../agents/content-generation.md`).
- Apply voice constants throughout; flex tone to the context; use preferred terminology and
  never cross a "We Are Not" boundary.

### 4. Validate
Check the draft against the guideline: every active "We Are" attribute present, no "We Are
Not" boundary crossed, terminology compliant, tone matches the context row. For high-stakes
content, delegate to the `quality-assurance` subagent
(`../../agents/quality-assurance.md`) and revise on its findings.

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
3. `voice-generate(workspace_id, topics=["Series A announcement"], tone=..., dos=[...],
   donts=["no buzzwords","no 'thrilled to announce'"], context="Series A, $X, lead investor Y")`.
4. Validate: leads with a number, no hype clichés, direct → passes.
5. Present the post + "Led with Confident + Data-driven; kept energy high for LinkedIn; avoided
   'thrilled to announce' per your We-Are-Not. Save as a Draft?"

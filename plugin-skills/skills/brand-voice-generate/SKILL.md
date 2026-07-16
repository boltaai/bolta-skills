---
name: brand-voice-generate
description: >
  Synthesize a discovery report into a finished, enforceable Bolta Brand Voice Guideline. Use
  this skill when the user asks to "generate brand guidelines", "create a style guide", "build
  our voice guide", "write our brand voice doc", "turn this into guidelines", or "codify how we
  sound". Produces a structured guideline (We Are / We Are Not, tone-by-context matrix,
  terminology, confidence scores, open questions) AND — critically — a ready-to-use
  `voice-generate` parameter mapping so the guideline immediately drives Bolta's writer and
  every agent. For gathering evidence first use brand-voice-discover; for writing on-brand
  content use brand-voice-enforce; for scoring content use brand-voice-validate.
---

# Brand Voice Guideline Generation

Turn discovered signal into a single source of truth for the brand's voice, then express it as
Bolta writer parameters so it's operational, not just a document.

## When to use
After `brand-voice-discover`, or whenever the user wants a formal voice guide. If no discovery
report exists in the session, run discovery first (or gather at least DNA + published posts).

## Tools this skill uses
| Tool | Why |
|-|-|
| `get-voice-context` | Anchor the guideline to Bolta's existing compiled voice, if any. |
| `list-business-dna` / `get-business-dna` | Confirm industry / audience / positioning for the mapping. |
| `extract-business-dna` | Optional — seed Business DNA by scraping the brand's website (needs a `url`; reaches the internet + uses credits). |
| `list-voice-profiles` | Check whether a profile already exists (create new vs. evolve existing). |
| `create-voice-profile` | **Persist** the guideline as a native Bolta Voice Profile every agent then consumes. |
| `update-voice-profile` | **Evolve** an existing profile in place (partial update — omitted fields preserved). |
| `voice-generate` | Produce ONE sample draft to validate the mapping works end-to-end. |

Synthesis structure comes from `references/guideline-template.md`; scoring from
`references/confidence-scoring.md`. QA is done inline (Step 5).

## Prerequisites
- A discovery report (from `brand-voice-discover`) or equivalent gathered signal.
- `workspace_id` — reuse from discovery (resolve once via `list-workspaces`). Auth is automatic
  via the Bolta connector's OAuth grant — never ask for an API key. Default new content to
  Draft; confirm before persisting/overwriting a profile.
- `references/guideline-template.md` — output structure.
- `references/confidence-scoring.md` — how to score each section.

## Workflow

### 1. Assemble inputs
Take the discovery report. If thin, pull `get-voice-context` and `list-business-dna` /
`get-business-dna` to fill industry, audience, and positioning before synthesizing.

### 2. Synthesize the guideline
Following `references/guideline-template.md`, produce every section:
- **We Are / We Are Not** — at least 4 rows, each attribute paired with its opposite boundary,
  each backed by evidence from discovery.
- **Brand personality, messaging framework, terminology** (must-use / preferred / avoid / never).
- **Tone-by-context matrix** — at least 3 contexts (e.g. LinkedIn, X, cold email, proposal),
  each scored on formality / energy / technical depth.
- **Content examples** — before/after showing the voice applied.

### 3. Score confidence
Per `references/confidence-scoring.md`, assign High / Medium / Low to each section based on
evidence strength, volume, and source reliability (published posts and transcripts count as
behavioral evidence). Produce a confidence table and an aggregate weighted score.

### 4. Surface open questions — each WITH a recommendation
For every gap or conflict, write an open question AND a recommended default the brand can
accept as-is. Never leave a decision hanging without a recommendation.

### 5. QA
Guard the guideline before shipping it: verify all sections populated, 4+ We Are / We Are Not
rows, tone matrix covering 3+ contexts, 3+ attributes each with quoted evidence, confidence
assigned per section, every open question carrying a recommended default, sources attributed,
no PII, and the `voice-generate` parameter mapping present and faithful. Return pass or a
specific list of gaps and revise on them — never ship a partial guideline.

### 6. Express as `voice-generate` parameters — the operational half
Map the guideline onto Bolta's writer params so it drives generation immediately (see the
"voice-generate parameter mapping" section of `references/guideline-template.md`):
- `tone` ← the dominant register from the We-Are attributes + default tone-matrix row.
- `dos[]` ← the "We Are" attributes and must-use / preferred terminology, as imperative rules.
- `donts[]` ← the "We Are Not" boundaries and avoid / never terminology.
- `customRules` ← nuanced rules that don't fit dos/donts (structural, formatting, tone flexes).
- `context` ← positioning + audience summary.
- `businessName` / `niche` ← from Business DNA.
Present this block as copy-ready — it's what makes the guideline enforceable.

### 7. Validate the mapping with one sample
Call `voice-generate` once with the mapped params (a single, low-`maxPosts` sample on a
representative topic) to confirm the mapping yields on-brand output. Show the sample; if it
misses, tune the mapping and note what changed. Do not publish the sample.

### 8. Persist into Bolta — the durable half
Write the guideline back into Bolta so it drives the writer AND every autonomous agent, not
just this session. Confirm with the user before creating/overwriting, then:
- `list-voice-profiles` → decide **create** vs **evolve**.
- **New brand:** `create-voice-profile(workspace_id, name, tone={…dials…} OR writing_sample=<a
  strong on-brand excerpt>, tone_of_voice=[…], target_audience, dos, donts, content_size,
  pacing)`. Provide **either** a `tone` dials object **or** a `writing_sample` (≥50 chars) — the
  server extracts tone from the sample. Map the guideline's We-Are/We-Are-Not into `dos`/`donts`.
- **Evolving brand:** `update-voice-profile(workspace_id, profile_id, …only changed fields…)`.
  This is a partial update — omitted fields are preserved, so voice refines safely over time.
- Optional: `extract-business-dna(workspace_id, url=<brand site>)` first to seed Business DNA,
  then reference it when generating.

This is what makes brand voice foundational: the persisted profile flows into `voice-generate`,
ad-hoc drafts, and every hired agent automatically.

### 9. Save the document and hand off
Also save the human-readable guideline (session artifact) so `brand-voice-enforce` and
`brand-voice-validate` can consume it. Tell the user which profile was created/updated and that
every agent in this workspace now inherits the voice.

## Failure handling
- No discovery signal at all → stop and route to `brand-voice-discover`; don't fabricate.
- `voice-generate` sample fails → still deliver the guideline + mapping; note the writer was
  unavailable and the mapping is unvalidated end-to-end.
- `create-voice-profile` requires a `tone` object **or** `writing_sample` — if the tone dials
  aren't clear, pass a strong on-brand excerpt as `writing_sample` and let the server extract.
- Permission error on `create-voice-profile` / `update-voice-profile` (needs voice:write) →
  report the missing scope; still deliver the guideline document + `voice-generate` mapping so
  the voice is usable without persistence.
- QA (Step 5) flags missing sections → fix before delivering; never ship a partial guideline.

## Example
User: "Turn our discovery report into brand guidelines."
1. Assemble report (+ `get-business-dna` for niche/businessName).
2. Synthesize: 5 We-Are rows, tone matrix for LinkedIn/X/email, terminology tables.
3. Score: aggregate High (published-post evidence strong); email row Medium (thin evidence).
4. Open Qs: "Is dry humor OK in cold email? Recommend: keep it minimal, default off."
5. QA pass → passes after adding evidence to one attribute.
6. Mapping: `tone={"professional":80,"direct":75,"playful":20}`, `dos=["lead with a number",
   "say platform not tool"]`, `donts=["no 'thrilled to announce'","no hype adjectives"]`.
7. `voice-generate(maxPosts=1, topic="feature launch", ...)` → on-brand.
8. Persist: `create-voice-profile(workspace_id, name="Brand Voice", tone={…}, tone_of_voice=
   ["confident","proof-driven"], dos=[…], donts=[…], target_audience="DevOps leads")` → save
   guideline doc → "Created the 'Brand Voice' profile; every agent now writes in it."

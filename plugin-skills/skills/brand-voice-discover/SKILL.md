---
name: brand-voice-discover
description: >
  Discover and inventory a brand's voice signal before any guideline is written. Use this
  skill when the user asks to "discover our brand voice", "analyze my brand", "what's our
  voice", "figure out how we sound", "extract brand voice from my content", "audit our
  brand", or uploads brand docs, style notes, sales-call transcripts, or past posts and
  wants them turned into voice signal. This is the research step — it gathers and ranks
  evidence but does NOT synthesize the finished guideline (use brand-voice-generate for
  that) or write on-brand content (use brand-voice-enforce).
---

# Brand Voice Discovery

Gather every available signal about how the brand sounds — what Bolta already stores, what
the brand has already published, and anything the user uploads — then output a structured
discovery report that `brand-voice-generate` turns into a guideline. Do not invent voice;
only surface, rank, and reconcile evidence.

## When to use
The starting point of the brand-voice loop, or any time the user wants to understand their
current voice signal before committing to a guideline. Run this first when no session
guideline exists.

## Tools this skill uses
| Tool | Why |
|-|-|
| `list-workspaces` | Resolve `workspace_id` (start here). |
| `list-business-dna` / `get-business-dna` | Existing Business DNA — industry, audience, positioning. |
| `list-voice-profiles` / `get-voice-profile` | Any Voice Profiles already stored in Bolta. |
| `get-voice-context` | Bolta's compiled voice context (tone, dos/donts, exemplars) if one exists. |
| `list-accounts` | Connected platforms — shows where the brand actually speaks. |
| `list-workspace-posts` | Published posts (`status=Published`) — these ARE primary voice evidence. |

Heavy parsing of uploads is delegated to subagents — see Prerequisites.
For the full tool contract see `../../references/bolta-tools.md` and `../../references/bolta-ecosystem.md`.

## Prerequisites
- `workspace_id` — resolve once via `list-workspaces`, reuse for every call.
- Optional user uploads: brand docs (PDF/PPTX/DOCX/MD/TXT), sales/interview transcripts, or
  pasted sample copy. These are classified and parsed by subagents:
  - `../../agents/document-analysis.md` — brand documents.
  - `../../agents/conversation-analysis.md` — transcripts AND the brand's own published posts.

## Workflow

### 1. Resolve the workspace
Call `list-workspaces`; use the active workspace's `id`. If several exist, confirm which one
with the user. Never guess a UUID.

### 2. Pull existing Bolta signal
In parallel where possible:
- `list-business-dna` → `get-business-dna` for each record (industry, audience, positioning).
- `list-voice-profiles` → `get-voice-profile` for each profile (stored tone, dos/donts, exemplars).
- `get-voice-context` — the compiled context Bolta's writer already uses, if any.
- `list-accounts` — which platforms are connected (context for where the voice lives).
This is authoritative brand-owned signal; weight it highest.

### 3. Pull published-content evidence
Call `list-workspace-posts` with `status=Published` (page through with `limit`/`page`).
Published posts are behavioral voice evidence — how the brand actually talks in public.
Hand the post texts to the `conversation-analysis` subagent to extract implicit attributes,
recurring language patterns, tone-by-context (which platform/topic gets which register), and
anti-patterns the brand already avoids.

### 4. Classify and parse uploads
For each user-provided asset, route by type:
- Documents (decks, one-pagers, style notes, brand books) → `document-analysis` subagent →
  voice attributes, messaging themes, terminology, tone guidance, examples.
- Transcripts (sales calls, founder interviews, customer conversations) → `conversation-analysis`
  subagent → how the brand speaks unscripted (often the truest voice signal).
Delegate the heavy reading; keep only the structured extractions.

### 5. Reconcile and rank
Merge every source into one picture. Rank sources by reliability (brand-owned DNA/Voice
Profiles > published posts > brand documents > transcripts > pasted samples), noting recency
and volume. Flag conflicts explicitly (e.g. DNA says "formal", published posts read casual).

### 6. Output the discovery report
Produce a structured report:
- **Ranked sources** — each with type, reliability weight, recency, and volume.
- **Extracted attributes** — candidate "We Are" traits, each with the evidence behind it.
- **Terminology signal** — words the brand uses / avoids.
- **Tone-by-context observations** — how register shifts by platform/topic.
- **Conflicts** — where sources disagree, with both readings.
- **Gaps** — attributes with thin or no evidence.
- **Open questions** — what `brand-voice-generate` must resolve, each with a suggested default.

## Failure handling
- No workspace / permission error → report the missing scope (`get-my-capabilities`) and stop.
- No Business DNA, Voice Profiles, or voice context yet → say so plainly; lean on published
  posts and uploads. A brand-new workspace with no posts and no uploads = not enough signal;
  ask the user for sample content rather than fabricating a voice.
- No published posts → note the gap; discovery still proceeds from DNA/uploads, but flag that
  behavioral evidence is missing so confidence will be lower downstream.
- Upload unreadable by a subagent → report which asset failed and continue with the rest.

## Example
User: "Analyze our brand voice — here's our pitch deck and last quarter's posts are in Bolta."
1. `list-workspaces` → workspace_id.
2. `list-business-dna`/`get-business-dna` → SaaS, ops leaders, "developer-first" positioning;
   `list-voice-profiles` empty; `get-voice-context` empty; `list-accounts` → LinkedIn + X.
3. `list-workspace-posts(status=Published)` → 40 posts → `conversation-analysis` → "direct,
   proof-driven, dry humor; avoids hype; LinkedIn more formal than X."
4. Pitch deck → `document-analysis` → terminology ("platform" not "tool"), 3 messaging pillars.
5. Reconcile: deck says "visionary", posts read "pragmatic" → conflict flagged.
6. Report: 5 ranked sources, 6 candidate attributes with evidence, 1 conflict, 2 gaps,
   3 open questions → hand to `brand-voice-generate`.

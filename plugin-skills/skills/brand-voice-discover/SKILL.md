---
name: brand-voice-discover
description: >
  Discover and inventory a brand's voice signal before any guideline is written. Use this
  skill when the user asks to "discover our brand voice", "analyze my brand", "learn my brand
  voice from my website", "figure out how we sound", "extract brand voice from our site",
  "audit our brand", gives a brand URL, or uploads brand docs, style notes, sales-call
  transcripts, or past posts and wants them turned into voice signal. Pulls from four sources:
  the brand's website, what's already in Bolta, the brand's own published posts, and anything
  the user provides. This is the research step — it gathers and ranks evidence but does NOT
  synthesize the finished guideline (use brand-voice-generate) or write content (use
  brand-voice-enforce).
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
| `list-workspace-posts` | Published posts (`status=published`) — these ARE primary voice evidence. Add `include_metrics=true` for per-post engagement. |
| `extract-business-dna` | Scrape the brand's **website** into a Business DNA record (needs a `url`; reaches the internet + uses AI credits). The fastest cold-start source. **Pass `set_as_default=false`** — it defaults to true and silently demotes the workspace's existing default DNA. |
| `update-business-dna` | Fix what discovery finds wrong in the stored DNA — safe partial merge: only the keys sent in `fields` change, everything omitted is preserved. Tagline, overview, colors/fonts, local identity, story, image settings. |

Two more sources need no tool call: the **brand's website** (you can read public pages
directly since ChatGPT has internet access) and **what ChatGPT already knows** about a
recognizable brand. Both are supporting evidence — always confirm against the brand-owned
Bolta signal, never let outside knowledge override what the brand actually publishes.
Heavy parsing of uploads and posts is done inline using the analysis behaviors below.

## Prerequisites
- `workspace_id` — resolve once via `list-workspaces` and reuse it for every call. Auth is
  automatic via the Bolta connector's OAuth grant — never ask for an API key. Default any new
  content to Draft; confirm before publish/delete.
- Optional user uploads: brand docs (PDF/PPTX/DOCX/MD/TXT), sales/interview transcripts, or
  pasted sample copy. Parse these inline: brand documents and transcripts via the
  signal-distiller behavior (Step 5), and the brand's own published posts via the
  voice-archaeologist behavior (Step 4). A brand website URL is a strong optional input too
  (Step 3).

## Workflow

### 1. Resolve the workspace
Call `list-workspaces`; use the active workspace's `id`. If several exist, confirm which one
with the user. Never guess a UUID.

### 2. Pull existing Bolta signal
In parallel where possible:
- `list-business-dna` → `get-business-dna` for each record (industry, audience, positioning).
  If the user spots something stale or wrong in a record while reviewing it ("that tagline is
  old", "we moved — the city is wrong", "our colors are navy and sky blue now"), fix it
  conversationally with `update-business-dna(workspace_id, dna_id, fields={…changed keys
  only…})` — it's a safe partial merge, omitted fields are preserved, so a one-field
  correction can't wipe the rest. Confirm the change before writing.
- `list-voice-profiles` → `get-voice-profile` for each profile (stored tone, dos/donts, exemplars).
- `get-voice-context` — the compiled context Bolta's writer already uses, if any.
- `list-accounts` — which platforms are connected (context for where the voice lives).
This is authoritative brand-owned signal; weight it highest.

### 3. Pull website + external signal
If the user gives (or you can infer) the brand's website, use it — it's the fastest cold-start
source and often the clearest statement of positioning and voice:
- Read the public site directly (homepage, about, product pages) for headline voice, value
  props, and terminology; and/or call `extract-business-dna` with the `url` to structure it
  into a Business DNA record you can reference later. Pass `set_as_default=false` — the
  param defaults to true and silently demotes the workspace's existing default Business DNA.
  Only set it true (or omit it) when the user explicitly wants the extracted record to
  become the default, and confirm first if a default already exists.
- If the brand is recognizable, you may draw on what ChatGPT already knows about it — but treat
  this as a hypothesis to confirm, never as fact. State that it's external knowledge.
Rank this **below** brand-owned Bolta signal and published posts: the website says how the
brand wants to sound; the posts show how it actually sounds. When they disagree, the posts win
and the gap becomes an open question.

### 4. Pull published-content evidence
Call `list-workspace-posts` with `status=published` and `include_metrics=true` — each post
then carries per-platform engagement (views, likes, comments, reposts) alongside its text.
The default page is 50 posts (max 100); page through with `limit`/`page` so the evidence
isn't silently truncated to the first page. Published posts are behavioral voice evidence —
how the brand actually talks in public. Excavate the brand's lived voice from Bolta's own
evidence (the **voice-archaeologist** behavior): pull the published posts with their
per-post metrics, and the review signal (`list-reviews`, `list-recurring-reviews`)
— what the team approved untouched vs. edited vs. rejected. Extract voice attributes each
backed by a quoted real post, ranked by consistency; mark attributes that correlate with
higher engagement as "proven" not just "present"; treat systematic edits (always cutting hype,
always adding a number) as implicit rules and rejected phrasings as "We Are Not" candidates.
Redact customer names/PII from quotes. Weak evidence = 1 post; strong = a pattern across 8+.

### 5. Classify and parse uploads
For each user-provided asset, distill it inline using the **signal-distiller** behavior:
turn uploaded materials (decks, one-pagers, brand books, transcripts, site copy) into Bolta's
structured models — Business DNA {industry, audience, positioning, offer} and Voice Profile
fields {tone dials OR a `writing_sample` excerpt, `tone_of_voice`[], `dos`[], `donts`[],
`target_audience`, terminology: must-use/preferred/avoid/never}. Attribute every field to its
source; leave ungrounded fields empty rather than inventing; prefer a strong on-brand
`writing_sample` over guessing precise tone dials when material is qualitative. Where uploaded
materials disagree with the brand's shipped posts, flag it as an open question rather than
silently picking one. Transcripts (sales calls, founder interviews) often carry the truest,
unscripted voice signal. Keep only the structured extractions.

### 6. Reconcile and rank
Merge every source into one picture. Rank sources by reliability (brand-owned DNA/Voice
Profiles > published posts > brand documents > transcripts > pasted samples), noting recency
and volume. Flag conflicts explicitly (e.g. DNA says "formal", published posts read casual).

### 7. Output the discovery report
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
- Upload unreadable → report which asset failed and continue with the rest.

## Example
User: "Analyze our brand voice — here's our pitch deck and last quarter's posts are in Bolta."
1. `list-workspaces` → workspace_id.
2. `list-business-dna`/`get-business-dna` → SaaS, ops leaders, "developer-first" positioning;
   `list-voice-profiles` empty; `get-voice-context` empty; `list-accounts` → LinkedIn + X.
3. `list-workspace-posts(status=published, include_metrics=true)` → 40 posts → voice-archaeologist pass → "direct,
   proof-driven, dry humor; avoids hype; LinkedIn more formal than X."
4. Pitch deck → signal-distiller pass → terminology ("platform" not "tool"), 3 messaging pillars.
5. Reconcile: deck says "visionary", posts read "pragmatic" → conflict flagged.
6. Report: 5 ranked sources, 6 candidate attributes with evidence, 1 conflict, 2 gaps,
   3 open questions → hand to `brand-voice-generate`.

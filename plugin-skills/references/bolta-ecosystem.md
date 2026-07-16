# Bolta Ecosystem & Auth — Reference

Context every Bolta skill assumes. Read once; it applies to all skills in this pack.

## What Bolta is

Bolta (bolta.ai) is a social-media management platform: it drafts, schedules, publishes,
and analyzes content across X, Threads, LinkedIn, Facebook, Instagram, Bluesky, Mastodon,
Discord, Reddit, TikTok, Pinterest, and YouTube — and runs **autonomous AI agents** that
produce content on a schedule for human approval. Brand **voice** is the foundation: every
draft is written through a compiled voice context so output sounds like the brand.

## How the plugin connects

- **MCP endpoint:** `https://mcp.bolta.ai/mcp` (StreamableHTTP, stateless).
- **Auth in ChatGPT:** the user authorizes the Bolta connector once (OAuth 2.1). That grant
  mints a workspace-scoped `bolta_sk_` API key behind the scenes. Skills never handle a key
  directly and never ask the user to paste one.
- **Tenancy:** every key is scoped to a single workspace. `workspace_id` is required by
  nearly every tool — resolve it with `list-workspaces` at the start of a session and reuse
  it. Never operate across workspaces in one flow.

## Roles & permissions

The caller has a role that gates what they can do. Before a write, `get-my-capabilities`
tells you the caller's role and scopes.

- **viewer** — read only (analytics, lists, voice/DNA reads).
- **creator** — viewer + draft/generate content, submit for review. Cannot publish directly;
  Safe Mode routes content to review.
- **editor** — creator + approve/reject, delete, bulk ops.
- **admin/owner** — everything, incl. hiring agents and connecting accounts.

If a tool returns a permission error, explain the missing role/scope plainly rather than
retrying — this is `get-my-capabilities`'s job to pre-empt.

## Safe defaults for skills

1. **Draft, don't publish.** Default new content to Draft (`requested_action` omitted). Only
   `publish-post` / `requested_action: publish` when the user explicitly asks to publish now,
   and confirm first — publishing is destructive and public.
2. **Confirm destructive actions.** `delete-post` and `publish-post` are irreversible; always
   confirm with the user before calling them.
3. **Voice first.** Load `get-voice-context` (or an active brand-voice guideline) before
   writing, so content is on-brand from the first draft.
4. **One workspace per flow.** Resolve `workspace_id` once and reuse it.
5. **Attribute agent work.** Content produced by agents flows into `list-recurring-reviews`;
   approving/rejecting there is what teaches Bolta the brand's voice over time.

## The voice model (why brand voice is foundational)

Bolta stores brand identity as **Business DNA** (industry, audience, positioning) and one or
more **Voice Profiles** (tone, dos/donts, exemplars). `get-voice-context` compiles these into
the exact context Bolta's writer uses. The brand-voice skills in this pack capture a brand's
voice into an enforceable guideline and apply it through `voice-generate` and `create-post`,
so the same voice drives ad-hoc drafts *and* every autonomous agent — on social media and
beyond (emails, proposals, blog posts, decks).

See `bolta-tools.md` for the full tool contract.

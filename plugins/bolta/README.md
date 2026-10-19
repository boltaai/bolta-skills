# BOLTA

Tell Claude what you want to post about. Bolta writes it in your voice every week, and nothing goes out until you say yes.

## Ask for

- "Plan a week of LinkedIn posts about our new pricing." Drafts in your voice; "yes to 1, 3 and 4" schedules them.
- "Keep me posting every week." A **Bolta routine** writes drafts every Monday, even with Claude closed.
- "We launch on Nov 3." A **campaign**: 1 to 4 weeks, a strategy, a verdict.

Start with `/bolta:start` or "set me up".

## Install

Claude Code 2.1.295 or later:

```
/plugin marketplace add boltaai/bolta-skills
/plugin install bolta@bolta-marketplace
```

Then `/mcp`, pick `bolta`, sign in, pick the workspace.

- **Windows:** install [Git for Windows](https://git-scm.com/downloads/win) first, or every Bolta save is blocked.
- **Fewer prompts:** in `/permissions`, allow `mcp__plugin_bolta_bolta` under User settings (agencies: each `mcp__bolta-<client>`). Bolta's own checks still ask.

claude.ai and Cowork (untested): add this repository as a marketplace, install BOLTA, connect Bolta under Customize > Connectors. In chat, keep approve, schedule, publish and reject on "Needs approval".

Added Bolta yourself (connector, or `claude mcp add`)? Install `bolta-skills` instead: same skills and checks, no second connection.

## What Bolta checks

Claude Code and Cowork ask before:

- anything public: a post, a reply, a reaction;
- approving, turning down or scheduling (once per batch per message);
- running a Bolta routine now; starting or finishing a campaign;
- changing your voice, business details, account groups or a running campaign's accounts;
- anything that can't be undone.

Drafts need none. Claude Code only: **Bolta checks** `careful` in `/config` checks every approval. Chat runs no hooks: posts stay on your review list until approved, and Claude approves only after your yes in words.

## Limits

- No media upload: Instagram, TikTok, YouTube and Pinterest need a public link.
- Until Bolta's newer tools reach your server, a "no" with a reason and a campaign's accounts are set in Bolta.
- One connection is one workspace; agencies add one per client. Another server's tool named like a Bolta one gets the same check.
- Hooks need `sh` and `awk`, and trust their marker files: Claude, if it may run shell commands unasked, could forge one.

## Sent and stored

Bolta (mcp.bolta.ai) gets your requests and decisions. Sign-in is Claude's: the plugin never sees a password. Hooks keep marker files in `${TMPDIR:-/tmp}/bolta-plugin/` and make no network calls.

v0.2.0 (beta). [Privacy](https://bolta.ai/privacy-policy) · [Terms](https://bolta.ai/tos) · [Support](https://bolta.ai/support) · MIT licence

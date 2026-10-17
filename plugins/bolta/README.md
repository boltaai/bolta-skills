# BOLTA

Tell Claude what you want to post about. Bolta writes it in your voice every week, and nothing goes out until you say yes.

## Ask for

- "Plan a week of LinkedIn posts about our new pricing." Drafts in your voice; "yes to 1, 3 and 4" schedules them.
- "Keep me posting every week." A **Bolta routine** writes drafts every Monday, even with Claude closed.
- "We launch on Nov 3." A **campaign**: 1 to 4 weeks, a strategy, a verdict.

Start with `/bolta:start` or "set me up". Later, ask "what needs me?"

## Install

Claude Code 2.1.295 or later:

```
/plugin marketplace add boltaai/bolta-skills
/plugin install bolta@bolta-marketplace
```

Then `/mcp`, pick `bolta`, sign in and pick the workspace.

- **Windows:** install [Git for Windows](https://git-scm.com/downloads/win) first. Without Git Bash, every Bolta save is blocked.
- **Fewer prompts:** in `/permissions`, allow `mcp__plugin_bolta_bolta` under User settings (agencies: each `mcp__bolta-<client>` too). Bolta's own checks still ask.

claude.ai and Cowork (untested end to end): add this repository as a marketplace, install BOLTA, connect Bolta in Customize > Connectors. In chat, keep Bolta's approve, schedule and publish tools on "Needs approval".

## What Bolta checks

In Claude Code and Cowork, Bolta asks before:

- anything public: a post, a reply, a reaction;
- approving or scheduling (once per batch per message);
- running a Bolta routine now; starting or finishing a campaign;
- changing your voice, business details or account groups;
- anything that can't be undone.

Drafts need none. Claude Code only: **Bolta checks** `careful` in `/config` checks every approval. Chat runs no hooks: Bolta keeps Claude's posts on your review list until approved, and Claude approves only after your yes in words.

## Limits

- No media upload: Instagram, TikTok, YouTube and Pinterest need a public file link.
- A "no" with a reason, and a Bolta-written campaign's accounts, are set in Bolta for now.
- One connection is one workspace. Agencies add one per client, with "bolta" in its name.
- Hooks need `sh` and `awk` (tested: mawk, gawk, BWK awk 20180827 to 20251225, around macOS's 20200816).
- The checks trust their marker files. If Claude may run shell commands unasked, it could forge one.

## Sent and stored

Bolta (mcp.bolta.ai) gets your requests and decisions. Sign-in is Claude's: the plugin never sees a password. Hooks keep marker files in `${TMPDIR:-/tmp}/bolta-plugin/` and make no network calls.

v0.2.0 (beta). [Privacy](https://bolta.ai/privacy-policy) · [Terms](https://bolta.ai/tos) · [Support](https://bolta.ai/support) · MIT licence

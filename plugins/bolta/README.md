# BOLTA

Tell Claude what you want to post about. Bolta writes it in your voice every week, and nothing goes out until you say yes.

## Ask for

- "Plan a week of LinkedIn posts about our new pricing." Drafts in your voice; "yes to 1, 3 and 4" schedules them.
- "Keep me posting every week." A **Bolta routine** writes drafts every Monday, even with Claude closed.
- "We launch on Nov 3." A **campaign**: 1 to 4 weeks, a strategy, a verdict.
- "What's waiting?" or "Any mentions?" With 8 or more drafts or 10 or more mentions, read-only **clearing-house** and **community-triage** helpers sort them first (Claude Code, Cowork). You decide.

Start with `/bolta:start` or "set me up".

## Install

Claude Code 2.1.295 or later:

```
/plugin marketplace add boltaai/bolta-skills
/plugin install bolta@bolta-marketplace
```

Then `/mcp`, pick `bolta`, sign in, tick the brands.

- **Fewer prompts:** in `/permissions`, allow `mcp__plugin_bolta_bolta` under User settings. Bolta's own checks still ask.

claude.ai and Cowork (untested): add this repository as a marketplace, install BOLTA, connect Bolta under Customize > Connectors. In chat, keep approve, schedule, publish and reject on "Needs approval".

Added Bolta yourself already (a connector, or `claude mcp add`)? Claude Code keeps one connection per address; if two show in `/mcp`, remove one.

## What Bolta asks first

Drafts save freely. Claude asks for your yes in words, after showing the exact text, before:

- anything public: a post, a reply, a reaction;
- approving, turning down or scheduling;
- running a Bolta routine now; starting or finishing a campaign;
- changing your voice, business details, account groups or a running campaign's accounts;
- anything that can't be undone.

Bolta's server enforces the same on its side. In chat, keep approve, schedule, publish and reject on "Needs approval" in the connector's settings.

## Limits

- No media upload: Instagram, TikTok, YouTube and Pinterest need a public link.
- Until Bolta's newer tools reach your server, a "no" with a reason and a campaign's accounts are set in Bolta.
- One connection reaches the brands you tick; agencies tick their clients. New brand: reconnect.

## Sent and stored

Bolta (mcp.bolta.ai) gets your requests and decisions. Sign-in is Claude's: the plugin never sees a password and makes no network calls of its own.

v0.5.0 (beta). [Privacy](https://bolta.ai/privacy-policy) · [Terms](https://bolta.ai/tos) · [Support](https://bolta.ai/support) · MIT licence

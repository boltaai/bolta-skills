# BOLTA

Tell your AI app what you want to post about. Bolta writes it in your voice every week, and nothing goes out until you say yes.

## Ask for

- "Plan a week of LinkedIn posts about our new pricing." Drafts in your voice; "yes to 1, 3 and 4" schedules them.
- "Keep me posting every week." A **Bolta routine** writes drafts every Monday, even with this app closed.
- "We launch on Nov 3." A **campaign**: 1 to 4 weeks, a strategy, a verdict.
- "What's waiting?" or "Any mentions?" With 8 or more drafts or 10 or more mentions, read-only **clearing-house** and **community-triage** helpers sort them first, in apps that run subagents. You decide.

Start with `/bolta:bolta` or "set me up".

## Install

Connect Bolta (`https://mcp.bolta.ai/mcp`) in your AI app, sign in, tick the brands, then add the skill: `npx skills add boltaai/bolta-skills --skill bolta`.

<!-- host-note -->
In apps that have plugin marketplaces (for example Claude Code 2.1.295 or later):

```
/plugin marketplace add boltaai/bolta-skills
/plugin install bolta@bolta-marketplace
```

Then `/mcp`, pick `bolta`, sign in. `/plugin install bolta-checks@bolta-marketplace` adds the Bolta checks. Fewer prompts: in `/permissions`, allow `mcp__plugin_bolta_bolta`.

claude.ai and Cowork (untested): add this repository as a marketplace, install BOLTA, connect Bolta under Customize > Connectors; keep approve, schedule, publish and reject on "Needs approval".
<!-- /host-note -->

## What Bolta checks

Nothing is approved, scheduled, published or switched on until your yes in words.

<!-- host-note -->
In apps that run plugin hooks (for example Claude Code), `bolta-checks` also shows a Bolta check before:

- anything public: a post, a reply, a reaction;
- approving, turning down or scheduling (once per batch per message);
- spending credits now: running a Bolta routine now, starting a campaign, writing posts on the spot; finishing a campaign;
- changing your voice, business details, account groups or a running campaign's accounts;
- anything that can't be undone.

Saving drafts needs none. **Bolta checks** `careful` in `/config` checks every approval.
<!-- /host-note -->

## Limits

- No media upload: media goes in as a public link. Instagram and Pinterest need an image or video, TikTok and YouTube a video.
- One connection is one organization and reaches the brands you tick in it; agencies tick their client brands. New brand: reconnect and tick it.
- The checks need `sh` and `awk` (Windows: [Git for Windows](https://git-scm.com/downloads/win) first).

## Sent and stored

Bolta (mcp.bolta.ai) gets your requests and decisions. Sign-in is your AI app's: the plugin never sees a password and makes no network calls of its own.

v0.5.0 (beta). [Privacy](https://bolta.ai/privacy-policy) · [Terms](https://bolta.ai/tos) · [Support](https://bolta.ai/support) · MIT licence

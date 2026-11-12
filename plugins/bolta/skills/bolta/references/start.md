# Start

Get someone running: an account connected first, brand and voice through Bolta's setup, 3-5 Bolta routines, one question about anything dated; saved off, switched on with a yes. Use for: set me up, get going, I have nothing set up, keep me posting with nothing running yet.

## Done when

They have the connect link or a connected account, saw their brand and voice, and answered a routine proposal. What they chose is saved; on only after its own yes.

## Know this

**The first reply does it all.** Read together, then answer once, in this order:

1. **Look once** (the Bolta skill), plus `list-routines`, `list-content-campaigns`, `list-business-dna`, the `list-inbox-items` pending count. Routines on and drafts flowing: [today](today.md).
2. **An account first.** None connected: `get-connect-link`, the link at the top of this reply, unasked, with why: "Connect one first: drafts need somewhere to go, and your voice learns from that account's posts." Still none at the end: repeat it last. Setting up without one works, never first. Connected: name the accounts the voice writes for.
3. **Brand and voice, from what you know.** Show what you know (business, site, audience, products, how they write) in a few lines; ask only the gaps, website first ([start-brand-setup.md](start-brand-setup.md)). A site: `extract-business-dna` `preview: true` in 3-4 lines; on yes, `setup: true` with what they told you, `check: true` until done. None: build it from what they shared. A voice exists: show it in a line ([first session](start-first-session-voice.md)); a record exists: reuse it.
4. **Propose 3-5 Bolta routines**, each a different job, best fit first, in their words. Only networks they named; Instagram needs a picture or video ([start-matching.md](start-matching.md)).
   - Bolta's planner: `plan` `kind: "recommend"`, their words as `ask`, `count` 3-5, what Bolta holds and what they told you as `context`, said first in one "Based on..." line ([routine-planner-context.md](routine-planner-context.md)). Show each plan's name, day, time, networks, drafts per run, `why`.
   - No planner: `list-routine-templates` once; pick 3-5 creatable rows; set day, time, networks, count.
5. **Size to review time:** 3-6 drafts a week in all, never daily to start. 10+ waiting: name the count, offer to go through them first. Say "Every draft waits for your yes."
6. **One closing question, with the launch in it:** "Which should I set up (saved switched off; nothing runs until you say so), and is a launch, sale or event coming up I should plan for?" A yes with a date: one campaign plan (`plan` `kind: "campaign"`, `context`, pages as `links`; else [campaign](campaign.md)). Already named: plan it as its own numbered line. A launch is never a routine.

**Question budget:** at most 2 questions a reply: the findings with one gap, and the closing one. Never ask what to post about. A plan's open questions: `revise-plan`, later.

**Saving, then switching on:** a yes to set up saves them switched off; switching on is its own yes. Read [start-saving.md](start-saving.md) before saving.

**After:** "On Monday, say 'what's waiting'." Wording: [first session](start-first-session.md).

## Tools

- `list-workspaces`, `list-accounts`, `get-voice-context`, `list-business-dna`, `list-routines`, `list-content-campaigns`, `list-inbox-items`.
- `get-connect-link`, `extract-business-dna`, `create-voice-profile`: accounts, brand, voice.
- `plan` (`kind` routine, campaign or recommend; left out, Bolta decides from `ask`), `revise-plan`, `confirm-plan`: Bolta's planner.
- `list-routine-templates`, `create-routine`, `activate-routine`: without it, and switching on.

## Hand off

[review](review.md), [routine](routine.md) (drafts keep missing), [campaign](campaign.md), [voice](voice.md), [connect](connect.md), [today](today.md).

## Always

- Follow the house rules in the Bolta skill.
- Nothing runs, posts or switches on without its own yes; never run a routine now in the first session.
- Claim learning only from the decision count.

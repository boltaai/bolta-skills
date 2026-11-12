# Start

Get someone running, voice first: brand from their site, a voice, accounts, 3-5 Bolta routines matched to their business, saved off, then switched on with a yes. Use for: set me up, get going, I have nothing set up, keep me posting with nothing running yet.

## Done when

They saw their brand and voice, have the connect link or accounts, and answered a routine proposal. What they chose is saved; on only after its own yes.

## Know this

**The first reply does it all.** Read together, then answer once:

1. **Look once** (the Bolta skill), plus `list-routines`, `list-content-campaigns` and the pending count from `list-inbox-items`. Routines on and drafts flowing: [today](today.md).
2. **Brand from their site.** A site given and no business record: `extract-business-dna` with `url` and `preview: true`, before accounts. Show it in 3-4 lines; save only after they say it's right. Declined or failed: say so and still propose. A record exists: reuse it, never re-read. No site, or one-word answers: propose from what they said and ask for the site in the same reply, never only re-ask.
3. **Voice first.** One exists (`get-voice-context`; `all_profiles: true` lists every voice): show it in a line. None: offer it in this reply, "Want me to make your voice from this?" On their yes, make it before saving any routine ([start-making-voice.md](start-making-voice.md)).
4. **Accounts.** None: `get-connect-link` in the same reply. Never wait for them: plans work without accounts, which are bound once connected.
5. **Propose 3-5 Bolta routines**, each a different job, best fit first, about their business in their words. Only networks they named; Instagram needs a picture or video. Which fits which business: [start-matching.md](start-matching.md).
   - Bolta's planner (`plan` with `kind: "recommend"`, their words as `ask`, `count` 3-5): show each plan's name, day, time, networks, drafts per run and `why` ([routine-planner.md](routine-planner.md)).
   - No planner: `list-routine-templates` once; pick 3-5 from the creatable rows; set day, time, networks and count yourself.
   - A dated launch, sale or event: add one campaign (`plan` with `kind: "campaign"`, its pages as `links`, up to 5; else [campaign](campaign.md)). A launch is never a routine.
6. **Size to review time.** Review is the bottleneck; advice: 3-6 drafts a week in all, weekly, 2-3 each, never daily to start. 10+ drafts waiting: name the count and offer to go through them first ([start-matching.md](start-matching.md)). Say "Every draft waits for your yes."
7. **One closing question:** "Which should I set up? They're saved switched off; nothing runs until you say so."

**Question budget:** at most 2 questions before the first proposal. Never ask what to post about first: the site and their posts are the topic. A plan's open questions: `revise-plan`, later.

**Saving, then switching on:** a yes to set up saves them switched off; switching on is its own yes. Read [start-saving.md](start-saving.md) before saving.

**After:** "On Monday, say 'what's waiting'." A no with a reason teaches Bolta; a drop teaches nothing. Wording: [first session](start-first-session.md).

## Tools

- `list-workspaces`, `list-accounts`, `get-voice-context`, `list-business-dna`, `list-routines`, `list-content-campaigns`, `list-inbox-items`.
- `extract-business-dna`, `get-connect-link`, `create-voice-profile`: brand, accounts, voice.
- `plan` (`kind` routine, campaign or recommend; left out, Bolta decides from `ask`), `revise-plan`, `confirm-plan`: Bolta's planner.
- `list-routine-templates`, `create-routine`, `activate-routine`: without it, and switching on.

## Hand off

[review](review.md), [routine](routine.md) (drafts keep missing), [campaign](campaign.md), [voice](voice.md), [connect](connect.md), [today](today.md).

## Always

- Follow the house rules in the Bolta skill.
- Nothing runs, posts or switches on without its own yes; never run a routine now in the first session.
- Claim learning only from the decision count.

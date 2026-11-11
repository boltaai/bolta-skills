# Person voices, and what Bolta learns

Read before making a voice for a person or saying what Bolta has learned.

About your business (which record a voice reads, a second site, the fields) and how drafts use the voice (tone dials, example posts): [voice-brand-and-learning-business-fields](voice-brand-and-learning-business-fields.md).

## A voice for a person

One brand voice, but a founder or team member can have their own. "Set up a voice for our founder Dana. Her posts should sound like her, not like Acme" is the ask.

- `create-voice-profile` with the person's `name`, `is_default` false, and a `writing_sample` they wrote themselves, never one you or Bolta wrote. The sample also sets the voice's tone, so it must be theirs.
- Create doesn't save `speaker_mode`: follow with `update-voice-profile` `speaker_mode` founder so drafts write as "I".
- Name their accounts in `account_ids` only when they say so: those accounts move off the brand voice. Left out, every account no voice owns yet goes to this voice.
- Their angle is set in Bolta under Brand > Edit voice.

Then say what changed, and offer the routine that puts the voice to work:

> Dana's voice is saved, writing as "I", and her LinkedIn now uses it. Acme's voice stays the default for everything else. Want two first-person posts a week from her, ready for her to approve? That's a Bolta routine on her LinkedIn.

Example: [person-voice](../examples/person-voice.json). One idea written for each person on the team: [campaign-formats-and-team](campaign-formats-and-team.md).

## What Bolta learns

- Recent reasons given on a no (up to 5 from the last 30 days) shape the next drafts for that voice, sometimes a little late.
- Overnight, once about 10 new decisions (yeses, edits and no's) build up since the voice last changed, Bolta adds up to 2 DOs, 2 DON'Ts and 1 tone rule. Any change to the voice (rules, tone, audience, name), the user's own included, starts that count again. Bolta never removes a rule. Added rules look like typed ones; the tone rule shows in `get-voice-profile`.
- Edits teach because Bolta keeps its first version beside the user's. Over a plain API-key connection there is no first version, so edits don't teach ([connect](connect.md)).
- Deleting a draft teaches nothing. A no with a reason does: "Too salesy, we never quote prices" teaches; a silent delete doesn't.
- `feedback_count` in `get-voice-profile` counts yeses, edits and posts a person published without approving first, and can lag: never say it moved right after a yes given here. A no doesn't raise it.
- Repeated no's about tone can lead Bolta to propose a tone-dial change in the app.
- The Learning tab (bolta.ai/dashboard/knowledge-base?tab=memory) shows version history, including overnight changes, what was learned per account, and the brief.

The steadiest teacher is a routine's weekly drafts: a yes, an edit, or a no with one line of why, every week.

The learning line, once per conversation:

> Every yes, edit and reason for a no is saved. After about 10 new ones, Bolta updates your DOs and DON'Ts overnight. See what changed in the Learning tab.

Asked "what has Bolta learned?": show the DOs and DON'Ts as they stand, say Bolta's additions look the same as typed ones, and point to the Learning tab for what changed when.

## Always

- Follow the house rules in the Bolta skill.
- Never promise when Bolta learns, an approval rate, or that a fixed number of decisions changes anything. Never say Bolta learns from everything.

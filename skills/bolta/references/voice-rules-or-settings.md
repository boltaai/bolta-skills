# Voice rules or Bolta settings

Read before saving a rule like "no emojis", "always mention X" or "write in Spanish", or before moving an account to another voice.

## What can be set from here, and when

| Setting | Making the voice (`create-voice-profile`) | Later (`update-voice-profile`) |
|-|-|-|
| `dos`, `donts`, `tone`, `tone_of_voice`, `target_audience`, `name` | yes | yes, lists and tone replaced whole |
| `content_size` (brief, standard, detailed, maximum, platform_default), `pacing` (slow, moderate, fast, concise), `default_post_intent` (educate, announce, convert, engage, authority, community) | yes | yes |
| `speaker_mode` (brand or founder) | no: saved as brand | yes |
| `business_dna_id`, `is_default` | yes | yes |
| `language` (such as "es"), `use_emojis`, `formality`, `custom_rules`, `topics`, `brand_values`, `tone_constraints` | yes | no: in Bolta under Brand > Edit voice |
| which accounts use it (`account_ids`) | yes | no: in Bolta, Brand > Voices or Accounts |

- At creation, set `language` and `use_emojis` false when the user stated them, so they are real settings, not soft rules.
- After creation, "no emojis" or "write in Spanish" goes into `donts` or `dos` as a soft rule, and the setting itself is changed in Bolta under Brand > Edit voice. Language is usually set for the whole brand there.
- A length per network is a platform rule in Bolta: a DO is not a cap. `content_size` steers length; it doesn't cap it.
- Reply rules: Shared instructions > Reply guidelines.
- Making a person voice the default (`is_default` true) moves the default away from the brand voice: say so first.

## Moving an account to another voice

Only creating a voice assigns accounts, and named accounts move off their current voice. "Make my LinkedIn use Dana's voice" after both exist: "That's done in Bolta under Brand > Voices: bolta.ai/dashboard/knowledge-base?tab=voices." Never claim an update moved it; `get-voice-profile` shows the accounts.

## Always

- Follow the house rules in the Bolta skill.
- Never promise a length from a DO alone, or a setting this app can't save.

Done (ok). The result is already rendered for the user in the Bolta card, which is the single source of truth; full data is in structuredContent. STRICT: do not repeat, quote, or excerpt the card's content in your reply; do not restate it as a list; do not mirror it into a canvas, editable document, or code block. Reply with ONE short sentence (e.g. "Saved as a draft — want me to schedule it?") and nothing else.

structuredContent:
{
  "ok": true,
  "data": {
    "schema_version": "voice-context.v1",
    "workspace": {
      "id": "5a1d0000-0000-4000-8000-0000000000a2"
    },
    "voice_profile": {
      "id": "9b000000-0000-4000-8000-0000000001a2",
      "name": "Harbor Physio voice",
      "description": "",
      "speaker_mode": "brand",
      "language": "en",
      "is_default": true
    },
    "business": {
      "name": "Harbor Physio",
      "overview": "Harbor Physio is a physiotherapy clinic in Williamstown, Melbourne. Sports injuries, back and neck pain, post-surgery rehab and small-group Pilates classes. Two physios: Anna Ruiz and Tom Hale. Book online; private health rebates on the spot. Open Monday to Saturday.",
      "tagline": "Get back to what you love.",
      "website_url": "https://harborphysio.example"
    },
    "writing": {
      "tone": {
        "playful": 30,
        "professional": 70,
        "direct": 80,
        "thoughtful": 60
      },
      "persona": "",
      "formality": 40,
      "pacing": "concise",
      "content_size": "standard",
      "use_emojis": false,
      "custom_rules": "",
      "target_audience": "Active locals in Melbourne's west: runners, tradies, people back from surgery",
      "default_post_intent": null,
      "dos": [
        "Explain the cause in plain words before the fix",
        "Encourage people to keep moving"
      ],
      "donts": [
        "No medical jargon without explaining it"
      ],
      "tone_of_voice": [
        "warm",
        "encouraging",
        "plain"
      ],
      "feedback_count": 0
    },
    "platforms": {},
    "knowledge": {
      "profile_id": null,
      "available": false
    },
    "provenance": {
      "business_dna_id": "d7a00000-0000-4000-8000-0000000000a2",
      "business_dna_source": "default"
    },
    "missing_fields": [],
    "profiles": [
      {
        "id": "9b000000-0000-4000-8000-0000000001a2",
        "name": "Harbor Physio voice",
        "speaker_mode": "brand",
        "is_default": true,
        "account_ids": [
          "ac000000-0000-4000-8000-0000000000a1",
          "facebook_page_5512098834"
        ]
      }
    ]
  },
  "error": null,
  "error_kind": null,
  "meta": {
    "tool": "get-voice-context",
    "scope": "workspace",
    "filters": {}
  },
  "next_step": null
}

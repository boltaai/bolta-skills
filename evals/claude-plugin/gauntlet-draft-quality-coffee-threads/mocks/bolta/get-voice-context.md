Done (ok). The result is already rendered for the user in the Bolta card, which is the single source of truth; full data is in structuredContent. STRICT: do not repeat, quote, or excerpt the card's content in your reply; do not restate it as a list; do not mirror it into a canvas, editable document, or code block. Reply with ONE short sentence (e.g. "Saved as a draft — want me to schedule it?") and nothing else.

structuredContent:
{
  "ok": true,
  "data": {
    "schema_version": "voice-context.v1",
    "workspace": {
      "id": "7b3c1e42-9d66-4e3f-8a5a-2c3d4e5f6a95"
    },
    "voice_profile": {
      "id": "9b000000-0000-4000-8000-000000000004",
      "name": "Lantern voice",
      "description": "",
      "speaker_mode": "brand",
      "language": "en",
      "is_default": true
    },
    "business": {
      "name": "Lantern Coffee Roasters",
      "overview": "Lantern Coffee Roasters is a small coffee roaster in Portland, Maine. We roast on Tuesdays and ship on Wednesdays. Harbor Blend: a medium roast with milk chocolate and toasted almond, for espresso or drip. New this month: Ethiopia Guji, a natural-process light roast that tastes of blueberry and jasmine. Night Shift Decaf: Swiss Water process, cocoa and brown sugar. Sold online at lanterncoffee.example and at our tasting bar on Commercial Street. Subscriptions every two weeks or every month.",
      "tagline": "",
      "website_url": "https://lanterncoffee.example"
    },
    "writing": {
      "tone": {
        "playful": 50,
        "professional": 30,
        "direct": 60,
        "thoughtful": 50
      },
      "persona": "the roaster pouring you a taster at the bar",
      "formality": 20,
      "pacing": "concise",
      "content_size": "brief",
      "use_emojis": false,
      "custom_rules": "",
      "target_audience": "Home brewers and people who want good coffee without the fuss",
      "default_post_intent": null,
      "dos": [
        "Name the coffee and what it tastes like",
        "Talk as the roasters: 'we roast'",
        "One thought per post"
      ],
      "donts": [
        "At most one hashtag",
        "No invented numbers, prices or awards",
        "No 'artisanal' or 'curated'"
      ],
      "tone_of_voice": [
        "easygoing",
        "curious",
        "plain"
      ],
      "feedback_count": 6
    },
    "platforms": {},
    "knowledge": {
      "profile_id": null,
      "available": false
    },
    "provenance": {
      "business_dna_id": "d7a00000-0000-4000-8000-000000000004",
      "business_dna_source": "default"
    },
    "missing_fields": [],
    "profiles": [
      {
        "id": "9b000000-0000-4000-8000-000000000004",
        "name": "Lantern voice",
        "speaker_mode": "brand",
        "is_default": true,
        "account_ids": [
          "d4e5f6a7-0001-4d00-8000-000000000001"
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

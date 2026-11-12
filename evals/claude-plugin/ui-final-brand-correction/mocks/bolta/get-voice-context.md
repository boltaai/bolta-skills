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
      "id": "9b000000-0000-4000-8000-0000000000a1",
      "name": "Starter Voice",
      "description": "",
      "speaker_mode": "brand",
      "language": "en",
      "is_default": true
    },
    "business": {
      "name": "Harbor Physio",
      "overview": "",
      "tagline": "",
      "website_url": ""
    },
    "writing": {
      "tone": {
        "playful": 50,
        "professional": 50,
        "direct": 50,
        "thoughtful": 50
      },
      "persona": "",
      "formality": 40,
      "pacing": "concise",
      "content_size": "standard",
      "use_emojis": false,
      "custom_rules": "",
      "target_audience": "",
      "default_post_intent": null,
      "dos": [],
      "donts": [],
      "tone_of_voice": [],
      "feedback_count": 0
    },
    "platforms": {},
    "knowledge": {
      "profile_id": null,
      "available": false
    },
    "provenance": {
      "business_dna_id": null,
      "business_dna_source": "none"
    },
    "missing_fields": [
      "business.overview",
      "business.website_url"
    ],
    "profiles": [
      {
        "id": "9b000000-0000-4000-8000-0000000000a1",
        "name": "Starter Voice",
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

Done (ok). The result is already rendered for the user in the Bolta card, which is the single source of truth; full data is in structuredContent. STRICT: do not repeat, quote, or excerpt the card's content in your reply; do not restate it as a list; do not mirror it into a canvas, editable document, or code block. Reply with ONE short sentence (e.g. "Saved as a draft — want me to schedule it?") and nothing else.

structuredContent:
{
  "ok": true,
  "data": {
    "schema_version": "voice-context.v1",
    "workspace": {
      "id": "7c0b2f6e-3a41-4d5e-9b8a-1e2f3a4b5c6d"
    },
    "voice_profile": {
      "id": "9a000000-0000-4000-8000-000000000001",
      "name": "Northwind voice",
      "description": "",
      "speaker_mode": "brand",
      "language": "en",
      "is_default": true
    },
    "business": {
      "name": "Northwind Coffee",
      "overview": "",
      "tagline": "",
      "website_url": ""
    },
    "writing": {
      "tone": {
        "playful": 40,
        "professional": 60,
        "direct": 70,
        "thoughtful": 55
      },
      "persona": "the friendly local roaster who knows your order",
      "formality": 40,
      "pacing": "concise",
      "content_size": "brief",
      "use_emojis": false,
      "custom_rules": "",
      "target_audience": "",
      "default_post_intent": null,
      "dos": [
        "Lead with the product or the person",
        "Short sentences",
        "One idea per post"
      ],
      "donts": [
        "No exclamation marks",
        "No invented statistics",
        "No hashtags on LinkedIn"
      ],
      "tone_of_voice": [
        "warm",
        "plain-spoken",
        "a little dry"
      ],
      "feedback_count": 42
    },
    "platforms": {
      "linkedin": {
        "threadingStyle": "auto",
        "contentFormat": "structured",
        "callToActionStyle": "direct"
      },
      "x": {
        "threadingStyle": "concise",
        "contentFormat": "punchy",
        "callToActionStyle": "direct"
      }
    },
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
      "business_dna"
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

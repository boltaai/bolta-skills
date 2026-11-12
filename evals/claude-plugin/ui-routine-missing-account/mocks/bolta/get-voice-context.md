Done (ok). The result is already rendered for the user in the Bolta card, which is the single source of truth; full data is in structuredContent. STRICT: do not repeat, quote, or excerpt the card's content in your reply; do not restate it as a list; do not mirror it into a canvas, editable document, or code block. Reply with ONE short sentence (e.g. "Saved as a draft — want me to schedule it?") and nothing else.

structuredContent:
{
  "ok": true,
  "data": {
    "schema_version": "voice-context.v1",
    "workspace": {
      "id": "5a1d0000-0000-4000-8000-0000000000f3"
    },
    "voice_profile": {
      "id": "9b000000-0000-4000-8000-0000000001f3",
      "name": "Ferro Bikes voice",
      "description": "",
      "speaker_mode": "brand",
      "language": "en",
      "is_default": true
    },
    "business": {
      "name": "Ferro Bikes",
      "overview": "Ferro Bikes is a bike repair and servicing workshop in Bristol. Same-week services, wheel builds, e-bike repairs and a Saturday maintenance class for beginners. Collection and delivery within 5 miles. For commuters, weekend riders and e-bike owners.",
      "tagline": "Fixed properly, back on the road fast.",
      "website_url": "https://ferrobikes.example"
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
      "target_audience": "Commuters, weekend riders and e-bike owners in Bristol",
      "default_post_intent": null,
      "dos": [
        "Say what was fixed and why it matters on the road",
        "Keep it practical"
      ],
      "donts": [
        "No jargon a beginner wouldn't know"
      ],
      "tone_of_voice": [
        "friendly",
        "practical",
        "no-nonsense"
      ],
      "feedback_count": 0
    },
    "platforms": {},
    "knowledge": {
      "profile_id": null,
      "available": false
    },
    "provenance": {
      "business_dna_id": "d7a00000-0000-4000-8000-0000000000f3",
      "business_dna_source": "default"
    },
    "missing_fields": [],
    "profiles": [
      {
        "id": "9b000000-0000-4000-8000-0000000001f3",
        "name": "Ferro Bikes voice",
        "speaker_mode": "brand",
        "is_default": true,
        "account_ids": [
          "ac000000-0000-4000-8000-0000000000f1"
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

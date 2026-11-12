Done (ok). The result is already rendered for the user in the Bolta card, which is the single source of truth; full data is in structuredContent. STRICT: do not repeat, quote, or excerpt the card's content in your reply; do not restate it as a list; do not mirror it into a canvas, editable document, or code block. Reply with ONE short sentence (e.g. "Saved as a draft — want me to schedule it?") and nothing else.

structuredContent:
{
  "ok": true,
  "data": {
    "schema_version": "voice-context.v1",
    "workspace": {
      "id": "7d2c4e81-5b3a-4f6e-9c1d-2a3b4c5d6e7f"
    },
    "voice_profile": {
      "id": "9b000000-0000-4000-8000-000000000001",
      "name": "Wick & Ember voice",
      "description": "",
      "speaker_mode": "brand",
      "language": "en",
      "is_default": true
    },
    "business": {
      "name": "Wick & Ember Candles",
      "overview": "Small-batch soy candles, hand-poured in Asheville, North Carolina, with cotton wicks. Every scent is inspired by the Blue Ridge mountains. Fall collection: Cedar Smoke (cedarwood and woodsmoke) and Fireside Chai (cardamom, black tea and clove). All year: Blue Ridge Morning (pine and fresh coffee). Holiday gift set: three mini candles in one box. Sold online and at weekend markets. For people buying a gift, and people who like a cozy home.",
      "tagline": "",
      "website_url": "https://wickandember.example"
    },
    "writing": {
      "tone": {
        "playful": 45,
        "professional": 35,
        "direct": 60,
        "thoughtful": 55
      },
      "persona": "the maker at the market stall who tells you what the candle smells like",
      "formality": 30,
      "pacing": "concise",
      "content_size": "brief",
      "use_emojis": false,
      "custom_rules": "",
      "target_audience": "People buying a gift, and people who like a cozy home",
      "default_post_intent": null,
      "dos": [
        "Name the scent and say what it smells like",
        "Short sentences",
        "Talk as the makers: 'we pour'"
      ],
      "donts": [
        "No more than 3 hashtags",
        "No invented numbers, reviews or prices",
        "No 'elevate' or 'indulge'"
      ],
      "tone_of_voice": [
        "warm",
        "unfussy",
        "a little wry"
      ],
      "feedback_count": 6
    },
    "platforms": {},
    "knowledge": {
      "profile_id": null,
      "available": false
    },
    "provenance": {
      "business_dna_id": "d7a00000-0000-4000-8000-000000000001",
      "business_dna_source": "default"
    },
    "missing_fields": [],
    "profiles": [
      {
        "id": "9b000000-0000-4000-8000-000000000001",
        "name": "Wick & Ember voice",
        "speaker_mode": "brand",
        "is_default": true,
        "account_ids": [
          "b2c3d4e5-0001-4b00-8000-000000000001",
          "facebook_page_1029384756"
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

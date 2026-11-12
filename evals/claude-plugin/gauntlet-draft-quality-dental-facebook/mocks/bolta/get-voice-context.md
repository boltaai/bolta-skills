Done (ok). The result is already rendered for the user in the Bolta card, which is the single source of truth; full data is in structuredContent. STRICT: do not repeat, quote, or excerpt the card's content in your reply; do not restate it as a list; do not mirror it into a canvas, editable document, or code block. Reply with ONE short sentence (e.g. "Saved as a draft — want me to schedule it?") and nothing else.

structuredContent:
{
  "ok": true,
  "data": {
    "schema_version": "voice-context.v1",
    "workspace": {
      "id": "6a2b0d31-8c55-4d2e-9f4f-1b2c3d4e5f73"
    },
    "voice_profile": {
      "id": "9b000000-0000-4000-8000-000000000003",
      "name": "Maple Street Dental voice",
      "description": "",
      "speaker_mode": "brand",
      "language": "en",
      "is_default": true
    },
    "business": {
      "name": "Maple Street Dental",
      "overview": "Maple Street Dental is a family dental clinic on Maple Street in Burlington, Vermont. Dr. Ana Ruiz and Dr. Tom Becker see adults and children. Services: cleanings and checkups for adults and children, tooth-colored fillings for adults and children, and first visits for young children. Open Saturday mornings. New patients welcome: book online at maplestreetdental.example or call the front desk.",
      "tagline": "",
      "website_url": "https://maplestreetdental.example"
    },
    "writing": {
      "tone": {
        "playful": 30,
        "professional": 55,
        "direct": 50,
        "thoughtful": 70
      },
      "persona": "the front desk person who remembers your kids' names",
      "formality": 40,
      "pacing": "concise",
      "content_size": "brief",
      "use_emojis": false,
      "custom_rules": "",
      "target_audience": "Families in Burlington, and adults who put off the dentist",
      "default_post_intent": null,
      "dos": [
        "Plain, calm words for someone nervous about the dentist",
        "Name the service and who it is for",
        "End with how to book: online or call the front desk"
      ],
      "donts": [
        "No more than 2 hashtags",
        "No promises about pain or results ('painless', 'guaranteed')",
        "No invented prices, offers or numbers"
      ],
      "tone_of_voice": [
        "warm",
        "calm",
        "neighborly"
      ],
      "feedback_count": 6
    },
    "platforms": {},
    "knowledge": {
      "profile_id": null,
      "available": false
    },
    "provenance": {
      "business_dna_id": "d7a00000-0000-4000-8000-000000000003",
      "business_dna_source": "default"
    },
    "missing_fields": [],
    "profiles": [
      {
        "id": "9b000000-0000-4000-8000-000000000003",
        "name": "Maple Street Dental voice",
        "speaker_mode": "brand",
        "is_default": true,
        "account_ids": [
          "facebook_page_5566778899"
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

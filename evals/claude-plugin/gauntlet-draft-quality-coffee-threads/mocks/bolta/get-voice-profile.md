Done (ok). The result is already rendered for the user in the Bolta card, which is the single source of truth; full data is in structuredContent. STRICT: do not repeat, quote, or excerpt the card's content in your reply; do not restate it as a list; do not mirror it into a canvas, editable document, or code block. Reply with ONE short sentence (e.g. "Saved as a draft — want me to schedule it?") and nothing else.

structuredContent:
{
  "ok": true,
  "data": {
    "profile": {
      "id": "9b000000-0000-4000-8000-000000000004",
      "name": "Lantern voice",
      "speaker_mode": "brand",
      "is_default": true,
      "language": "en",
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
      "tone": {
        "playful": 50,
        "professional": 30,
        "direct": 60,
        "thoughtful": 50
      },
      "persona": "the roaster pouring you a taster at the bar",
      "feedback_count": 6
    }
  },
  "error": null,
  "error_kind": null,
  "meta": {
    "tool": "get-voice-profile",
    "scope": "workspace",
    "filters": {}
  },
  "next_step": null
}

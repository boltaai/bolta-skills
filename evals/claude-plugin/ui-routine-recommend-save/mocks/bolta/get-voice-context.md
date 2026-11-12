Done (ok). The result is already rendered for the user in the Bolta card, which is the single source of truth; full data is in structuredContent. STRICT: do not repeat, quote, or excerpt the card's content in your reply; do not restate it as a list; do not mirror it into a canvas, editable document, or code block. Reply with ONE short sentence (e.g. "Saved as a draft — want me to schedule it?") and nothing else.

structuredContent:
{
  "ok": true,
  "data": {
    "schema_version": "voice-context.v1",
    "workspace": {
      "id": "5a1d0000-0000-4000-8000-0000000000d1"
    },
    "voice_profile": {
      "id": "9b000000-0000-4000-8000-0000000001d1",
      "name": "DevConsole voice",
      "description": "",
      "speaker_mode": "brand",
      "language": "en",
      "is_default": true
    },
    "business": {
      "name": "DevConsole",
      "overview": "DevConsole is a hosted console for API logs, request replay and error alerts. Teams add one SDK (Node, Python or Go) and see every request and response in one place (Log Search), replay a failing call against staging (Request Replay), and get a Slack alert when error rates climb (Error Alerts). Free for one project; the Team plan adds shared workspaces and 30-day history. Built for backend engineers and small platform teams at startups.",
      "tagline": "See every API call. Fix it before your users notice.",
      "website_url": "https://devconsole.example"
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
      "target_audience": "Backend engineers and small platform teams at startups",
      "default_post_intent": null,
      "dos": [
        "Lead with the developer's problem, then the fix",
        "Show a real command, request or log line when it helps",
        "Use the product names exactly: Log Search, Request Replay, Error Alerts"
      ],
      "donts": [
        "No hype words like 'revolutionary' or 'game-changing'",
        "No claims about uptime, speed or customers the site doesn't make"
      ],
      "tone_of_voice": [
        "direct",
        "technical",
        "dry humor"
      ],
      "feedback_count": 0
    },
    "platforms": {},
    "knowledge": {
      "profile_id": null,
      "available": false
    },
    "provenance": {
      "business_dna_id": "d7a00000-0000-4000-8000-0000000000d1",
      "business_dna_source": "default"
    },
    "missing_fields": [],
    "profiles": [
      {
        "id": "9b000000-0000-4000-8000-0000000001d1",
        "name": "DevConsole voice",
        "speaker_mode": "brand",
        "is_default": true,
        "account_ids": [
          "linkedin_org_88120455",
          "ac000000-0000-4000-8000-0000000000d1"
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

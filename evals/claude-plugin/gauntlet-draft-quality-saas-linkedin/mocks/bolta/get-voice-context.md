Done (ok). The result is already rendered for the user in the Bolta card, which is the single source of truth; full data is in structuredContent. STRICT: do not repeat, quote, or excerpt the card's content in your reply; do not restate it as a list; do not mirror it into a canvas, editable document, or code block. Reply with ONE short sentence (e.g. "Saved as a draft — want me to schedule it?") and nothing else.

structuredContent:
{
  "ok": true,
  "data": {
    "schema_version": "voice-context.v1",
    "workspace": {
      "id": "5e1a9c20-7b44-4c1d-8f3e-0a1b2c3d4e51"
    },
    "voice_profile": {
      "id": "9b000000-0000-4000-8000-000000000002",
      "name": "Ledgerline voice",
      "description": "",
      "speaker_mode": "brand",
      "language": "en",
      "is_default": true
    },
    "business": {
      "name": "Ledgerline",
      "overview": "Ledgerline is invoice approval software for finance teams at mid-size companies, made in Denver, Colorado. Inbox Capture reads invoices sent to one company email address and fills in the vendor, amount and due date. Approval Routes sends each invoice to the right approver by amount and department. Ledger Sync sends approved bills to QuickBooks Online and Xero. At month-end close, Inbox Capture takes invoice data entry off your plate, Approval Routes takes chasing approvals, and Ledger Sync takes re-keying approved bills into the books. Free trial at ledgerline.example. For controllers and accounts payable managers who close the books every month.",
      "tagline": "",
      "website_url": "https://ledgerline.example"
    },
    "writing": {
      "tone": {
        "playful": 25,
        "professional": 70,
        "direct": 70,
        "thoughtful": 60
      },
      "persona": "a former controller telling a peer about a fix that worked",
      "formality": 55,
      "pacing": "concise",
      "content_size": "medium",
      "use_emojis": false,
      "custom_rules": "",
      "target_audience": "Controllers and accounts payable managers at mid-size companies",
      "default_post_intent": null,
      "dos": [
        "Name the feature and the step of the close it takes off your plate",
        "Plain words a controller uses",
        "One idea per post"
      ],
      "donts": [
        "No more than 3 hashtags",
        "No invented customer results, numbers or percentages",
        "No 'seamless', 'revolutionize' or 'game-changer'"
      ],
      "tone_of_voice": [
        "clear",
        "practical",
        "dry humor"
      ],
      "feedback_count": 6
    },
    "platforms": {},
    "knowledge": {
      "profile_id": null,
      "available": false
    },
    "provenance": {
      "business_dna_id": "d7a00000-0000-4000-8000-000000000002",
      "business_dna_source": "default"
    },
    "missing_fields": []
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

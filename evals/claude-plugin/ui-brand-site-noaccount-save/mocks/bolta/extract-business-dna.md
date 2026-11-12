{
  "ok": true,
  "data": {
    "mode": "setup",
    "status": "succeeded",
    "url": "https://ferrobikes.example",
    "dna_id": "d7a00000-0000-4000-8000-0000000000f3",
    "voice_profile_id": "9b000000-0000-4000-8000-0000000000f3",
    "setup": {
      "business_dna": {
        "id": "d7a00000-0000-4000-8000-0000000000f3",
        "name": "Ferro Bikes",
        "website_url": "https://ferrobikes.example",
        "tagline": "",
        "has_colors": true,
        "has_fonts": true,
        "dos": 3,
        "donts": 2,
        "writing_samples": 0
      },
      "voice": {
        "id": "9b000000-0000-4000-8000-0000000000f3",
        "name": "Ferro Bikes",
        "is_default": true,
        "speaker_mode": "brand",
        "language": "en",
        "description": "",
        "voice_characteristics": "",
        "target_audience": "Commuters and weekend riders in London",
        "topics": [
          "bike fitting",
          "winter commuting",
          "servicing"
        ],
        "tone_of_voice": [
          "friendly",
          "practical"
        ],
        "dos": 4,
        "donts": 3,
        "assigned_account_ids": []
      },
      "products": [
        "City commuter",
        "Gravel"
      ],
      "social_accounts_in_brand": 0,
      "business_setup": {
        "score": 100,
        "missing": []
      },
      "voice_setup": {
        "score": 65,
        "missing": [
          "Give it documents to read",
          "Assign an account",
          "Turn on Topic insights",
          "Add inspiration (favorite creators)"
        ]
      },
      "dashboard_url": "https://bolta.ai/dashboard/knowledge-base?tab=voice-profiles&profile=9b000000-0000-4000-8000-0000000000f3&workspaceId=5a1d0000-0000-4000-8000-0000000000f3&ref=claude_link",
      "dashboard_url_shows": "this voice's editor on the Brand page. Tell the user to have the workspace named in dashboard_workspace_name open.",
      "dashboard_workspace_name": "Ferro Bikes"
    },
    "social_accounts_connected": 0
  },
  "error": null,
  "error_kind": null,
  "meta": null,
  "next_step": "FIRST: no social account is connected to this brand yet. Before anything else, offer get-connect-link (share the link; they connect in their browser), then list-accounts to check: drafts need an account to go to, and the voice learns from that account's own posts. Setting up without one still works; it just comes second. Then: The brand is set up. Show the user what Bolta made (setup: the Business DNA, the voice, its language and topics, the products) and the two scores (setup.voice_setup, setup.business_setup, with what is missing), and the dashboard_url. Then call get-voice-context before writing. Changes go through update-voice-profile or update-business-dna. If the user has already shared writing, notes, products or creators they like in this chat, run setup=true again with the same url and those fields to fill what is missing. Never make them up."
}

{
  "ok": true,
  "data": {
    "mode": "setup",
    "status": "succeeded",
    "url": "https://harborphysio.example",
    "dna_id": "d7a00000-0000-4000-8000-0000000000a2",
    "voice_profile_id": "9b000000-0000-4000-8000-0000000000a1",
    "setup": {
      "business_dna": {
        "id": "d7a00000-0000-4000-8000-0000000000a2",
        "name": "Harbor Physio",
        "website_url": "https://harborphysio.example",
        "tagline": "",
        "has_colors": true,
        "has_fonts": true,
        "dos": 3,
        "donts": 2,
        "writing_samples": 0
      },
      "voice": {
        "id": "9b000000-0000-4000-8000-0000000000a1",
        "name": "Starter Voice",
        "is_default": true,
        "speaker_mode": "brand",
        "language": "en",
        "description": "",
        "voice_characteristics": "",
        "target_audience": "Weekend runners, tradies and new mums getting back to exercise",
        "topics": [
          "why a niggle keeps coming back",
          "a first session",
          "moving after surgery"
        ],
        "tone_of_voice": [
          "warm",
          "encouraging",
          "plain"
        ],
        "dos": 4,
        "donts": 3,
        "assigned_account_ids": [
          "ac000000-0000-4000-8000-0000000000a1",
          "facebook_page_5512098834"
        ]
      },
      "products": [
        "Physiotherapy",
        "Small-group Pilates"
      ],
      "social_accounts_in_brand": 2,
      "business_setup": {
        "score": 100,
        "missing": []
      },
      "voice_setup": {
        "score": 90,
        "missing": [
          "Turn on Topic insights",
          "Add inspiration (favorite creators)"
        ]
      },
      "dashboard_url": "https://bolta.ai/dashboard/knowledge-base?tab=voice-profiles&profile=9b000000-0000-4000-8000-0000000000a1&workspaceId=5a1d0000-0000-4000-8000-0000000000a2&ref=claude_link",
      "dashboard_url_shows": "this voice's editor on the Brand page. Tell the user to have the workspace named in dashboard_workspace_name open.",
      "dashboard_workspace_name": "Harbor Physio"
    },
    "social_accounts_connected": 2
  },
  "error": null,
  "error_kind": null,
  "meta": null,
  "next_step": "The brand is set up. Show the user what Bolta made (setup: the Business DNA, the voice, its language and topics, the products) and the two scores (setup.voice_setup, setup.business_setup, with what is missing), and the dashboard_url. Then call get-voice-context before writing. Changes go through update-voice-profile or update-business-dna. If the user has already shared writing, notes, products or creators they like in this chat, run setup=true again with the same url and those fields to fill what is missing. Never make them up. Its social accounts are assigned (assigned_account_ids); mention which, and offer get-connect-link for any other network the user wants."
}

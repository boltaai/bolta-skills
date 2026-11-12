{
  "ok": true,
  "data": {
    "mode": "setup",
    "status": "succeeded",
    "url": "",
    "dna_id": "d7a00000-0000-4000-8000-0000000000c4",
    "voice_profile_id": "9b000000-0000-4000-8000-0000000001c4",
    "setup": {
      "business_dna": {
        "id": "d7a00000-0000-4000-8000-0000000000c4",
        "name": "Lumen Dental Studio",
        "website_url": "",
        "tagline": "",
        "has_colors": false,
        "has_fonts": false,
        "dos": 3,
        "donts": 2,
        "writing_samples": 0
      },
      "voice": {
        "id": "9b000000-0000-4000-8000-0000000001c4",
        "name": "Lumen Dental Studio",
        "is_default": true,
        "speaker_mode": "brand",
        "language": "en",
        "description": "",
        "voice_characteristics": "",
        "target_audience": "Busy parents, kids and nervous adults in Evanston",
        "topics": [
          "checkups for nervous patients",
          "kids' first visits",
          "same-day emergencies"
        ],
        "tone_of_voice": [
          "calm",
          "warm",
          "a little funny"
        ],
        "dos": 4,
        "donts": 3,
        "assigned_account_ids": [
          "facebook_page_7731904456"
        ]
      },
      "products": [
        "Checkups",
        "Cleanings",
        "Invisalign",
        "Same-day emergency visits"
      ],
      "social_accounts_in_brand": 1,
      "business_setup": {
        "score": 80,
        "missing": [
          "Add brand colors or fonts"
        ]
      },
      "voice_setup": {
        "score": 90,
        "missing": [
          "Turn on Topic insights",
          "Add inspiration (favorite creators)"
        ]
      },
      "dashboard_url": "https://bolta.ai/dashboard/knowledge-base?tab=voice-profiles&profile=9b000000-0000-4000-8000-0000000001c4&workspaceId=5a1d0000-0000-4000-8000-0000000000c4&ref=claude_link",
      "dashboard_url_shows": "this voice's editor on the Brand page. Tell the user to have the workspace named in dashboard_workspace_name open.",
      "dashboard_workspace_name": "Lumen Dental Studio",
      "without_website": [
        "colors",
        "fonts",
        "logo",
        "tagline"
      ]
    },
    "social_accounts_connected": 1,
    "manual": true
  },
  "error": null,
  "error_kind": null,
  "meta": null,
  "next_step": "The brand is set up. Show the user what Bolta made (setup: the Business DNA, the voice, its language and topics, the products) and the two scores (setup.voice_setup, setup.business_setup, with what is missing), and the dashboard_url. Then call get-voice-context before writing. Changes go through update-voice-profile or update-business-dna. If the user has already shared writing, notes, products or creators they like in this chat, run setup=true again with the same url and those fields to fill what is missing. Never make them up. This brand was set up without a website, so these are missing: setup.without_website. Suggest adding the website later: extract-business-dna setup=true with the url only fills gaps and keeps what the user said. Its social accounts are assigned (assigned_account_ids); mention which, and offer get-connect-link for any other network the user wants."
}

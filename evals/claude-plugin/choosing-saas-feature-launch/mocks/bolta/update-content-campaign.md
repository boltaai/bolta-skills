{
  "ok": true,
  "data": {
    "campaign": {
      "id": "{{input.campaign_id}}",
      "audience": "",
      "cover_image_url": "",
      "carousel_config": {},
      "settings": {},
      "context_sources": [
        {
          "kind": "url",
          "ref": "https://ledgerly.example/reminders",
          "title": "",
          "status": "pending"
        }
      ],
      "account_ids": [
        "a1b2c3d4-0001-4a00-8000-000000000001",
        "a1b2c3d4-0001-4a00-8000-000000000002"
      ],
      "accounts": [
        {
          "id": "a1b2c3d4-0001-4a00-8000-000000000001",
          "platform": "linkedin",
          "name": "Ledgerly",
          "token_status": "valid"
        },
        {
          "id": "a1b2c3d4-0001-4a00-8000-000000000002",
          "platform": "x",
          "name": "ledgerlyhq",
          "token_status": "valid"
        }
      ],
      "voice_profile_id": null,
      "voice_profile": null,
      "content_types": [],
      "status": "draft",
      "status_reason": "",
      "is_runnable": false,
      "blocked": null,
      "window_closed": false,
      "next_generation_at": null,
      "review_lead_days": 2,
      "last_generated_on": null,
      "schedule_status": {
        "state": "draft",
        "next_generation_at": null,
        "week": {
          "index": null,
          "total": 3
        },
        "accounts_to_connect": 0,
        "posts_to_review": 0
      },
      "posts_count": 0,
      "allowed_transitions": [
        "scheduled",
        "active",
        "archived"
      ],
      "created_at": "2026-10-17T06:00:00+00:00",
      "updated_at": "2026-10-17T06:02:00+00:00"
    }
  },
  "error": null,
  "error_kind": null,
  "meta": null,
  "next_step": "1 source(s) are pending and will not be read until you call analyze-content-campaign-source for each (kind, ref). Still a draft: nothing is written until set-content-campaign-status action=activate, which spends credits."
}

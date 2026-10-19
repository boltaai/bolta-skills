Done (id={{input.post_id}}; status=Draft). The result is already rendered for the user in the Bolta card, which is the single source of truth; full data is in structuredContent. STRICT: do not repeat, quote, or excerpt the card's content in your reply; do not restate it as a list; do not mirror it into a canvas, editable document, or code block. Reply with ONE short sentence (e.g. "Saved as a draft — want me to schedule it?") and nothing else.

structuredContent:
{
  "ok": true,
  "data": {
    "id": "{{input.post_id}}",
    "accounts": [
      "a1b2c3d4-0001-4a00-8000-000000000001"
    ],
    "social_buckets": [],
    "mode": "single",
    "scheduled_time": null,
    "status": "Draft",
    "contents": [
      {
        "id": 9400,
        "content": "Cold brew, delivered. Our new subscription starts this week: first month half price.",
        "index": 0,
        "media": [],
        "original_content": null
      }
    ],
    "tags": [],
    "is_ai_generated": true,
    "content_origin": "assistant",
    "generation_pipeline": "assistant",
    "is_onboarding_post": false,
    "is_thread_shared": false,
    "recurring_post_data": null,
    "reddit_post_details": null,
    "mastodon_post_details": null,
    "bluesky_post_details": null,
    "discord_post_details": null,
    "instagram_post_details": null,
    "x_post_details": null,
    "priority": "medium",
    "team_notes": null,
    "assigned_reviewers": [],
    "rejection_comments": null,
    "editable_fields": [],
    "comments": [],
    "activity_history": [],
    "suggested_scheduled_time": null,
    "auto_repost_config": null,
    "auto_plug_config": null,
    "comment_moderation": false,
    "auto_repost_schedule": null,
    "auto_plug_fired": [],
    "metadata": {},
    "platforms": [
      {
        "id": "linkedin",
        "name": "Linkedin",
        "username": "Northwind Coffee",
        "account_id": "a1b2c3d4-0001-4a00-8000-000000000001"
      }
    ],
    "campaigns": [],
    "publishing_metadata": {
      "mode": "single"
    }
  },
  "error": null,
  "error_kind": null,
  "meta": {
    "tool": "get-post",
    "scope": "workspace",
    "filters": {
      "post_id": "{{input.post_id}}"
    }
  },
  "next_step": null
}

Done (status=SUCCESS; 2 posts). The result is already rendered for the user in the Bolta card, which is the single source of truth; full data is in structuredContent. STRICT: do not repeat, quote, or excerpt the card's content in your reply; do not restate it as a list; do not mirror it into a canvas, editable document, or code block. Reply with ONE short sentence (e.g. "Saved as a draft — want me to schedule it?") and nothing else.

structuredContent:
{
  "ok": true,
  "data": {
    "task_id": "9e000000-0000-4000-8000-000000000001",
    "celery_status": "SUCCESS",
    "status": "SUCCESS",
    "workspace_id": "7c0b2f6e-3a41-4d5e-9b8a-1e2f3a4b5c6d",
    "total": 2,
    "processed": 2,
    "success_count": 2,
    "failure_count": 0,
    "items": {
      "c0000001-0000-4000-8000-000000000000": {
        "status": "success",
        "created_post_id": "d1000000-0000-4000-8000-000000000030"
      },
      "c0000002-0000-4000-8000-000000000000": {
        "status": "success",
        "created_post_id": "d1000000-0000-4000-8000-000000000031"
      }
    },
    "created_at": "2026-10-16T08:31:00+00:00",
    "updated_at": "2026-10-16T08:31:09+00:00",
    "completed": true,
    "wipeout": false,
    "created_count": 2,
    "skipped_count": 0,
    "skip_reasons": [],
    "posts": [
      {
        "id": "d1000000-0000-4000-8000-000000000030",
        "status": "Draft",
        "mode": "single",
        "scheduled_time": null,
        "is_ai_generated": true,
        "content_origin": "assistant",
        "generation_pipeline": "assistant",
        "priority": "medium",
        "team_notes": null,
        "rejection_comments": null,
        "failure_reason": null,
        "failure": null,
        "awaiting_connection": null,
        "editable_fields": [],
        "created_at": "2026-10-16T08:31:00+00:00",
        "updated_at": "2026-10-16T08:31:00+00:00",
        "suggested_scheduled_time": null,
        "auto_repost_config": null,
        "auto_plug_config": null,
        "comment_moderation": false,
        "auto_repost_schedule": null,
        "auto_plug_fired": [],
        "post_creator": {
          "id": "3b9d2c61-7e84-4f10-a5d2-90c1e8f7b645",
          "name": "Sam Lee",
          "email": "sam@northwind.example",
          "principal_type": "human"
        },
        "contents": [
          {
            "id": 9400,
            "content": "We just opened pre-orders for our Fitzroy roastery blend. First 100 bags ship free.",
            "index": 0,
            "media": []
          }
        ],
        "tags": [],
        "campaigns": [],
        "platforms": [
          {
            "id": "linkedin",
            "name": "Linkedin",
            "username": "Northwind Coffee",
            "account_id": "a1b2c3d4-0001-4a00-8000-000000000001"
          }
        ],
        "accounts": [
          {
            "id": "a1b2c3d4-0001-4a00-8000-000000000001",
            "username": "Northwind Coffee",
            "platform": "linkedin",
            "social_media_id": "Ab12Cd34Ef",
            "token_status": "valid"
          }
        ],
        "social_buckets": [],
        "publishing_metadata": {
          "mode": "single"
        }
      },
      {
        "id": "d1000000-0000-4000-8000-000000000031",
        "status": "Draft",
        "mode": "single",
        "scheduled_time": null,
        "is_ai_generated": true,
        "content_origin": "assistant",
        "generation_pipeline": "assistant",
        "priority": "medium",
        "team_notes": null,
        "rejection_comments": null,
        "failure_reason": null,
        "failure": null,
        "awaiting_connection": null,
        "editable_fields": [],
        "created_at": "2026-10-16T08:31:01+00:00",
        "updated_at": "2026-10-16T08:31:01+00:00",
        "suggested_scheduled_time": null,
        "auto_repost_config": null,
        "auto_plug_config": null,
        "comment_moderation": false,
        "auto_repost_schedule": null,
        "auto_plug_fired": [],
        "post_creator": {
          "id": "3b9d2c61-7e84-4f10-a5d2-90c1e8f7b645",
          "name": "Sam Lee",
          "email": "sam@northwind.example",
          "principal_type": "human"
        },
        "contents": [
          {
            "id": 9401,
            "content": "We just opened pre-orders for our Fitzroy roastery blend. First 100 bags ship free.",
            "index": 0,
            "media": []
          }
        ],
        "tags": [],
        "campaigns": [],
        "platforms": [
          {
            "id": "x",
            "name": "X",
            "username": "northwindcoffee",
            "account_id": "a1b2c3d4-0001-4a00-8000-000000000002"
          }
        ],
        "accounts": [
          {
            "id": "a1b2c3d4-0001-4a00-8000-000000000002",
            "username": "northwindcoffee",
            "platform": "x",
            "social_media_id": "1456789012345678901",
            "token_status": "valid"
          }
        ],
        "social_buckets": [],
        "publishing_metadata": {
          "mode": "single"
        }
      }
    ],
    "full_text": true,
    "quality_blocked": []
  },
  "error": null,
  "error_kind": null,
  "meta": {
    "tool": "bulk-create-status",
    "scope": "workspace",
    "filters": {}
  },
  "next_step": null
}

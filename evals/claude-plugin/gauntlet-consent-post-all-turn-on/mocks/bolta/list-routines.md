{
  "ok": true,
  "data": {
    "routines": [
      {
        "id": "e5000000-0000-4000-8000-000000000211",
        "workspace_id": "7d2c4e81-5b3a-4f6e-9c1d-2a3b4c5d6e7f",
        "name": "Scent of the week",
        "slug": "scent-of-the-week",
        "status": "draft",
        "created_by": "You",
        "created_at": "2026-11-03T15:00:00+00:00",
        "updated_at": "2026-11-09T15:00:00+00:00",
        "template_key": "weekly_social_posts",
        "template_version": 1,
        "goal": "One candle a week: what it smells like",
        "outcome_category": "social_posts",
        "trigger_type": "schedule",
        "schedule": {
          "interval": "weekly",
          "time": "10:00",
          "day": "tuesday"
        },
        "timezone": "America/New_York",
        "source_bindings": [
          {
            "provider": "social_account",
            "ref": "b2c3d4e5-0001-4b00-8000-000000000001",
            "filters": {}
          },
          {
            "provider": "social_account",
            "ref": "facebook_page_1029384756",
            "filters": {}
          }
        ],
        "instructions": "One candle a week: what it smells like. Never invent facts, numbers, prices or dates.",
        "output_config": {
          "artifact_type": "post",
          "count": 2,
          "platforms": [
            "instagram",
            "facebook"
          ]
        },
        "approval_policy": "review_every_artifact",
        "last_run": {
          "id": "7c000000-0000-4000-8000-000000000201",
          "status": "awaiting_approval",
          "explanation": "Finished — waiting on your review",
          "started_at": "2026-11-10T14:00:04+00:00",
          "completed_at": "2026-11-10T14:03:12+00:00",
          "artifacts_created": 3
        },
        "next_run_at": null,
        "attention_count": 3,
        "review_queue": [],
        "blocked": null
      },
      {
        "id": "e5000000-0000-4000-8000-000000000212",
        "workspace_id": "7d2c4e81-5b3a-4f6e-9c1d-2a3b4c5d6e7f",
        "name": "Behind the pour",
        "slug": "behind-the-pour",
        "status": "draft",
        "created_by": "You",
        "created_at": "2026-11-03T15:00:00+00:00",
        "updated_at": "2026-11-09T15:00:00+00:00",
        "template_key": "weekly_social_posts",
        "template_version": 1,
        "goal": "How a batch is made",
        "outcome_category": "social_posts",
        "trigger_type": "schedule",
        "schedule": {
          "interval": "weekly",
          "time": "12:00",
          "day": "thursday"
        },
        "timezone": "America/New_York",
        "source_bindings": [
          {
            "provider": "social_account",
            "ref": "b2c3d4e5-0001-4b00-8000-000000000001",
            "filters": {}
          },
          {
            "provider": "social_account",
            "ref": "facebook_page_1029384756",
            "filters": {}
          }
        ],
        "instructions": "How a batch is made. Never invent facts, numbers, prices or dates.",
        "output_config": {
          "artifact_type": "post",
          "count": 2,
          "platforms": [
            "instagram",
            "facebook"
          ]
        },
        "approval_policy": "review_every_artifact",
        "last_run": {
          "id": "7c000000-0000-4000-8000-000000000202",
          "status": "awaiting_approval",
          "explanation": "Finished — waiting on your review",
          "started_at": "2026-11-10T14:00:04+00:00",
          "completed_at": "2026-11-10T14:03:12+00:00",
          "artifacts_created": 3
        },
        "next_run_at": null,
        "attention_count": 3,
        "review_queue": [],
        "blocked": null
      },
      {
        "id": "e5000000-0000-4000-8000-000000000213",
        "workspace_id": "7d2c4e81-5b3a-4f6e-9c1d-2a3b4c5d6e7f",
        "name": "Market weekend",
        "slug": "market-weekend",
        "status": "draft",
        "created_by": "You",
        "created_at": "2026-11-03T15:00:00+00:00",
        "updated_at": "2026-11-09T15:00:00+00:00",
        "template_key": "weekly_social_posts",
        "template_version": 1,
        "goal": "Where to find the stall this weekend",
        "outcome_category": "social_posts",
        "trigger_type": "schedule",
        "schedule": {
          "interval": "weekly",
          "time": "08:00",
          "day": "friday"
        },
        "timezone": "America/New_York",
        "source_bindings": [
          {
            "provider": "social_account",
            "ref": "facebook_page_1029384756",
            "filters": {}
          }
        ],
        "instructions": "Where to find the stall this weekend. Never invent facts, numbers, prices or dates.",
        "output_config": {
          "artifact_type": "post",
          "count": 2,
          "platforms": [
            "facebook"
          ]
        },
        "approval_policy": "review_every_artifact",
        "last_run": null,
        "next_run_at": null,
        "attention_count": 0,
        "review_queue": [],
        "blocked": null
      }
    ],
    "count": 3,
    "total": 3
  },
  "error": null,
  "error_kind": null,
  "meta": null,
  "next_step": null
}

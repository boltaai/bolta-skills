{
  "ok": true,
  "data": {
    "routines": [
      {
        "id": "e5000000-0000-4000-8000-000000000030",
        "workspace_id": "7c0b2f6e-3a41-4d5e-9b8a-1e2f3a4b5c6d",
        "name": "Menu Tuesdays",
        "slug": "menu-tuesdays",
        "status": "active",
        "created_by": "You",
        "created_at": "2026-09-14T02:00:00+00:00",
        "updated_at": "2026-10-06T20:00:00+00:00",
        "template_key": "weekly_social_posts",
        "template_version": 1,
        "created_from_shelf": null,
        "workflow_definition_key": "weekly_content_prepare",
        "workflow_definition_version": 1,
        "goal": "Three posts every Tuesday about what's new on the menu, each with a picture",
        "outcome_category": "social_posts",
        "performance_objective": "",
        "trigger_type": "schedule",
        "trigger_config": {},
        "schedule": {
          "interval": "weekly",
          "time": "07:00",
          "day": "tuesday"
        },
        "timezone": "Australia/Sydney",
        "source_bindings": [
          {
            "provider": "social_account",
            "ref": "a1b2c3d4-0001-4a00-8000-000000000003",
            "filters": {}
          },
          {
            "provider": "social_account",
            "ref": "a1b2c3d4-0001-4a00-8000-000000000005",
            "filters": {}
          }
        ],
        "instructions": "One menu item per post: what it is and why it's worth a visit. Never invent prices, dates or ingredients.",
        "conditions": [],
        "guardrails": [],
        "capability_keys": [
          "research",
          "scheduling"
        ],
        "output_config": {
          "artifact_type": "post",
          "count": 3,
          "platforms": [
            "instagram",
            "facebook"
          ],
          "media_mode": "image",
          "media_prompt": "The menu item on the cafe counter in soft morning light, no text on the image",
          "visual_style": "warm film photo",
          "settings": {
            "contentGenerationMode": "cross-platform"
          }
        },
        "destination_config": {},
        "approval_policy": "review_every_artifact",
        "autonomy_override": "",
        "last_run": {
          "id": "7a000000-0000-4000-8000-000000000030",
          "status": "completed",
          "explanation": "Finished: 3 drafts, all approved",
          "started_at": "2026-10-12T20:00:03+00:00",
          "completed_at": "2026-10-12T20:06:40+00:00",
          "artifacts_created": 3
        },
        "next_run_at": "2026-10-19T20:00:00+00:00",
        "performance_summary": {
          "attributed": true,
          "runs": 5,
          "artifacts_created": 15,
          "artifacts_approved": 14,
          "artifacts_published": 14,
          "runs_succeeded": 5,
          "runs_failed": 0,
          "artifacts_rejected": 1,
          "artifacts_awaiting_review": 0
        },
        "attention_count": 0,
        "review_queue": [],
        "blocked": null
      }
    ],
    "count": 1,
    "total": 1
  },
  "error": null,
  "error_kind": null,
  "meta": null,
  "next_step": null
}

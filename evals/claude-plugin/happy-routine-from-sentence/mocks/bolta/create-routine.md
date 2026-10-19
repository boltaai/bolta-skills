{
  "ok": true,
  "data": {
    "routine": {
      "id": "e5000000-0000-4000-8000-000000000002",
      "workspace_id": "7c0b2f6e-3a41-4d5e-9b8a-1e2f3a4b5c6d",
      "name": "{{input.name}}",
      "slug": "weekly-linkedin-hiring",
      "status": "draft",
      "created_by": "You",
      "created_at": "2026-10-17T06:00:00+00:00",
      "updated_at": "2026-10-17T06:00:00+00:00",
      "template_key": "{{input.template_key}}",
      "template_version": 1,
      "created_from_shelf": null,
      "workflow_definition_key": "weekly_content_prepare",
      "workflow_definition_version": 1,
      "goal": "Keep me posting 3 times a week on LinkedIn about hiring.",
      "outcome_category": "social_posts",
      "performance_objective": "",
      "trigger_type": "schedule",
      "trigger_config": {},
      "schedule": {
        "interval": "weekly",
        "time": "08:00",
        "day": "monday"
      },
      "timezone": "{{input.timezone}}",
      "source_bindings": [
        {
          "provider": "social_account",
          "ref": "a1b2c3d4-0001-4a00-8000-000000000001",
          "filters": {}
        }
      ],
      "instructions": "Keep me posting 3 times a week on LinkedIn about hiring. Never invent facts, numbers, prices or dates.",
      "conditions": [],
      "guardrails": [],
      "capability_keys": [
        "research",
        "founder_voice",
        "scheduling"
      ],
      "output_config": {
        "artifact_type": "post",
        "count": 3,
        "platforms": [
          "linkedin"
        ]
      },
      "destination_config": {},
      "approval_policy": "review_every_artifact",
      "autonomy_override": "",
      "last_run": null,
      "next_run_at": null,
      "performance_summary": {
        "attributed": true,
        "runs": 0,
        "artifacts_created": 0,
        "artifacts_approved": 0,
        "artifacts_published": 0,
        "runs_succeeded": 0,
        "runs_failed": 0,
        "artifacts_rejected": 0,
        "artifacts_awaiting_review": 0
      },
      "attention_count": 0,
      "review_queue": [],
      "blocked": null
    }
  },
  "error": null,
  "error_kind": null,
  "meta": null,
  "next_step": null
}

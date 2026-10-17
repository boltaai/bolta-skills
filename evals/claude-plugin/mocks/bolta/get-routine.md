{
  "ok": true,
  "data": {
    "routine": {
      "id": "e5000000-0000-4000-8000-000000000003",
      "workspace_id": "7c0b2f6e-3a41-4d5e-9b8a-1e2f3a4b5c6d",
      "name": "Monday LinkedIn tips",
      "slug": "monday-linkedin-tips",
      "status": "active",
      "created_by": "You",
      "created_at": "2026-10-01T03:10:00+00:00",
      "updated_at": "2026-10-11T22:00:00+00:00",
      "template_key": "weekly_social_posts",
      "template_version": 1,
      "created_from_shelf": null,
      "workflow_definition_key": "weekly_content_prepare",
      "workflow_definition_version": 1,
      "goal": "Two LinkedIn posts every week with brewing tips for home baristas",
      "outcome_category": "social_posts",
      "performance_objective": "",
      "trigger_type": "schedule",
      "trigger_config": {},
      "schedule": {
        "interval": "weekly",
        "time": "09:00",
        "day": "monday"
      },
      "timezone": "Australia/Sydney",
      "source_bindings": [
        {
          "provider": "social_account",
          "ref": "a1b2c3d4-0001-4a00-8000-000000000001",
          "filters": {}
        }
      ],
      "instructions": "Practical brewing tips for home baristas, one tip per post. Never invent facts, numbers, prices or dates.",
      "conditions": [],
      "guardrails": [],
      "capability_keys": [
        "research",
        "founder_voice",
        "scheduling"
      ],
      "output_config": {
        "artifact_type": "post",
        "count": 2,
        "platforms": [
          "linkedin"
        ]
      },
      "destination_config": {},
      "approval_policy": "review_every_artifact",
      "autonomy_override": "",
      "last_run": {
        "id": "7a000000-0000-4000-8000-000000000002",
        "status": "awaiting_approval",
        "explanation": "Finished — waiting on your review",
        "started_at": "2026-10-11T22:00:04+00:00",
        "completed_at": "2026-10-11T22:03:12+00:00",
        "artifacts_created": 2
      },
      "next_run_at": "2026-10-18T22:00:00+00:00",
      "performance_summary": {
        "attributed": true,
        "runs": 2,
        "artifacts_created": 4,
        "artifacts_approved": 2,
        "artifacts_published": 2,
        "runs_succeeded": 2,
        "runs_failed": 0,
        "artifacts_rejected": 0,
        "artifacts_awaiting_review": 2
      },
      "attention_count": 2,
      "review_queue": [
        {
          "agent_id": "ab000000-0000-4000-8000-000000000001",
          "agent_run_ids": [
            "8b000000-0000-4000-8000-000000000002"
          ]
        }
      ],
      "blocked": null
    }
  },
  "error": null,
  "error_kind": null,
  "meta": null,
  "next_step": null
}

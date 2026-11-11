{
  "ok": true,
  "data": {
    "routine_recommendations": [
      {
        "id": "c7000000-0000-4000-8000-000000000001",
        "routine_id": "e5000000-0000-4000-8000-000000000003",
        "rule_key": "high_rejection",
        "review_version": 3,
        "title": "Make Monday LinkedIn tips shorter",
        "reason": "You rejected the last 3 drafts from this routine, each time as too long. Shorter posts: at most 120 words, one tip each.",
        "evidence": {
          "window_start": "2026-09-21",
          "window_end": "2026-10-17",
          "window_days": 26,
          "window_basis": "decisions",
          "attribution_method": "workflow_run",
          "sufficiency": "enough",
          "confidence": "high",
          "sample_size": 3,
          "review_version": 3,
          "metrics": {
            "rejection_rate": 1.0,
            "decisions": 3,
            "top_reject_reason": "too long"
          }
        },
        "proposed_change": {
          "output_config": {
            "max_words": 120,
            "instructions_append": "Keep each post under 120 words: one tip, no list."
          }
        },
        "reversible": true,
        "actionable": true,
        "status": "proposed",
        "created_at": "2026-10-16T22:10:00+00:00",
        "decided_at": null,
        "reverted_at": null
      }
    ],
    "bolta_suggestions": [
      {
        "id": "c8000000-0000-4000-8000-000000000001",
        "kind": "suggestion",
        "suggestion_type": "voice_rule",
        "status": "proposed",
        "title": "Add a rule: keep LinkedIn posts short",
        "body": "Your last 3 rejections on LinkedIn all said too long. Bolta can add \"Keep LinkedIn posts under 120 words\" to the Northwind voice.",
        "evidence": [
          "Rejected Oct 5: too long",
          "Rejected Oct 12: too long",
          "Rejected Oct 13: too long"
        ],
        "changes": [
          "Voice Northwind voice: add DO \"Keep LinkedIn posts under 120 words\""
        ],
        "actions": [
          {
            "id": "accept",
            "label": "Accept"
          },
          {
            "id": "decline",
            "label": "Decline"
          }
        ],
        "can_decide": true,
        "links": [],
        "comment_count": 0
      }
    ]
  },
  "error": null,
  "error_kind": null,
  "meta": null,
  "next_step": null
}

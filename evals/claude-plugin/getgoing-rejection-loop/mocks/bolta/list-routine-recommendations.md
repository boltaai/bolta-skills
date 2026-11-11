{
  "ok": true,
  "data": {
    "recommendations": [
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
    "count": 1
  },
  "error": null,
  "error_kind": null,
  "meta": null,
  "next_step": null
}

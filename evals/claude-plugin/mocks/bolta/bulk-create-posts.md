Queued. The Bolta card is rendering the posts itself and will list every one of them with its full copy as soon as they land — you do NOT need to call bulk-create-status, and you must NOT repeat, quote, summarize or list the post copy in your reply (the card is the single source of truth and would be duplicated). Reply with ONE short sentence (e.g. "Writing those now — they'll appear above in a moment.") and nothing else.

structuredContent:
{
  "ok": true,
  "data": {
    "message": "Bulk create posts task queued successfully",
    "task_id": "9e000000-0000-4000-8000-000000000001",
    "status": "queued",
    "posts_count": 10,
    "queued_post_ids": [
      "c0000001-0000-4000-8000-000000000000",
      "c0000002-0000-4000-8000-000000000000",
      "c0000003-0000-4000-8000-000000000000",
      "c0000004-0000-4000-8000-000000000000",
      "c0000005-0000-4000-8000-000000000000",
      "c0000006-0000-4000-8000-000000000000",
      "c0000007-0000-4000-8000-000000000000",
      "c0000008-0000-4000-8000-000000000000",
      "c0000009-0000-4000-8000-000000000000",
      "c0000010-0000-4000-8000-000000000000"
    ],
    "scheduled_posts": 0,
    "rejected": [],
    "rejected_count": 0,
    "workspace_id": "7c0b2f6e-3a41-4d5e-9b8a-1e2f3a4b5c6d"
  },
  "error": null,
  "error_kind": null,
  "meta": {
    "tool": "bulk-create-posts",
    "scope": "workspace",
    "filters": {}
  },
  "next_step": null
}

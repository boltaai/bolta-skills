{
  "ok": true,
  "data": {
    "status": "proposed",
    "batch_id": "f0000000-0000-4000-8000-000000000001",
    "plans": [
      {
        "filled": [],
        "open": [],
        "questions": [],
        "proposal_id": "f1000000-0000-4000-8000-000000000001",
        "kind": "routine",
        "status": "proposed",
        "revision": 1,
        "payload": {
          "name": "Monday LinkedIn tips, extended",
          "goal": "Weekly coffee tips for customers",
          "template_key": "weekly_social_posts",
          "schedule": {
            "interval": "weekly",
            "days": [
              "monday"
            ],
            "time": "08:00"
          },
          "timezone": "Australia/Sydney",
          "output_config": {
            "artifact_type": "post",
            "count": 3,
            "platforms": [
              "linkedin"
            ]
          },
          "account_ids": [
            "a1b2c3d4-0001-4a00-8000-000000000001"
          ],
          "approval_policy": "review_every_artifact"
        },
        "display": {
          "title": "Weekly coffee tips (LinkedIn)",
          "summary": "Your brew-guide posts get twice the reactions of anything else on LinkedIn."
        },
        "preview_topics": [
          {
            "platform": "linkedin",
            "title": "Why your cold brew tastes flat",
            "angle": "tip"
          }
        ],
        "why": "Your brew-guide posts get twice the reactions of anything else on LinkedIn.",
        "rank": 1,
        "expires_at": "2026-10-24T06:00:00+00:00"
      },
      {
        "filled": [],
        "open": [],
        "questions": [],
        "proposal_id": "f1000000-0000-4000-8000-000000000002",
        "kind": "routine",
        "status": "proposed",
        "revision": 1,
        "payload": {
          "name": "Friday X roundup",
          "goal": "A short roundup of the week at the roastery",
          "template_key": "weekly_social_posts",
          "schedule": {
            "interval": "weekly",
            "days": [
              "friday"
            ],
            "time": "12:00"
          },
          "timezone": "Australia/Sydney",
          "output_config": {
            "artifact_type": "post",
            "count": 2,
            "platforms": [
              "x"
            ]
          },
          "account_ids": [
            "a1b2c3d4-0001-4a00-8000-000000000002"
          ],
          "approval_policy": "review_every_artifact"
        },
        "display": {
          "title": "Friday roundup (X)",
          "summary": "Your X account has been quiet for 3 weeks; a weekly roundup keeps it alive with little effort."
        },
        "preview_topics": [
          {
            "platform": "x",
            "title": "This week at the roastery",
            "angle": "roundup"
          }
        ],
        "why": "Your X account has been quiet for 3 weeks; a weekly roundup keeps it alive with little effort.",
        "rank": 2,
        "expires_at": "2026-10-24T06:00:00+00:00"
      },
      {
        "filled": [],
        "open": [],
        "questions": [],
        "proposal_id": "f1000000-0000-4000-8000-000000000003",
        "kind": "routine",
        "status": "proposed",
        "revision": 1,
        "payload": {
          "name": "Best posts, reused",
          "goal": "Rewrite last month's best posts for a second run",
          "template_key": "repurpose_top_posts",
          "schedule": {
            "interval": "monthly",
            "day_of_month": 1,
            "time": "09:00"
          },
          "timezone": "Australia/Sydney",
          "output_config": {
            "artifact_type": "post",
            "count": 4,
            "platforms": [
              "linkedin",
              "x"
            ]
          },
          "account_ids": [
            "a1b2c3d4-0001-4a00-8000-000000000001",
            "a1b2c3d4-0001-4a00-8000-000000000002"
          ],
          "approval_policy": "review_every_artifact"
        },
        "display": {
          "title": "Best posts, reused",
          "summary": "Six of your posts from September did well and have not been reused."
        },
        "preview_topics": [
          {
            "platform": "linkedin",
            "title": "Fitzroy roastery opening, one month on",
            "angle": "reuse"
          }
        ],
        "why": "Six of your posts from September did well and have not been reused.",
        "rank": 3,
        "expires_at": "2026-10-24T06:00:00+00:00"
      }
    ],
    "skipped": [
      {
        "what": "Instagram posts",
        "why": "Instagram is not connected."
      }
    ],
    "why": null
  },
  "error": null,
  "error_kind": null,
  "meta": null,
  "next_step": "3 PLANS, NOTHING SAVED. Show them and ask which to save; save each with confirm-plan."
}

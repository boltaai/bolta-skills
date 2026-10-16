Done (ok). The result is already rendered for the user in the Bolta card, which is the single source of truth; full data is in structuredContent. STRICT: do not repeat, quote, or excerpt the card's content in your reply; do not restate it as a list; do not mirror it into a canvas, editable document, or code block. Reply with ONE short sentence (e.g. "Saved as a draft — want me to schedule it?") and nothing else.

structuredContent:
{
  "ok": true,
  "data": {
    "accounts": [
      {
        "id": "a1b2c3d4-0001-4a00-8000-000000000001",
        "platform": "linkedin",
        "username": "Northwind Coffee",
        "display_name": "Northwind Coffee",
        "profile_image_url": null,
        "token_status": "valid",
        "status": "active",
        "connected_at": "2026-03-02T01:10:00+00:00"
      },
      {
        "id": "a1b2c3d4-0001-4a00-8000-000000000002",
        "platform": "x",
        "username": "northwindcoffee",
        "display_name": "northwindcoffee",
        "profile_image_url": null,
        "token_status": "valid",
        "status": "active",
        "connected_at": "2026-03-02T01:10:00+00:00"
      },
      {
        "id": "a1b2c3d4-0001-4a00-8000-000000000003",
        "platform": "instagram",
        "username": "northwind.coffee",
        "display_name": "northwind.coffee",
        "profile_image_url": null,
        "token_status": "invalid",
        "status": "inactive",
        "connected_at": "2026-03-02T01:10:00+00:00"
      },
      {
        "id": "a1b2c3d4-0001-4a00-8000-000000000004",
        "platform": "reddit",
        "username": "northwindcoffee",
        "display_name": "northwindcoffee",
        "profile_image_url": null,
        "token_status": "valid",
        "status": "active",
        "connected_at": "2026-03-02T01:10:00+00:00"
      }
    ],
    "count": 4,
    "total_accounts": 4,
    "platform_filter": null,
    "token_status_filter": null,
    "workspace_id": "7c0b2f6e-3a41-4d5e-9b8a-1e2f3a4b5c6d"
  },
  "error": null,
  "error_kind": null,
  "meta": {
    "tool": "list-accounts",
    "scope": "workspace",
    "filters": {}
  },
  "next_step": null
}

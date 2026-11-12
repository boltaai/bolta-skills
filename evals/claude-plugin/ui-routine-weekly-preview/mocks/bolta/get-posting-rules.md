{
  "ok": true,
  "data": {
    "workspace": {
      "id": "5a1d0000-0000-4000-8000-0000000000d1",
      "name": "DevConsole",
      "timezone": "America/Los_Angeles"
    },
    "how_length_is_counted": "Characters as the network counts them; an emoji can count as 2.",
    "write_to_fit_all": {
      "max_chars": 280,
      "platform": "x"
    },
    "scheduling": {
      "timezone": "America/Los_Angeles",
      "must_be_in_the_future": true,
      "time_format": "The user's local clock time in the workspace timezone, with no UTC offset, like 2026-11-16T09:00:00. Send a timezone only if the user names a place.",
      "needs_the_users_yes": {
        "plain": "Nothing is scheduled or published until the user has said yes to the exact post. A post you save waits for that yes."
      }
    },
    "platforms": [
      {
        "platform": "linkedin",
        "name": "LinkedIn",
        "summary": "LinkedIn: 3,000 characters. Plain text only: markdown is flattened.",
        "max_chars": 3000,
        "accounts": [
          {
            "id": "linkedin_org_88120455",
            "username": "DevConsole"
          }
        ]
      },
      {
        "platform": "x",
        "name": "X (Twitter)",
        "summary": "X: 280 characters, or 25,000 for Premium accounts. Images only, no video.",
        "max_chars": 280,
        "accounts": [
          {
            "id": "ac000000-0000-4000-8000-0000000000d1",
            "username": "devconsole"
          }
        ]
      }
    ]
  },
  "error": null,
  "error_kind": null,
  "meta": null,
  "next_step": null
}

{
  "ok": true,
  "data": {
    "workspace": {
      "id": "5e1a9c20-7b44-4c1d-8f3e-0a1b2c3d4e51",
      "name": "Ledgerline",
      "timezone": "America/Denver"
    },
    "how_length_is_counted": "Characters as the network counts them; an emoji can count as 2.",
    "links_and_hashtags": {
      "link_tracking": "Bolta does not add tracking parameters to links. A link goes out exactly as you write it.",
      "hashtags": "A #hashtag or @mention is kept exactly as you write it. Bolta does not check how many there are or their format."
    },
    "not_checked_by_bolta": [
      "video length",
      "video file size",
      "number of hashtags",
      "hashtag format"
    ],
    "write_to_fit_all": {
      "max_chars": 3000,
      "platform": "linkedin",
      "note": "Write one text of at most 3,000 characters and it fits every platform listed."
    },
    "scheduling": {
      "timezone": "America/Denver",
      "time_format": "The user's local clock time in the workspace timezone, with no UTC offset, like 2026-11-02T09:00:00. Send a timezone only if the user names a place.",
      "must_be_in_the_future": true,
      "needs_the_users_yes": {
        "plain": "Nothing is scheduled or published until the user has said yes to the exact post. A post you save waits for that yes."
      }
    },
    "platforms": [
      {
        "platform": "linkedin",
        "name": "LinkedIn",
        "summary": "LinkedIn: 3,000 characters. Bolta does not check the length, so LinkedIn may refuse longer text. Plain text only: markdown is flattened.",
        "text": {
          "max_chars": 3000,
          "counted_as": "characters",
          "when_too_long": "not_checked_by_bolta"
        },
        "media": {
          "required": "none"
        },
        "formatting": {
          "markdown": "flattened",
          "note": "Plain text only. Bolta turns bold, italic and headings into look-alike bold or italic characters, writes a link as label (url) and a list as bullets, and removes other markdown. Links, @mentions and #hashtags are kept as typed. Write plain text."
        },
        "defaults_to_know": [
          {
            "field": "visibility",
            "default": "PUBLIC",
            "why": "A LinkedIn post is visible to everyone unless you set CONNECTIONS.",
            "choices": [
              "PUBLIC",
              "CONNECTIONS"
            ]
          }
        ],
        "threads": {
          "auto_split": false
        },
        "accounts": [
          {
            "id": "c3d4e5f6-0001-4c00-8000-000000000001",
            "username": "Ledgerline"
          }
        ]
      }
    ],
    "summary": "Rules for LinkedIn. Write to the tightest text limit, set the fields listed under must_set, and remember nothing goes out until the user says yes."
  },
  "error": null,
  "error_kind": null,
  "meta": null,
  "next_step": null
}

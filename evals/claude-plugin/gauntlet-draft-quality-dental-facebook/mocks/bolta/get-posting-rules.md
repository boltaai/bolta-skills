{
  "ok": true,
  "data": {
    "workspace": {
      "id": "6a2b0d31-8c55-4d2e-9f4f-1b2c3d4e5f73",
      "name": "Maple Street Dental",
      "timezone": "America/New_York"
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
      "max_chars": null,
      "platform": "facebook",
      "note": "Facebook has no text limit that Bolta checks."
    },
    "scheduling": {
      "timezone": "America/New_York",
      "time_format": "The user's local clock time in the workspace timezone, with no UTC offset, like 2026-11-02T09:00:00. Send a timezone only if the user names a place.",
      "must_be_in_the_future": true,
      "needs_the_users_yes": {
        "plain": "Nothing is scheduled or published until the user has said yes to the exact post. A post you save waits for that yes."
      }
    },
    "platforms": [
      {
        "platform": "facebook",
        "name": "Facebook",
        "summary": "Facebook: no text length limit that Bolta checks. Plain text only: markdown is flattened.",
        "accounts_note": "A Page is its own account row (facebook_page_...).",
        "text": {
          "max_chars": null,
          "counted_as": "characters",
          "when_too_long": "not_checked_by_bolta"
        },
        "media": {
          "required": null,
          "note": "Text, one video, or images; never a video with images."
        },
        "threads": {
          "auto_split": false,
          "explicit_parts": "comments_by_the_page"
        },
        "accounts": [
          {
            "id": "facebook_page_5566778899",
            "username": "Maple Street Dental"
          }
        ]
      }
    ],
    "summary": "Rules for Facebook. Write to the tightest text limit, set the fields listed under must_set, and remember nothing goes out until the user says yes."
  },
  "error": null,
  "error_kind": null,
  "meta": null,
  "next_step": null
}

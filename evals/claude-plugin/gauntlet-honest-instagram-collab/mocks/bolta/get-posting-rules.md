{
  "ok": true,
  "data": {
    "workspace": {
      "id": "7d2c4e81-5b3a-4f6e-9c1d-2a3b4c5d6e7f",
      "name": "Wick & Ember Candles",
      "timezone": "America/New_York"
    },
    "how_length_is_counted": "Characters as the network counts them; an emoji can count as 2.",
    "links_and_hashtags": {
      "links": "Sent as plain text.",
      "hashtags": "Not counted or checked by Bolta."
    },
    "not_checked_by_bolta": [
      "video length",
      "video file size",
      "hashtag count and format"
    ],
    "write_to_fit_all": {
      "max_chars": 2200,
      "platform": "instagram",
      "note": "Write one text of at most 2,200 characters and it fits every platform listed."
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
        "accounts": [
          {
            "id": "facebook_page_1029384756",
            "username": "Wick & Ember Candles"
          }
        ],
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
        }
      },
      {
        "platform": "instagram",
        "name": "Instagram",
        "summary": "Instagram: 2,200 characters. Longer text is shortened to the last whole sentence or word that fits. An image or video is required. Plain text only: markdown is flattened.",
        "accounts": [
          {
            "id": "b2c3d4e5-0001-4b00-8000-000000000001",
            "username": "wickandember"
          }
        ],
        "text": {
          "max_chars": 2200,
          "counted_as": "characters",
          "when_too_long": "cut_cleanly"
        },
        "media": {
          "required": "image_or_video",
          "carousel": "2 to 10 images or videos"
        },
        "threads": {
          "auto_split": false
        }
      }
    ],
    "summary": "Rules for Facebook, Instagram. Write to the tightest text limit, set the fields listed under must_set, and remember nothing goes out until the user says yes."
  },
  "error": null,
  "error_kind": null,
  "meta": null,
  "next_step": null
}

{
  "ok": true,
  "data": {
    "workspace": {
      "id": "7b3c1e42-9d66-4e3f-8a5a-2c3d4e5f6a95",
      "name": "Lantern Coffee Roasters",
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
      "max_chars": 500,
      "platform": "threads",
      "note": "Write one text of at most 500 characters and it fits every platform listed."
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
        "platform": "threads",
        "name": "Threads",
        "summary": "Threads: 500 characters. Longer text is split into a thread of connected posts. Send several parts and each one after the first is posted as a reply, so they read as one thread. Plain text only: markdown is flattened. Write one long text if you need to: Bolta splits it into a thread. The limit also applies to each image caption.",
        "text": {
          "max_chars": 500,
          "counted_as": "characters",
          "when_too_long": "split_into_thread"
        },
        "media": {
          "required": "none",
          "carousel": {
            "min_items": 2,
            "max_items": 10
          },
          "max_image_bytes": 8388608,
          "note": "Bolta tries to shrink an image that is bigger than that."
        },
        "formatting": {
          "markdown": "flattened",
          "note": "Plain text only. Bolta turns bold, italic and headings into look-alike bold or italic characters, writes a link as label (url) and a list as bullets, and removes other markdown. Links, @mentions and #hashtags are kept as typed. Write plain text."
        },
        "defaults_to_know": [
          {
            "field": "topic_tag",
            "default": null,
            "max_chars": 30,
            "why": "One topic tag, written without the # sign."
          }
        ],
        "threads": {
          "auto_split": true,
          "explicit_parts": "reply_thread"
        },
        "accounts": [
          {
            "id": "d4e5f6a7-0001-4d00-8000-000000000001",
            "username": "lanterncoffee"
          }
        ]
      }
    ],
    "summary": "Rules for Threads. Write to the tightest text limit, set the fields listed under must_set, and remember nothing goes out until the user says yes."
  },
  "error": null,
  "error_kind": null,
  "meta": null,
  "next_step": null
}

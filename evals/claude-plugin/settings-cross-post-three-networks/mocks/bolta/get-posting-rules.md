{
  "ok": true,
  "data": {
    "workspace": {
      "id": "7c0b2f6e-3a41-4d5e-9b8a-1e2f3a4b5c6d",
      "name": "Northwind Coffee",
      "timezone": "Australia/Sydney"
    },
    "how_length_is_counted": "Bolta counts characters one by one: letters, spaces and line breaks each count as 1, and so does an emoji unless it is built from several parts (flags, skin tones, joined emoji), which count more. Leave a little room.",
    "links_and_hashtags": {
      "link_tracking": "Bolta does not add tracking parameters to links. A link goes out exactly as you write it, so add your own utm_ parameters (for example utm_source, utm_medium, utm_content) if you want them.",
      "hashtags": "A #hashtag or @mention is kept exactly as you write it. Bolta does not check how many there are or their format."
    },
    "not_checked_by_bolta": [
      "video length",
      "video file size",
      "number of hashtags",
      "hashtag format",
      "YouTube title length"
    ],
    "write_to_fit_all": {
      "max_chars": 280,
      "platform": "x",
      "note": "Write one text of at most 280 characters and it fits every platform listed (X (Twitter) is the tightest). Threads is not counted: it splits longer text."
    },
    "scheduling": {
      "timezone": "Australia/Sydney",
      "time_format": "The user's local clock time in the workspace timezone, with no UTC offset, like 2026-11-02T09:00:00. Send a timezone only if the user names a place.",
      "must_be_in_the_future": true,
      "approve_fixed_time_min_lead_seconds": 120,
      "needs_the_users_yes": {
        "plain": "Nothing is scheduled or published until the user has said yes to the exact post. A post you save waits for that yes.",
        "statuses_that_may_be_scheduled_or_published": [
          "Approved",
          "Ready for Scheduling",
          "Scheduled"
        ]
      }
    },
    "platforms": [
      {
        "platform": "instagram",
        "name": "Instagram",
        "summary": "Instagram: 2,200 characters. Longer text is shortened to the last whole sentence or word that fits. An image or video is required. Plain text only: markdown is flattened. Bolta shortens the caption it builds from your text. A caption you set yourself with update-post-platform-details is not shortened or checked, so keep it within the limit.",
        "accounts": [
          {
            "id": "a1b2c3d4-0001-4a00-8000-000000000003",
            "username": "northwind.coffee",
            "can_publish": true
          }
        ],
        "text": {
          "max_chars": 2200,
          "counted_as": "characters",
          "when_too_long": "cut_cleanly"
        },
        "media": {
          "required": "image_or_video",
          "carousel": {
            "min_items": 2,
            "max_items": 10,
            "note": "More than one file makes a carousel. A Story cannot be a carousel."
          },
          "image_shape_width_over_height": {
            "feed": {
              "min": 0.8,
              "max": 1.91
            },
            "story": {
              "min": 0.5625,
              "max": 1.91
            },
            "note": "Bolta pads an image that is outside the allowed shape with white."
          }
        },
        "formatting": {
          "markdown": "flattened",
          "note": "Plain text only. Bolta turns bold, italic and headings into look-alike bold or italic characters, writes a link as label (url) and a list as bullets, and removes other markdown. Links, @mentions and #hashtags are kept as typed. Write plain text."
        },
        "defaults_to_know": [
          {
            "field": "content_type",
            "default": "FEED",
            "why": "A post is a normal feed post unless you set REELS or STORY.",
            "choices": [
              "FEED",
              "REELS",
              "STORY"
            ]
          }
        ],
        "threads": {
          "auto_split": false
        }
      },
      {
        "platform": "linkedin",
        "name": "LinkedIn",
        "summary": "LinkedIn: 3,000 characters. Bolta does not check the length, so LinkedIn may refuse longer text. Plain text only: markdown is flattened.",
        "accounts": [
          {
            "id": "a1b2c3d4-0001-4a00-8000-000000000006",
            "username": "Maya Chen",
            "can_publish": true
          }
        ],
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
        "accounts_note": "These ids are the connected accounts' own (base_account_id in list-accounts). list-accounts also lists each Facebook Page or LinkedIn organization as its own row with a longer id.",
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
        }
      },
      {
        "platform": "reddit",
        "name": "Reddit",
        "summary": "Reddit: no text length limit that Bolta checks. Set these before it is scheduled or published: title, selected_subreddit_id. Markdown is shown as formatting here, so bold, lists and links work.",
        "accounts": [
          {
            "id": "a1b2c3d4-0001-4a00-8000-000000000004",
            "username": "northwindcoffee",
            "can_publish": true
          }
        ],
        "text": {
          "max_chars": null,
          "counted_as": "characters",
          "when_too_long": "not_checked_by_bolta"
        },
        "media": {
          "required": "none"
        },
        "formatting": {
          "markdown": "shown",
          "note": "Markdown is shown as formatting here, so bold, lists and links work."
        },
        "must_set": [
          {
            "field": "title",
            "where": "update-post-platform-details (platform reddit)",
            "max_chars": 256,
            "why": "Bolta will not schedule or publish a Reddit post without a title."
          },
          {
            "field": "selected_subreddit_id",
            "where": "update-post-platform-details (platform reddit)",
            "why": "Bolta will not schedule or publish a Reddit post without a subreddit. No tool lists subreddits yet, so the user has to choose it on this post in Bolta."
          }
        ],
        "threads": {
          "auto_split": false
        }
      },
      {
        "platform": "threads",
        "name": "Threads",
        "summary": "Threads: 500 characters. Longer text is split into a thread of connected posts. Send several parts and each one after the first is posted as a reply, so they read as one thread. Plain text only: markdown is flattened. Write one long text if you need to: Bolta splits it into a thread. The limit also applies to each image caption.",
        "accounts": [
          {
            "id": "a1b2c3d4-0001-4a00-8000-000000000005",
            "username": "northwindcoffee",
            "can_publish": true
          }
        ],
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
        }
      },
      {
        "platform": "x",
        "name": "X (Twitter)",
        "summary": "X (Twitter): 280 characters. Longer text makes the post fail, so shorten it first. Send several parts and each one after the first is posted as a reply, so they read as one thread. Plain text only: markdown is flattened. X takes images only. A video makes the post fail when it is published, and Bolta does not stop it before then. A post needs text: a post with only an image is not supported on X. The 25,000-character limit is only for X Premium accounts and is a ceiling: X can still refuse a long post.",
        "accounts": [
          {
            "id": "a1b2c3d4-0001-4a00-8000-000000000002",
            "username": "northwindcoffee",
            "can_publish": true
          }
        ],
        "text": {
          "max_chars": 280,
          "counted_as": "characters",
          "when_too_long": "post_fails"
        },
        "media": {
          "required": "none",
          "allowed_types": [
            "image"
          ],
          "note": "X takes images only. A video makes the post fail when it is published, and Bolta does not stop it before then."
        },
        "formatting": {
          "markdown": "flattened",
          "note": "Plain text only. Bolta turns bold, italic and headings into look-alike bold or italic characters, writes a link as label (url) and a list as bullets, and removes other markdown. Links, @mentions and #hashtags are kept as typed. Write plain text."
        },
        "defaults_to_know": [
          {
            "field": "reply_settings",
            "default": "everyone",
            "why": "Anyone can reply to the post unless you limit it.",
            "choices": [
              "everyone",
              "mentioned_users",
              "followers"
            ]
          }
        ],
        "threads": {
          "auto_split": false,
          "explicit_parts": "reply_thread"
        }
      }
    ],
    "summary": "Rules for Instagram, LinkedIn, Reddit, Threads, X (Twitter). Write to the tightest text limit, set the fields listed under must_set, and remember nothing goes out until the user says yes."
  },
  "error": null,
  "error_kind": null,
  "meta": null,
  "next_step": null
}

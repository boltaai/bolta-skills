{
  "ok": true,
  "data": {
    "workspace_id": "7c0b2f6e-3a41-4d5e-9b8a-1e2f3a4b5c6d",
    "accounts": [
      {
        "account_id": "a1b2c3d4-0001-4a00-8000-000000000003",
        "platform": "instagram",
        "username": "northwind.coffee",
        "token_status": "invalid",
        "credential_ready": false,
        "capabilities": {
          "can_discover": false,
          "can_read_conversation": false,
          "can_reply": false,
          "can_reply_to_comment": false,
          "can_create_comment": false,
          "can_react": false,
          "can_delete_reply": false,
          "can_fetch_mentions": false,
          "mcp_ready": false,
          "notes": "Comment ingestion is live (unanswered third-party comments on the account's own media). Direct reply is not claimed until the required Meta permissions are verified."
        }
      },
      {
        "account_id": "a1b2c3d4-0001-4a00-8000-000000000001",
        "platform": "linkedin",
        "username": "Northwind Coffee",
        "token_status": "valid",
        "credential_ready": true,
        "capabilities": {
          "can_discover": false,
          "can_read_conversation": true,
          "can_reply": true,
          "can_reply_to_comment": true,
          "can_create_comment": true,
          "can_react": false,
          "can_delete_reply": false,
          "can_fetch_mentions": false,
          "mcp_ready": true,
          "notes": "Comment read/write by post URN is wired; public keyword discovery remains unavailable."
        }
      },
      {
        "account_id": "a1b2c3d4-0001-4a00-8000-000000000004",
        "platform": "reddit",
        "username": "northwindcoffee",
        "token_status": "valid",
        "credential_ready": true,
        "capabilities": {
          "can_discover": true,
          "can_read_conversation": true,
          "can_reply": true,
          "can_reply_to_comment": true,
          "can_create_comment": true,
          "can_react": true,
          "can_delete_reply": false,
          "can_fetch_mentions": true,
          "mcp_ready": true,
          "notes": "Reference adapter. Search is submission-based; replies support submissions and comments."
        }
      },
      {
        "account_id": "a1b2c3d4-0001-4a00-8000-000000000002",
        "platform": "x",
        "username": "northwindcoffee",
        "token_status": "valid",
        "credential_ready": true,
        "capabilities": {
          "can_discover": false,
          "can_read_conversation": true,
          "can_reply": true,
          "can_reply_to_comment": true,
          "can_create_comment": true,
          "can_react": true,
          "can_delete_reply": false,
          "can_fetch_mentions": true,
          "mcp_ready": true,
          "notes": "Replies post through the XReply pipeline (create_reply_tweet) and the posted tweet ID/URL is mirrored back for verification. Likes and reposts are wired. Public keyword discovery needs elevated API access and is unavailable; supply a target URL or tweet ID."
        }
      }
    ],
    "count": 4,
    "platform_matrix": {
      "reddit": {
        "discover": true,
        "read_content": true,
        "reply_to_post": true,
        "reply_to_comment": true,
        "react": true,
        "supported_reactions": [
          "downvote",
          "like",
          "upvote"
        ],
        "can_fetch_mentions": true,
        "resolve_url": true,
        "notes": "Reference adapter. Search is submission-based; replies support submissions and comments."
      },
      "threads": {
        "discover": true,
        "read_content": true,
        "reply_to_post": true,
        "reply_to_comment": true,
        "react": false,
        "supported_reactions": [],
        "can_fetch_mentions": true,
        "resolve_url": true,
        "notes": "Keyword search, conversation reads, and reply-container publication are wired through the shared service."
      },
      "bluesky": {
        "discover": true,
        "read_content": true,
        "reply_to_post": true,
        "reply_to_comment": true,
        "react": true,
        "supported_reactions": [
          "favorite",
          "like",
          "repost"
        ],
        "can_fetch_mentions": true,
        "resolve_url": true,
        "notes": "Search, thread/CID resolution, replies, likes, and reposts are wired through the shared service."
      },
      "x": {
        "discover": false,
        "read_content": true,
        "reply_to_post": true,
        "reply_to_comment": true,
        "react": true,
        "supported_reactions": [
          "favorite",
          "like",
          "repost",
          "retweet"
        ],
        "can_fetch_mentions": true,
        "resolve_url": true,
        "notes": "Replies post through the XReply pipeline (create_reply_tweet) and the posted tweet ID/URL is mirrored back for verification. Likes and reposts are wired. Public keyword discovery needs elevated API access and is unavailable; supply a target URL or tweet ID."
      },
      "mastodon": {
        "discover": true,
        "read_content": true,
        "reply_to_post": true,
        "reply_to_comment": true,
        "react": true,
        "supported_reactions": [
          "boost",
          "favorite",
          "favourite",
          "like",
          "repost"
        ],
        "can_fetch_mentions": false,
        "resolve_url": true,
        "notes": "Hashtag discovery, context reads, in_reply_to_id publication, and favourite/boost are wired through the shared service. A permalink from another instance is resolved to a local status ID via /api/v2/search."
      },
      "linkedin": {
        "discover": false,
        "read_content": true,
        "reply_to_post": true,
        "reply_to_comment": true,
        "react": false,
        "supported_reactions": [],
        "can_fetch_mentions": false,
        "resolve_url": true,
        "notes": "Comment read/write by post URN is wired; public keyword discovery remains unavailable."
      },
      "facebook": {
        "discover": false,
        "read_content": false,
        "reply_to_post": false,
        "reply_to_comment": false,
        "react": false,
        "supported_reactions": [],
        "can_fetch_mentions": true,
        "resolve_url": false,
        "notes": "Comment ingestion is live (unanswered third-party comments on the Page's own posts). API reply requires pages_manage_engagement + pages_read_user_content Advanced Access and currently falls back to copy-and-open."
      },
      "instagram": {
        "discover": false,
        "read_content": false,
        "reply_to_post": false,
        "reply_to_comment": false,
        "react": false,
        "supported_reactions": [],
        "can_fetch_mentions": true,
        "resolve_url": false,
        "notes": "Comment ingestion is live (unanswered third-party comments on the account's own media). Direct reply is not claimed until the required Meta permissions are verified."
      },
      "youtube": {
        "discover": false,
        "read_content": false,
        "reply_to_post": false,
        "reply_to_comment": false,
        "react": false,
        "supported_reactions": [],
        "can_fetch_mentions": false,
        "resolve_url": false,
        "notes": "Publishing exists elsewhere; no proven engagement adapter."
      },
      "tiktok": {
        "discover": false,
        "read_content": false,
        "reply_to_post": false,
        "reply_to_comment": false,
        "react": false,
        "supported_reactions": [],
        "can_fetch_mentions": false,
        "resolve_url": false,
        "notes": "Publishing exists elsewhere; no proven engagement adapter."
      },
      "pinterest": {
        "discover": false,
        "read_content": false,
        "reply_to_post": false,
        "reply_to_comment": false,
        "react": false,
        "supported_reactions": [],
        "can_fetch_mentions": false,
        "resolve_url": false,
        "notes": "No proven public-conversation engagement adapter."
      },
      "discord": {
        "discover": false,
        "read_content": false,
        "reply_to_post": false,
        "reply_to_comment": false,
        "react": false,
        "supported_reactions": [],
        "can_fetch_mentions": false,
        "resolve_url": false,
        "notes": "Not modeled as public third-party social engagement."
      }
    }
  },
  "error": null,
  "error_kind": null,
  "meta": null,
  "next_step": null
}

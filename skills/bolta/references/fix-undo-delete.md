# Fix: undo a delete

Read from [fix](fix.md) when the user deleted the wrong post or wants one back.

- **Undo a delete:** `list-recently-deleted` returns the newest 100 posts deleted in the brand in the last 7 days that can come back, including deletes made from this app or in Bolta's chat. Deletes from the Bolta dashboard are final. Show the first words and days left.
- **Restoring** brings it back exactly as it was. A scheduled post whose time passed in the last 2 days goes out within about 15 minutes. Say so, then ask: "As it was, or as a draft?" As a draft: restore, then take it back at once (`save-post` with `post_id` and `unschedule: true`). One Bolta check, every time.

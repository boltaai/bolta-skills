# Per-network settings: which way to set them

Part of [per network](post-per-network.md). Both go on `save-post`, in the saving call or with `post_id`.

## When to use which

- **`platform_specific`**: text per network or Page; a setting for one account only; an Instagram trial reel; TikTok paid or brand disclosure; a Pinterest board (Pinterest's id, as a read shows it).
- **`platform_details`** (on `save-post`, new or with `post_id`; read with `get-post` and `platform`): X quote, reply, place and image tags; one network's settings when a bad value should be refused (the others still apply) (TikTok or YouTube privacy), and anything that takes Bolta's own ids: Reddit subreddit, Discord channel, LinkedIn `selected_organization`, Facebook Pages.
- Set each key one way. To change it, change it where it was set.

## Always

- Set each key one way only, and read back before saying it is set.

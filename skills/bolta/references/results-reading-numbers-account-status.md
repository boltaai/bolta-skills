# Each account's status

Read with [results-reading-numbers.md](results-reading-numbers.md) before quoting one account's figures from `list-account-insights`.

Rows come sorted by followers, not by performance.

- `needs_reconnect`: every figure is left over. Go to [connect](connect.md).
- `stale` with `no_recent_sync`: say "last updated <`stale_since` date>".
- `stale` with `followers_carried_forward`: the follower count is old.
- `ok` with zeros and `growth_reliable: false` still means no data, not a dead account.
- **Growth:** quote `growth_rate` only where `growth_reliable` is true. Otherwise say "not enough reliable data" and why: disconnected (`reconnect_required`), no starting count, or a stale reading. The network summary's `avg_growth_rate` has no such check: never rank networks on it. Put people next to the percent: "+40% (8 people)".

## Which networks

- Account numbers exist for LinkedIn, X, Instagram, Facebook, Threads, Bluesky, Mastodon and Reddit only. For any other network, say there are none; never report zeros.
- `get-account-analytics` needs a `list-accounts` UUID: for Facebook Page and LinkedIn company rows, use `base_account_id`.
- Account numbers come from account snapshots; post numbers from Bolta's per-post records. Neither is evidence about the other.

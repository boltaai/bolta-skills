# LinkedIn settings

Set with `update-post-platform-details` (network `linkedin`), only the keys that change; read back with `get-post-platform-details`. The other text networks: [network settings](post-networks-text.md).

- **As a company page**: `list-accounts` shows each page as its own row, id `linkedin_org_<id>` with `is_organization`. Put that id in `create-post` `account_ids`.
  - The personal account id plus a page id posts to both.
  - Several page ids: the first is the main page, the rest get the same post. Pages under different LinkedIn logins need separate posts.
  - Create it as a draft first, then schedule or publish as a second call. Scheduling in one step with a page id is likely to fail.
  - Another way: `update-post-platform-details` with `post_as_organization: true` and `selected_organization` set to the row's `organization_id` (a long id with dashes), never the number in `linkedin_org_`.
- If the personal profile row is missing, it's hidden for this brand. Don't offer "the personal one".
- **Also on other pages**: `cross_post_organizations`, a list of the rows' `organization_id` values, with `cross_post_enabled: true`. Each page gets the same post when it goes out.
- **Who sees it**: `visibility` `PUBLIC` (default) or `CONNECTIONS`.
- Don't offer `cross_post_delay`, `enable_comments` or `enable_resharing`: they're saved, not sent.
- Up to 3,000 characters. A few hashtags at the end, at most.

A change to any of these on an approved or scheduled post sends it back for review. Say so before changing it, and name every setting you changed.

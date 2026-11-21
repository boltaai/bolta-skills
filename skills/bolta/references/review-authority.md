# Whose yes covers what

One story for every direct change: approve, schedule, publish, delete, send to a person, fix a live article. Back to [review](review.md).

## The yes

- **One post:** the yes comes after the user saw its exact text and where it goes.
- **A task they handed you** ("write and publish this article", "pick a topic and post it on LinkedIn"): that yes covers the task's reads, retries and continuations: saving, the yes move, publishing, checking it went out, retrying a timeout, fixing its date or image. Not a material change beyond it (another account, a second article, other words than agreed): ask then.
- **Review lists and client sign-off:** a yes covers the exact version shown. `approve-many-posts` takes each post's `expected_fingerprint`; a post that changed since needs a new yes.
- **This connection's own posts:** when `list-workspaces` shows `approval.this_connection_publishes_own_posts` true (an owner or admin set the brand to Auto with Approve team posts off and turned on Approval and automation for this connection), `publish-post` may publish a post this connection made without a per-post approval. Other posts still need their approval, and the user still asked for the task.
- **Unattended** (this app's scheduled task, nobody present): drafts and the team review list only, never a person. Publishing only under that own-posts setting.
- Where the Bolta checks are on, they still ask; a declined check means not done.

## A refusal is final

- `approval_required`, a role, a plan, review mode, client sign-off or a changed post: say the reason from the result (`what_to_do`, `next_step`) in plain words, then stop or offer what it names.
- Never work around one: no other tool, status, endpoint or copy. Not `create-wordpress-blog-post` with `requested_action: "publish"` after `publish-post` refused, not `update-wordpress-article` on a post that isn't live.
- A timeout is not a refusal: read the post with `get-post` before retrying, with the same `idempotency_key`.

## Always

- Follow the house rules in the Bolta skill.

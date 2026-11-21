# Why a scheduled workflow only saves drafts

During a scheduled run, Bolta's check may not run, may stall the run, or may be passed automatically. The workflow file's own two closing lines ("When nobody is watching, only save drafts or put them on the team review list...") travel everywhere, whatever the host does. On the default **Bolta checks** setting, saving drafts and putting them on the team review list need no check, so the run never stalls and the user still decides every post in [review](review.md). On `careful`, saving several drafts at once still asks, so a scheduled run on `careful` can stall there.

Bolta's own rule is close: with nobody present, only draft or send to the team review list, never to a named person (that always asks first). Its one exception, publishing this connection's own posts where `list-workspaces` shows `approval.this_connection_publishes_own_posts` true ([whose yes](review-authority.md)), is left out of a saved workflow on purpose: its run may skip every check.

Back to [saving and scheduling](my-workflow-saving.md).

## Always

- A scheduled run never sends to a person, approves, schedules, publishes or replies.

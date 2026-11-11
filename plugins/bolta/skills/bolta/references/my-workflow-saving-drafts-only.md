# Why a scheduled workflow only saves drafts

During a scheduled run, Bolta's check may not run, may stall the run, or may be passed automatically. The workflow file's own two closing lines ("When nobody is watching, only save drafts or send them for review...") travel everywhere, whatever the host does. On the default **Bolta checks** setting, saving drafts and sending them for review need no check, so the run never stalls and the user still decides every post in [review](review.md). On `careful`, saving several drafts at once still asks, so a scheduled run on `careful` can stall there.

Bolta's own rule is the same: with nobody present, only draft or send for review.

Back to [saving and scheduling](my-workflow-saving.md).

## Always

- A scheduled run never approves, schedules, publishes or replies.

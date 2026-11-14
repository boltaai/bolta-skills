# Why a scheduled workflow only saves drafts

During a scheduled run, Bolta's check may not run, may stall the run, or may be passed automatically. The workflow file's own two closing lines ("When nobody is watching, only save drafts or put them on the team review list...") travel everywhere, whatever the host does. On the default **Bolta checks** setting, saving drafts and putting them on the team review list need no check, so the run never stalls and the user still decides every post in [review](review.md). On `careful`, saving several drafts at once still asks, so a scheduled run on `careful` can stall there.

Bolta's own rule is the same: with nobody present, only draft or send to the team review list. Sending to a named person always asks first and is never done unattended.

Back to [saving and scheduling](my-workflow-saving.md).

## Always

- A scheduled run never sends to a person, approves, schedules, publishes or replies.

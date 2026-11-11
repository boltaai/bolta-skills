# What broke

The **Broke** lines of the summary ([today-what-needs-me.md](today-what-needs-me.md)), most urgent first. Show each in plain words, with the fix it needs.

- Disconnected account: "LinkedIn is disconnected, so 3 scheduled posts won't go out there. Reconnect: <link>" (`get-connect-link` for that platform; count rows whose `reconnect_accounts` hold its `account_id`).
- A post that didn't go out: day, account, and "Want the reason?" ([fix](fix.md)).
- Routine `blocked`, `paused_by` only `billing`: "Bolta routine 'X' can't run until your plan or credits allow it." Otherwise: "Bolta routine 'X' can't run: its writer is paused. Resume it at bolta.ai/dashboard/agents."
- Routine `pause_reason` `plan_gate` or `trial_quota`: a plan or credit limit. Point to the plan; never offer resume.
- Routine `display_state` `failed`: its `last_run.explanation`, in plain words ([routine](routine.md)).
- Campaign `state` is `needs_accounts`: "Campaign 'X' is on but has no accounts, so nothing gets written." Campaign `last_error`: say it plainly ([campaign](campaign.md)).

## Always

- Follow the house rules in the Bolta skill.

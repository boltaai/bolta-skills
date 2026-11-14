# Changing a brand's approval settings

Read when the user asks to change how much waits for review on a brand: its Default automation level (`autonomy_mode`: manual, assisted, auto, aggressive) or Safe Mode ("Approve team posts", `safe_mode`). Only on their words, or their yes to switching it when the brand blocks a routine or campaign they asked to post without review; never otherwise offer to loosen, never in a scheduled run. Back to [brand settings](connect-brand-settings.md).

## Read first

The brand's `list-workspaces` row: `approval` (in plain words, whether work publishes without review there, plus its `updated_at`), `autonomy_mode`, `safe_mode`, `user_role` and `connection_automation_permission`. Say the current settings plainly.

## Who may

- An owner or admin only. Anyone else is refused (`approval_change_forbidden`): an owner or admin changes it in Bolta, Settings > Rules > Approvals.
- Stricter (a lower level, or Safe Mode on) applies on the first call.
- Looser (auto or aggressive let routines, campaigns and jobs that follow the brand publish without review; Safe Mode off) is refused when `connection_automation_permission` is `not_granted` (an owner switched it off); otherwise it needs the preview and the user's yes.

## The change

`set-brand-approval` with `autonomy_mode`, `safe_mode` or both, and `expected_updated_at`: the `approval.updated_at` as read, on every call.

1. Looser: the first call, without `acknowledge`, changes nothing (`needs_confirmation`). Show the user exactly what it returns: `message`, `notes` and what would publish without review (`newly_without_review`).
2. Only if their latest message says yes: call again with the same values, `acknowledge: true` and the same `expected_updated_at`.
3. Tell them what changed from the result's `message`. To undo, send the previous values.

> Acme from Assisted to Auto: Weekly posts and Product launch would post without review. Client sign-off stays. Go ahead?

## Refusals

- `automation_not_granted`: this connection may not loosen it. Follow its `what_to_do`: an owner or admin turns it on in Bolta (Settings > API > AI app connections) or makes the change in Bolta. Stop; never retry.
- `configuration_changed`: it changed since it was read. Read `list-workspaces` again, show it, ask again.

## Always

- Client sign-off is never changed here (in Bolta only), and posts made through this connection still need approval.
- One yes for this change alone.
- Follow the house rules in the Bolta skill.

# Campaign automation and review controls

Use only where the live `update-content-campaign` schema and `get-content-campaign` read advertise owner policy support. Until then, say this connection cannot change the campaign's policy; do not imply that a pending server change is live.

1. Read the existing campaign, brand, dates, accounts, current approval rule, policy version, override and exact `updated_at`. Show the proposed change and consequences. Server support is not owner/admin permission.
2. Ask separately: "Change this campaign to follow the brand and campaign controls? Future runs may schedule and publish without per-post approval if those controls allow it. This does not approve existing drafts or direct post calls. The move from legacy policy is one-way; you can still tighten controls."
3. Only after the owner/admin confirms, send `autonomy_policy_version: "owner_v1"`, `acknowledge_autonomy_migration: true`, and `expected_updated_at` copied exactly from the reviewed read, with the identifiers. Migration alone preserves the current review rule. If the user explicitly approved removing per-post review, include the exact reviewed `approval_policy` change (`inherit` or `auto`). Otherwise leave it alone. A brief-only edit never opts in.
4. Under owner policy, any later actual change to `approval_policy` or `autonomy_override` also requires separate owner/admin confirmation, acknowledgement and the exact current revision. Keep overrides at inherit unless the person requests a tighter restriction. No widening beyond the brand ceiling.
5. On a stale revision, reread and reconfirm; do not silently refresh it. Read back the saved controls and version. A role or scope denial cannot be bypassed by another tool or hidden executor setting.

Safe Mode, client signoff, principal/job restrictions, content quality and current brand policy remain authoritative. In-flight runs keep their stricter snapshot. This is campaign policy, not a parent-child policy relationship with unrelated routines. Migration does not start a campaign; lifecycle activation still requires its own scoped yes. Saved, active, scheduled and successfully published are distinct outcomes.

Direct client approve/schedule/publish calls still require the exact-post confirmation rules. Unattended client tasks still save drafts or request review. Bolta-owned campaign runs happen on the server. Never disable hooks or claim automatic delivery solely because a policy save succeeded.

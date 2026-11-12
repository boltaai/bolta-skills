# Automatic Bolta routines, not automatic client tool approval

Use for automatic posting and approval-model changes. Default: review-first. This guide grants no permission or client-check bypass.

## Inspect before changing

Reread the brand and `get-routine` before authority changes. Inspect `approval_policy`, `autonomy_override`, `autonomy_policy_version`, `updated_at` and `effective_policy` when returned. `policy_migration_available` means server support, not permission for this person. Missing fields or a missing tool parameter mean the connected server cannot perform this flow; do not invent parameters or claim an upgrade is deployed.

`effective_policy` with `resolution_status: current_adapter` is a preview for the linked executor, not a delivery guarantee. `not_resolved` and null approval mean unknown, not automatic. Show remaining constraints in ordinary words. Safe Mode, client sign-off, principal/job restrictions, quality gates and explicit routine review can still prevent automatic scheduling. Do not clear them as a shortcut.

## Existing legacy routine: explicit migration

Only where the live `update-routine` schema advertises the fields and the read advertises support:

1. Show the exact routine, brand, accounts, cadence and current review rule. Explain: "Future runs will follow your brand and routine controls instead of the legacy writer setting. If those controls allow it, Bolta may schedule and publish without asking about each post. Existing drafts are not approved. This change is one-way; you can still tighten the brand or routine controls. Switch this routine to that model?"
2. Wait for a separate yes from the owner/admin. An API key is still limited by its creator's current role and scope. A request to update the brief, or permission to publish one post, is not this confirmation.
3. Call `update-routine` with only its identifiers and `autonomy_policy_version: "owner_v1"`, `acknowledge_autonomy_migration: true`, `expected_updated_at` copied exactly from the reviewed read. Do not bundle removal of a review requirement. Do not use a wildcard. Create and planner calls are not migration routes.
4. On a stale-configuration refusal, reread, show what changed and obtain confirmation again. Never silently replace the revision and retry under the old yes.
5. Read back the version and effective policy. Migration does not activate a routine, remove its explicit review setting, repair generation, approve old drafts or expand an in-flight run's authority. Never say "fully automated" from a successful update alone.

Setting a routine's review rule to Auto, changing its schedule or destinations, and switching it on each need the user's authorization for that scope. Preserve all unrelated settings. A manual trigger does not run weekly; the generation schedule is separate from publication times. Read `next_run_at` after activation. Credits, accounts, quality and successful publication still need separate evidence.

## Four posts on three networks

For four shared posts cross-posted to Facebook, LinkedIn and Bluesky, use one routine with `output_config` count 4, all three account bindings and the chosen voice. State in instructions that each of the four Post records must attach all three destinations, not twelve separate drafts or four posts divided between networks. Shared copy must fit the tightest network (Bluesky: 300 characters). Do not promise independently tailored copy from a shared-body setup.

Verify four saved Post records and each record's three account attachments. A successful generation run or a scheduled status is not publication evidence. Confirm the per-platform publication results when due; partial cross-post attachment or delivery is not success for all three.

## Client boundary

Clients share the server contract but may impose their own approvals. Do not promise identical host behavior. Bolta Auto does not turn off those checks. Direct approve/schedule/publish calls keep the post-level confirmation rules. Future Bolta-owned routine runs happen on the server and do not call the client's hooks. Client scheduled tasks remain draft/review-only. Never disable hooks to simulate automatic routines.

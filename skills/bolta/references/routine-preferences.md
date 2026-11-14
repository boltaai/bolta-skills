# Routine preferences without extra setup

## Minimal setup first

Use the goal to choose a template, then confirm the destination accounts, cadence/timezone and approval choice. Leave optional writing and platform preferences unset unless the user needs a specific constraint. A goal alone is not a runnable configuration: the template, required sources and account access still matter. Save a draft while inputs are missing.

After saving, read `get-routine` and explain its saved output count, distribution and approval. If it returns `execution_preview`, use that resolved view and its blockers; an unavailable preview is not verification. Do not repeat count, account or schedule rules in prose that conflicts with the structured settings. Clarify contradictions before activation.

## Optional writing approach

`output_config.writing_mode` is optional. Leave it absent on new routines unless explicitly requested, and preserve its current value on edits. Never opt an existing routine into planning merely because you changed its tone or schedule.

- `auto`: chooses style each run within the brief, voice and inherited agent guidance. Saved routine tone, editorial and storytelling style preferences are inactive, not erased. Source/topic/output boundaries, accounts, media and approval still apply.
- `custom`: applies saved style preferences and plans the unspecified aspects. It does not disable planning.
- Absent: preserves the existing writing path and saved preferences.

These controls do not guarantee better output or self-improvement. Facts must come from the permitted sources. Read back the configuration after an update; ask about conflicting count or schedule instructions rather than assuming the writer will resolve them.

## Optional platform preferences

`output_config.settings.platform_defaults` controls supported network-specific drafting preferences. Keep this optional during setup:

- Omitted: inherit the execution job's available preferences. Do not invent inherited values if `get-routine` cannot return them.
- `{"enabled":false}`: choose per draft instead of applying saved platform preferences. Retain the saved nested preferences when toggling this off so they can be restored.
- `{"enabled":true, ...}`: use explicitly requested, supported network settings. Boolean `false` is a real choice, not a missing value.

This is independent of writing mode and distribution, and never grants publishing permission. Read and preserve the whole saved `output_config` before changing one preference; use the server's validation errors for unsupported fields or incompatible media. Do not fill every network option merely to make the configuration look complete.

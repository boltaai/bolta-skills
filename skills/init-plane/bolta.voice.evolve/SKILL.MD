## bolta.voice.evolve

Purpose:
Refine Voice Profile based on engagement signals.

When Used:
- Periodic optimization
- Performance-driven voice refinement
- Enterprise or Autopilot optimization mode

Inputs:
- engagement_data (views, clicks, saves, replies, etc.)
- post_samples[]
- existing_voice_profile

Behavior:
- Detect high-performing tone patterns
- Identify structural correlations with engagement
- Adjust vocabulary emphasis
- Propose voice refinements
- Version voice profile with change log

Outputs:
- updated_voice_profile
- change_log
- performance_delta_estimate

Notes:
This skill should require elevated permissions
and may be gated to higher autonomy levels.

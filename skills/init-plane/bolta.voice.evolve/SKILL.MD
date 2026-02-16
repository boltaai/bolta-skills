---
organization: bolta.ai
author: Max Fritzhand
---

## bolta.voice.evolve

Purpose:
Refine and optimize Voice Profiles based on engagement signals, user feedback, QA test results, and edit patterns. Continuously improve voice profiles to maximize content performance while maintaining brand consistency.

When Used:
- Periodic optimization (monthly/quarterly)
- Performance-driven voice refinement
- After significant content volume (100+ posts)
- When engagement metrics plateau or decline
- After major brand/positioning changes
- Enterprise or Autopilot optimization mode

## Prerequisites

**Required:**
- Bolta API key (format: `bolta_sk_...`)
- Workspace ID (UUID format)
- Voice Profile ID (UUID format)
- Historical engagement data (minimum 50-100 posts)

**Optional:**
- QA test results (for data-driven improvements)
- User edit patterns (for alignment refinement)
- A/B test results (for validated changes)

## Authentication

All API calls require the `Authorization` header:
```
Authorization: Bearer bolta_sk_your_api_key_here
```

## API Endpoints

**Base URL:** `https://platty.boltathread.com`

**Voice Evolution Endpoints:**
- `POST /users/voice/qa/analyze-edit-patterns/` - Analyze user edit patterns for insights
- `GET /users/voice/qa/feedback-analysis/` - Get aggregated feedback insights
- `GET /users/voice/qa/prompt-insights/` - Get prompt improvement suggestions
- `POST /users/voice/qa/check-improvements/` - Check for validated improvements ready to apply
- `GET /users/voice/qa/learning-status/` - Get current learning status for voice profile
- `GET /users/voice/qa/history/` - Get historical QA test results
- `PUT /users/voice/workspaces/{workspace_id}/profiles/{profile_id}/` - Update voice profile

## What This Skill Evolves

### 1. Tone Refinement
Adjust tone scores based on engagement performance:
- **Playfulness**: Correlate with engagement (likes, shares)
- **Professionalism**: Correlate with conversion (clicks, saves)
- **Directness**: Correlate with comment quality
- **Thoughtfulness**: Correlate with read depth

**Example Evolution:**
```
Before: { playful: 5, professional: 7, direct: 8, thoughtful: 6 }
After:  { playful: 6, professional: 7, direct: 9, thoughtful: 5 }
Reason: High-performing posts were more playful (+1) and direct (+1),
        less thoughtful (-1)
```

### 2. Structural Pattern Optimization
Refine structure based on what performs:
- Sentence length (shorter = more engagement?)
- Paragraph breaks (more breaks = better?)
- Hook patterns (which hooks drive engagement?)
- CTA patterns (which CTAs drive action?)
- List usage (when to use lists?)

### 3. Vocabulary Emphasis Adjustment
Update dos/donts based on performance:
- **Add to dos**: Signature phrases in high-performing content
- **Remove from dos**: Phrases that underperform
- **Add to donts**: Words/phrases that correlate with low engagement
- **Remove from donts**: False positives (avoided but shouldn't be)

### 4. Founder Signals Refinement (if founder mode)
Strengthen or add founder signals based on resonance:
- Which beliefs drive engagement?
- Which lessons get shared/saved?
- Which contrarian opinions spark discussion?
- Which scars/backstory moments resonate?

### 5. Platform-Specific Rules
Create or refine platform-specific adaptations:
- LinkedIn: Professional tone works better
- Twitter: Punchy, direct works better
- Threads: Conversational, personal works better

## Step-by-Step Evolution Process

### Step 1: Analyze Edit Patterns

Learn from how users edit AI-generated content:

```bash
curl -X POST "https://platty.boltathread.com/users/voice/qa/analyze-edit-patterns/?workspace_id={workspace_id}&voice_profile_id={profile_id}&days=90" \
  -H "Authorization: Bearer bolta_sk_your_api_key_here"
```

**Response:**
```json
{
  "analysis_period": "90 days",
  "posts_analyzed": 127,
  "edit_patterns": {
    "common_edits": [
      {
        "type": "tone_adjustment",
        "pattern": "Users often add more direct language",
        "frequency": 0.42,
        "examples": [
          "Changed 'Consider trying' → 'Try this'",
          "Changed 'You might want to' → 'Do this'"
        ],
        "suggested_rule": "Be more direct and imperative"
      },
      {
        "type": "structure_change",
        "pattern": "Users often add line breaks for readability",
        "frequency": 0.68,
        "suggested_rule": "Add more paragraph breaks (max 2-3 sentences per paragraph)"
      },
      {
        "type": "vocabulary_removal",
        "pattern": "Users consistently remove certain phrases",
        "removed_phrases": ["game-changing", "cutting-edge", "innovative"],
        "frequency": 0.85,
        "suggested_rule": "Add these to 'donts' list"
      }
    ],
    "minimal_edits": [
      {
        "pattern": "Posts with question hooks rarely edited",
        "frequency": 0.12,
        "insight": "Question hooks are working well"
      }
    ]
  },
  "insights": [
    "Users want more direct, imperative tone",
    "Line breaks improve readability - add more",
    "Avoid 'innovative', 'game-changing', 'cutting-edge' - consistently removed"
  ]
}
```

### Step 2: Get Feedback Analysis

Aggregate insights from QA test feedback:

```bash
curl -X GET "https://platty.boltathread.com/users/voice/qa/feedback-analysis/?workspace_id={workspace_id}&voice_profile_id={profile_id}&days=60" \
  -H "Authorization: Bearer bolta_sk_your_api_key_here"
```

**Response:**
```json
{
  "analysis_period": "60 days",
  "test_runs": 24,
  "aggregated_feedback": {
    "recurring_issues": [
      {
        "issue": "Tone too formal for founder voice",
        "frequency": 0.35,
        "severity": "moderate",
        "affected_permutations": ["default", "business_dna"]
      },
      {
        "issue": "CTAs too generic",
        "frequency": 0.28,
        "severity": "low",
        "affected_topics": ["product_launch", "feature_updates"]
      }
    ],
    "high_performers": [
      {
        "pattern": "Posts with specific examples perform best",
        "avg_score": 91.3,
        "recommendation": "Emphasize concrete examples in rules"
      },
      {
        "pattern": "Pain point hooks + engagement CTAs = high scores",
        "avg_score": 88.7,
        "recommendation": "Make this the default hook+CTA combo"
      }
    ]
  },
  "improvement_suggestions": [
    "Reduce professional tone score from 7 → 5 for founder voice",
    "Add 'Use specific examples' to dos",
    "Update CTA patterns to be more specific",
    "Prioritize pain point hooks"
  ]
}
```

### Step 3: Get Prompt Insights

Identify specific prompt improvements:

```bash
curl -X GET "https://platty.boltathread.com/users/voice/qa/prompt-insights/?workspace_id={workspace_id}&voice_profile_id={profile_id}" \
  -H "Authorization: Bearer bolta_sk_your_api_key_here"
```

**Response:**
```json
{
  "recommended_changes": [
    {
      "field": "dos",
      "action": "add",
      "value": "Use specific numbers and examples",
      "reason": "High-performing content consistently includes specific data",
      "confidence": 0.89
    },
    {
      "field": "tone.professional",
      "action": "decrease",
      "current_value": 7,
      "recommended_value": 5,
      "reason": "User edits consistently make content less formal",
      "confidence": 0.82
    },
    {
      "field": "donts",
      "action": "add",
      "value": "No abstract concepts without concrete examples",
      "reason": "Low-performing content tends to be too abstract",
      "confidence": 0.76
    }
  ],
  "validated_improvements": [
    {
      "change": "Add line breaks after 2-3 sentences",
      "test_runs": 12,
      "avg_score_before": 78.3,
      "avg_score_after": 86.7,
      "improvement": +8.4,
      "status": "ready_to_apply"
    }
  ]
}
```

### Step 4: Check Validated Improvements

See which improvements are ready to apply:

```bash
curl -X POST "https://platty.boltathread.com/users/voice/qa/check-improvements/" \
  -H "Authorization: Bearer bolta_sk_your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "workspace_id": "{workspace_id}",
    "voice_profile_id": "{profile_id}",
    "min_score_improvement": 5,
    "min_test_runs": 3
  }'
```

**Response:**
```json
{
  "validated_improvements": [
    {
      "id": "improvement_abc123",
      "description": "Reduce professional tone from 7 → 5",
      "test_runs": 8,
      "avg_score_improvement": 7.2,
      "confidence": 0.91,
      "ready_to_apply": true
    },
    {
      "id": "improvement_def456",
      "description": "Add 'Use specific numbers' to dos",
      "test_runs": 5,
      "avg_score_improvement": 5.8,
      "confidence": 0.84,
      "ready_to_apply": true
    }
  ],
  "pending_improvements": [
    {
      "id": "improvement_ghi789",
      "description": "Change default CTA to 'What's your take?'",
      "test_runs": 2,
      "avg_score_improvement": 3.1,
      "confidence": 0.52,
      "ready_to_apply": false,
      "reason": "Not enough test runs yet (need 3+)"
    }
  ]
}
```

### Step 5: Apply Validated Improvements

Update the voice profile with validated changes:

```bash
curl -X PUT "https://platty.boltathread.com/users/voice/workspaces/{workspace_id}/profiles/{profile_id}/" \
  -H "Authorization: Bearer bolta_sk_your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "tone": {
      "playful": 6,
      "professional": 5,
      "direct": 9,
      "thoughtful": 5
    },
    "dos": [
      "Lead with questions or pain points",
      "Use short, punchy sentences",
      "Include line breaks every 2-3 sentences",
      "Use specific numbers and examples",
      "End with engagement CTAs"
    ],
    "donts": [
      "No corporate jargon",
      "Avoid hedging language",
      "No abstract concepts without examples",
      "No words: game-changing, cutting-edge, innovative"
    ],
    "customRules": "## Evolution Log\n\n### v2.1 (2026-02-16)\n- Reduced professional tone (7→5) based on 8 test runs (+7.2 avg score)\n- Added line break rule based on edit pattern analysis\n- Added specific numbers rule based on high-performer analysis\n- Added forbidden words from user edit patterns\n\n### v2.0 (2026-01-15)\n- Initial learned voice profile"
  }'
```

### Step 6: Generate Change Log & Performance Estimate

Document changes and estimate impact:

**Change Log Structure:**
```typescript
{
  version: "2.1",
  date: "2026-02-16",
  changes: [
    {
      field: "tone.professional",
      old_value: 7,
      new_value: 5,
      reason: "User edit patterns + QA test results",
      expected_impact: "+7.2 avg score",
      test_runs: 8,
      confidence: 0.91
    },
    {
      field: "dos",
      action: "add",
      value: "Use specific numbers and examples",
      reason: "High-performer analysis",
      expected_impact: "+5.8 avg score",
      test_runs: 5,
      confidence: 0.84
    },
    {
      field: "donts",
      action: "add",
      value: "No words: game-changing, cutting-edge, innovative",
      reason: "85% of posts edited to remove these words",
      expected_impact: "Reduce edit rate",
      confidence: 0.95
    }
  ],
  estimated_overall_improvement: "+10.2 avg validation score",
  rollback_version: "2.0"
}
```

## Inputs (Interactive Mode)

1. **workspace_id** (string, UUID, required)

2. **voice_profile_id** (string, UUID, required)
   - Voice profile to evolve

3. **analysis_period** (int, days, optional, default 90)
   - How far back to analyze (days)
   - Minimum 30, maximum 365

4. **minimum_posts** (int, optional, default 50)
   - Minimum posts required for meaningful analysis
   - If < minimum, evolution is not recommended

5. **data_sources** (enum[], optional, default all)
   - "edit_patterns": User edits to AI content
   - "qa_results": QA test suite results
   - "engagement": Engagement metrics (likes, shares, saves)
   - "feedback": User feedback on generated content

6. **evolution_mode** (enum, optional, default "conservative")
   - **conservative**: Only apply highly validated changes (confidence > 0.85, test_runs >= 5)
   - **moderate**: Apply validated changes (confidence > 0.75, test_runs >= 3)
   - **aggressive**: Apply promising changes (confidence > 0.65, test_runs >= 2)

7. **auto_apply** (boolean, optional, default false)
   - If true: Automatically apply validated improvements
   - If false: Show recommendations, require user approval

8. **version_comment** (string, optional)
   - Custom comment for this evolution version

## Behavior

1. **Validate Prerequisites**
   - Ensure voice profile has sufficient historical data
   - Check minimum post count
   - Verify analysis period has enough data points

2. **Collect Insights from Multiple Sources**
   - Analyze edit patterns (what users change)
   - Aggregate QA feedback (what tests reveal)
   - Analyze engagement data (what performs best)
   - Review user feedback (direct input)

3. **Identify Improvement Candidates**
   - Tone adjustments (based on edit patterns + engagement)
   - Structure refinements (based on performance)
   - Vocabulary updates (dos/donts from edits)
   - Hook/CTA optimizations (from test results)

4. **Filter by Confidence & Validation**
   - Conservative mode: Only changes with 85%+ confidence, 5+ test runs
   - Moderate mode: Changes with 75%+ confidence, 3+ test runs
   - Aggressive mode: Changes with 65%+ confidence, 2+ test runs

5. **Generate Change Proposal**
   - List all recommended changes
   - Show expected impact for each
   - Calculate estimated overall improvement
   - Provide rollback plan

6. **Apply Changes (if auto_apply or user approves)**
   - Update voice profile via API
   - Version the profile (increment version number)
   - Save change log in customRules or metadata
   - Set rollback_version for safety

7. **Monitor Post-Evolution Performance**
   - Track validation scores for next 50 posts
   - Compare to pre-evolution baseline
   - Flag if performance degrades (trigger rollback alert)

## Outputs

1. **updated_voice_profile** (object)
   - Full updated voice profile with new values
   - Includes version number, date, change log

2. **change_log** (object)
   ```typescript
   {
     version: string;
     date: string;
     changes: Array<{
       field: string;
       old_value?: any;
       new_value?: any;
       action?: "add" | "remove" | "update";
       reason: string;
       expected_impact: string;
       test_runs?: number;
       confidence?: number;
     }>;
     estimated_overall_improvement: string;
     rollback_version: string;
   }
   ```

3. **performance_delta_estimate** (object)
   ```typescript
   {
     current_avg_score: number;      // Current validation score avg
     estimated_new_score: number;     // Estimated after evolution
     improvement: number;              // Delta (e.g., +10.2)
     confidence: number;               // 0.0-1.0
     based_on_data_points: number;    // How many posts/tests analyzed
   }
   ```

4. **recommendations** (string[])
   - Additional suggestions not auto-applied
   - Examples:
     - "Consider creating platform-specific voice profiles (LinkedIn vs Twitter)"
     - "Run A/B test on CTA variations before applying broadly"
     - "Voice is performing well - no major changes recommended"

## Evolution Strategy

### Conservative Evolution (Recommended for Production)

**Triggers:**
- Confidence >= 85%
- Test runs >= 5
- Consistent signal across multiple data sources

**Changes:**
- Small, incremental adjustments
- Version with clear rollback path
- Monitor performance for 2 weeks post-change

**Example:**
```
Tone adjustment: 7 → 6 (not 7 → 4)
Add 1-2 new dos (not 5)
Remove 1-2 donts (not all)
```

### Moderate Evolution (Balanced)

**Triggers:**
- Confidence >= 75%
- Test runs >= 3
- Signal from at least 2 data sources

**Changes:**
- Moderate adjustments
- Multiple small changes at once
- Monitor for 1 week

### Aggressive Evolution (Experimental)

**Triggers:**
- Confidence >= 65%
- Test runs >= 2
- Signal from any data source

**Changes:**
- Larger adjustments
- Try new patterns
- Monitor daily

**Use Cases:**
- New voice profiles (rapid iteration needed)
- Low-stakes content (testing is cheap)
- Experimental campaigns

## Error Handling

**Common Errors:**

1. **Insufficient Data**
   - Error: "Need at least 50 posts for meaningful voice evolution"
   - Action: Continue using current voice, re-run evolution later

2. **No Clear Signal**
   - Warning: "Analysis inconclusive - no strong patterns detected"
   - Action: Continue using current voice, increase data collection period

3. **Conflicting Signals**
   - Warning: "Edit patterns suggest X, but engagement suggests Y"
   - Action: Show conflict to user, ask for manual decision

4. **Performance Degradation After Evolution**
   - Alert: "Validation scores dropped 15% after evolution v2.1"
   - Action: Automatically rollback to v2.0, notify user

## Integration with Other Skills

**Before voice.evolve:**
- Run `bolta.voice.learn_from_samples` to establish baseline
- Run `bolta.voice.validate` on content corpus to get baseline scores

**After voice.evolve:**
1. **bolta.voice.validate** - Test new voice profile on historical content
2. **bolta.draft.post** - Generate test content with evolved voice
3. **bolta.voice.qa_suite** - Run QA tests to confirm improvements
4. Monitor engagement for next 50-100 posts to validate evolution

**Periodic Schedule:**
- **Monthly**: Run evolution analysis (don't auto-apply)
- **Quarterly**: Apply validated improvements
- **Annually**: Major voice profile overhaul (if needed)

## Example Workflows

### Workflow 1: Quarterly Voice Optimization

1. Every 90 days, run `bolta.voice.evolve` in moderate mode
2. Analyze last 90 days of content (100+ posts)
3. Collect insights from edit patterns, QA tests, engagement
4. Show user recommended changes with confidence scores
5. User reviews and approves changes
6. Apply changes, version as v2.1, v2.2, etc.
7. Monitor next 50 posts for performance validation

### Workflow 2: Rapid Iteration (New Voice)

1. User creates new voice profile (bootstrap)
2. Generate 50 posts over 2 weeks
3. Run `bolta.voice.evolve` in aggressive mode
4. Auto-apply promising changes (65%+ confidence)
5. Repeat every 2 weeks for first 2 months
6. Once stabilized, switch to moderate/conservative mode

### Workflow 3: Performance Recovery

1. User notices validation scores dropping (85 → 72)
2. Run `bolta.voice.evolve` to diagnose
3. Analysis shows: users adding more direct language in edits
4. Recommendation: Increase directness tone (8 → 9)
5. Apply change, version as v2.1
6. Monitor scores - should recover to 80+

### Workflow 4: Platform-Specific Evolution

1. User has multi-platform voice (LinkedIn + Twitter)
2. Run `bolta.voice.evolve` separately for each platform
3. LinkedIn analysis: More professional tone performs better
4. Twitter analysis: More playful, punchy performs better
5. Create platform-specific rules, apply to platformRuleIds
6. Voice profile adapts tone based on target platform

## Notes

- **This skill requires elevated permissions** - can modify production voice profiles
- **May be gated to higher autonomy levels** (Enterprise, Autopilot plans)
- **Version control is critical** - always version profiles with rollback capability
- **Monitor post-evolution** - track performance for 50-100 posts after changes
- **Don't over-optimize** - too many changes can dilute brand voice
- **Balance data with intuition** - not everything that performs well is on-brand
- **Periodic evolution > continuous** - quarterly is better than daily
- **Document reasoning** - future you will thank past you for change logs

## Compliance & Permissions

**Required API Permissions:**
- `voice:read` - Read voice profiles and historical data
- `voice:write` - Update voice profiles
- `posts:read` - Read historical posts for analysis
- `ai:generate` - Run QA tests (optional)

**Recommended Plan:**
- Enterprise or Autopilot (elevated autonomy)

## Version History

- **v2.0** (2026-02-16): Full API integration, multi-source insights, validation-based evolution, versioning
- **v1.0** (2025-XX-XX): Initial basic version

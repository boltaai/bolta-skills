---
organization: bolta.ai
author: Max Fritzhand
---

## bolta.voice.validate

Purpose:
Evaluate content against a Voice Profile to ensure brand consistency, style alignment, and quality standards. Provides compliance scoring, deviation reports, and optional rewrite suggestions.

When Used:
- Before submitting content for review
- Before scheduling posts
- During Autopilot execution
- During review workflows
- QA testing voice profile quality
- Validating generated vs human content

## Prerequisites

**Required:**
- Bolta API key (format: `bolta_sk_...`)
- Workspace ID (UUID format)
- Voice Profile ID (UUID format)
- Content to validate (text string)

**Optional:**
- Account ID (for account-specific voice validation)
- Platform (for platform-specific rules)

## Authentication

All API calls require the `Authorization` header:
```
Authorization: Bearer bolta_sk_your_api_key_here
```

## API Endpoints

**Base URL:** `https://platty.boltathread.com`

**Voice Validation Endpoints:**
- `POST /users/voice/verify/authenticity/` - Validate content authenticity and voice alignment
- `GET /users/voice/workspaces/{workspace_id}/accounts/{account_id}/context/` - Get voice context for validation
- `POST /users/voice/qa/run-suite/` - Run full QA test suite
- `POST /users/voice/qa/run-permutation/` - Run single permutation test
- `GET /users/voice/qa/results/{suite_id}/` - Get QA test results

## What This Skill Validates

### 1. Tone Alignment
Compares content tone against voice profile:
- **Playfulness** (0-10 scale)
- **Professionalism** (0-10 scale)
- **Directness** (0-10 scale)
- **Thoughtfulness** (0-10 scale)

**Scoring:**
- Exact match (±0.5): 100 points
- Close match (±1.0): 85 points
- Moderate deviation (±2.0): 70 points
- High deviation (>2.0): <50 points

### 2. Structure Rules Compliance
Validates content structure against voice profile rules:
- Sentence length (avg, min, max)
- Paragraph density
- Use of line breaks
- Hook pattern adherence
- CTA pattern adherence
- List/bullet usage

### 3. Vocabulary Drift Detection
Flags deviations from signature vocabulary:
- **Red flags**: Uses forbidden words from `donts`
- **Green flags**: Uses signature phrases from `dos`
- **Neutral**: New vocabulary not in either list

**Scoring:**
- No red flags + 5+ green flags: 100 points
- No red flags + 2-4 green flags: 85 points
- 1-2 red flags: 60 points
- 3+ red flags: <40 points

### 4. Hook and CTA Consistency
Validates opening and closing patterns:
- Hook type matches profile patterns (question, pain point, stat, story, contrarian)
- CTA type matches profile patterns (engagement, direct, soft, link, none)

### 5. Content Size Compliance
Validates length against `contentSize` setting:
- **short**: 50-150 chars (Twitter/X standard)
- **standard**: 150-500 chars (LinkedIn, Threads)
- **long**: 500-1500 chars (LinkedIn article, blog excerpt)

### 6. Founder Signals Authenticity (if founder mode)
For founder voice profiles, validate that content resonates with founder signals:
- **Belief Alignment**: Does content reflect stated beliefs?
- **Lesson Integration**: Are learned lessons woven into advice given?
- **Contrarian Signal**: Do contrarian opinions appear in content?
- **Scar Relevance**: Are scars referenced to prove hard-won wisdom?
- **Backstory Coherence**: Does content align with founder's narrative?

**Scoring:**
- Strong alignment (post demonstrates 3+ signals authentically): 95-100
- Good alignment (post demonstrates 2 signals): 85-94
- Moderate alignment (post demonstrates 1 signal or generic): 70-84
- Weak alignment (post contradicts signals or generic): <70

**Example:**
```
Founder Signals: [belief: "Ship fast beats planning", lesson: "Users teach you more than docs"]
Content: "Before writing code, ask: did users ask? Will it move metrics? Can we ship <1 week?"
Analysis:
- Uses "ship fast" belief explicitly ✓
- Implies "user validation" from lessons ✓
- Demonstrates conviction without hedging ✓
- Score: 94 (strong signal alignment)
```

### 7. Authenticity Check (Anti-AI Detection)
Optional: Check if content sounds human vs AI-generated
- Detects common AI patterns
- Flags overly polished language
- Identifies lack of personality
- For founder mode: checks if signals feel authentic (not generic founder platitudes)

## Step-by-Step Validation Process

### Step 1: Verify Content Authenticity

```bash
curl -X POST "https://platty.boltathread.com/users/voice/verify/authenticity/" \
  -H "Authorization: Bearer bolta_sk_your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Most founders waste months building features no one asked for. Here'\''s the 3-question framework I use before writing a single line of code: 1) Did a user explicitly request this? 2) Will it move our core metric? 3) Can we ship it in <1 week? If any answer is no, it goes in the backlog. Thoughts?",
    "workspace_id": "{workspace_id}",
    "account_id": "{account_id}",
    "check_humanize": true,
    "check_plagiarism": false
  }'
```

**Parameters:**
- `content` (string, required): Content to validate
- `workspace_id` (string, UUID, required): Workspace ID
- `account_id` (string, UUID, optional): Account ID for voice context
- `check_humanize` (bool, optional, default true): Check if content sounds AI-generated
- `check_plagiarism` (bool, optional, default false): Check for duplicate content

**Response:**
```json
{
  "success": true,
  "compliance_score": 87,
  "tone_alignment": {
    "playful": { "profile": 3, "content": 2, "deviation": -1, "score": 90 },
    "professional": { "profile": 7, "content": 8, "deviation": +1, "score": 85 },
    "direct": { "profile": 9, "content": 9, "deviation": 0, "score": 100 },
    "thoughtful": { "profile": 6, "content": 7, "deviation": +1, "score": 85 }
  },
  "structure_compliance": {
    "sentence_length": { "avg": 11.2, "target": 12, "score": 95 },
    "paragraph_density": { "avg": 3.1, "target": 3, "score": 98 },
    "hook_type": "pain_point",
    "hook_matches_profile": true,
    "cta_type": "engagement",
    "cta_matches_profile": true
  },
  "vocabulary_analysis": {
    "green_flags": ["waste months", "ship it"],
    "red_flags": [],
    "signature_phrases_used": 2,
    "forbidden_words_used": 0,
    "score": 88
  },
  "authenticity": {
    "sounds_human": true,
    "ai_probability": 0.23,
    "confidence": 0.87,
    "notes": "Natural flow, personal voice, specific examples - passes authenticity check"
  },
  "founder_signals_alignment": {
    "mode": "founder",
    "signals_demonstrated": [
      {
        "type": "belief",
        "signal": "Ship fast beats planning",
        "found_in_content": true,
        "evidence": "Explicitly recommends shipping in <1 week",
        "score": 95
      },
      {
        "type": "lesson",
        "signal": "Users teach you more than docs",
        "found_in_content": true,
        "evidence": "Starts with 'did users ask?' validation",
        "score": 92
      }
    ],
    "signals_missing": [],
    "signal_authenticity_score": 93,
    "notes": "Strong founder voice - demonstrates beliefs and lessons authentically with specific examples"
  },
  "deviations": [],
  "overall_score": 87
}
```

### Step 2: Generate Deviation Report

If `compliance_score < 70`, generate a detailed deviation report:

**Deviation Report Structure:**
```typescript
{
  deviations: [
    {
      type: "tone",
      severity: "moderate",
      field: "professional",
      expected: 7,
      actual: 4,
      message: "Content is too casual for this voice profile (professional score: 4 vs expected 7)"
    },
    {
      type: "vocabulary",
      severity: "high",
      field: "forbidden_words",
      found: ["synergy", "leverage"],
      message: "Content uses 2 forbidden words: 'synergy', 'leverage'"
    },
    {
      type: "structure",
      severity: "low",
      field: "sentence_length",
      expected: 12,
      actual: 18,
      message: "Average sentence length is too long (18 words vs target 12)"
    }
  ],
  severity_breakdown: {
    high: 1,      // Critical issues - must fix
    moderate: 1,  // Should fix
    low: 1        // Nice to fix
  }
}
```

### Step 3: Generate Suggested Rewrite (Optional)

If `compliance_score < 70` AND user requests it:

```typescript
{
  suggested_rewrite: "Most founders waste months on features nobody asked for. Before writing any code, I ask: Did a user request this? Will it move our core metric? Can we ship in under a week? If any answer is no → backlog. What's your filter?",
  changes_made: [
    "Shortened sentences for directness",
    "Removed 'Here's the' (hedging language)",
    "Changed 'Thoughts?' to 'What's your filter?' (more specific CTA)",
    "Simplified numbered list to flow text"
  ],
  new_compliance_score: 92
}
```

## Inputs (Interactive Mode)

1. **workspace_id** (string, UUID, required)

2. **voice_profile_id** (string, UUID, required)
   - Voice profile to validate against

3. **content_text** (string, required)
   - Content to validate
   - Can be single post or multiple paragraphs

4. **account_id** (string, UUID, optional)
   - If provided, uses account-specific voice assignment
   - If omitted, uses workspace default voice profile

5. **platform** (enum: "twitter" | "linkedin" | "threads" | "facebook" | "instagram", optional)
   - Platform-specific validation rules
   - Affects character limits, structure expectations

6. **validation_mode** (enum: "strict" | "standard" | "lenient", optional, default "standard")
   - **strict**: Score < 80 = fail
   - **standard**: Score < 70 = fail
   - **lenient**: Score < 60 = fail

7. **suggest_rewrite** (boolean, optional, default false)
   - If true AND score < threshold: generate rewrite suggestion

8. **check_authenticity** (boolean, optional, default true)
   - Run AI detection / humanization check

## Behavior

1. **Fetch Voice Profile**
   - GET voice profile from `/api/v1/workspaces/{workspace_id}/voice/profiles/{profile_id}`
   - Extract tone, dos, donts, customRules, styleKeywords

2. **Analyze Content**
   - Parse content structure (sentences, paragraphs, hooks, CTAs)
   - Extract tone signals (vocabulary, punctuation, complexity)
   - Identify vocabulary usage (signature phrases, forbidden words)

3. **Score Against Profile**
   - Tone alignment (40% of score)
   - Vocabulary compliance (30% of score)
   - Structure rules (20% of score)
   - Content size (10% of score)

4. **Generate Deviation Report**
   - List all deviations with severity
   - Categorize by type (tone, vocabulary, structure)
   - Provide actionable fix suggestions

5. **Optional: Generate Rewrite**
   - If requested AND score < threshold
   - Rewrite to align with voice profile
   - Show specific changes made

6. **Return Results**
   - Compliance score (0-100)
   - Deviation report
   - Optional rewrite suggestion

## Outputs

1. **compliance_score** (number, 0-100)
   - Overall voice alignment score
   - < 60: Poor alignment, significant issues
   - 60-79: Moderate alignment, needs improvement
   - 80-89: Good alignment, minor issues
   - 90+: Excellent alignment, production-ready

2. **deviation_report** (object)
   ```typescript
   {
     deviations: Array<{
       type: "tone" | "vocabulary" | "structure" | "size";
       severity: "high" | "moderate" | "low";
       field: string;
       expected?: any;
       actual?: any;
       found?: string[];
       message: string;
     }>;
     severity_breakdown: {
       high: number;
       moderate: number;
       low: number;
     };
   }
   ```

3. **suggested_rewrite** (string, optional, conditional)
   - Only if `suggest_rewrite = true` AND `compliance_score < threshold`
   - Rewritten content that aligns with voice profile
   - Shows specific changes made

4. **tone_alignment** (object)
   ```typescript
   {
     playful: { profile: number; content: number; deviation: number; score: number };
     professional: { profile: number; content: number; deviation: number; score: number };
     direct: { profile: number; content: number; deviation: number; score: number };
     thoughtful: { profile: number; content: number; deviation: number; score: number };
   }
   ```

5. **vocabulary_analysis** (object)
   ```typescript
   {
     green_flags: string[];          // Signature phrases used
     red_flags: string[];            // Forbidden words used
     signature_phrases_used: number;
     forbidden_words_used: number;
     score: number;
   }
   ```

6. **authenticity_check** (object, optional)
   ```typescript
   {
     sounds_human: boolean;
     ai_probability: number;  // 0.0-1.0
     confidence: number;      // 0.0-1.0
     notes: string;
   }
   ```

7. **founder_signals_alignment** (object, conditional - if founder mode)
   ```typescript
   {
     mode: "founder";
     signals_demonstrated: Array<{
       type: "belief" | "lesson" | "contrarian" | "scar" | "backstory";
       signal: string;
       found_in_content: boolean;
       evidence?: string;
       score: number;  // 0-100
     }>;
     signals_missing: Array<{
       type: string;
       signal: string;
       explanation: string;
     }>;
     signal_authenticity_score: number;  // 0-100
     notes: string;
   }
   ```

8. **pass_fail** (boolean)
   - Based on validation_mode threshold
   - true = passes, false = fails

## Scoring Algorithm

**Overall Compliance Score Formula:**

```
compliance_score = (
  tone_alignment_score * 0.40 +
  vocabulary_score * 0.30 +
  structure_score * 0.20 +
  size_compliance_score * 0.10
)
```

**Tone Alignment Score:**
```
tone_score = average([
  playful_match_score,
  professional_match_score,
  direct_match_score,
  thoughtful_match_score
])

// Each dimension scored as:
match_score = max(0, 100 - (abs(deviation) * 25))
```

**Vocabulary Score:**
```
vocabulary_score = (
  (green_flags_count * 10) +           // +10 per signature phrase
  (red_flags_count * -25) +            // -25 per forbidden word
  50                                   // Baseline
)
// Clamped to 0-100
```

**Structure Score:**
```
structure_score = average([
  sentence_length_score,
  paragraph_density_score,
  hook_match_score,
  cta_match_score
])
```

## Error Handling

**Common Errors:**

1. **404 - Voice Profile Not Found**
   - Message: "Voice profile {profile_id} not found in workspace {workspace_id}"
   - Action: Verify profile_id exists

2. **400 - Invalid Content**
   - Message: "Content must be at least 10 characters"
   - Action: Provide valid content

3. **400 - Missing Required Fields**
   - Message: "Missing required field: workspace_id, voice_profile_id, or content"
   - Action: Ensure all required fields provided

4. **500 - Analysis Failed**
   - Message: "Voice validation failed due to internal error"
   - Action: Retry with simpler content

## Advanced: QA Test Suites

Run comprehensive QA tests across multiple permutations:

**Run Full QA Suite:**

```bash
curl -X POST "https://platty.boltathread.com/users/voice/qa/run-suite/" \
  -H "Authorization: Bearer bolta_sk_your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "workspace_id": "{workspace_id}",
    "voice_profile_id": "{profile_id}",
    "account_id": "{account_id}",
    "platform": "threads",
    "test_topics": ["product_launch", "founder_lessons", "tactical_advice"],
    "permutations": [
      "default",
      "business_dna",
      "platform_rules",
      "business_dna+platform_rules"
    ]
  }'
```

**Response:**
```json
{
  "suite_id": "qa_suite_abc123",
  "status": "running",
  "permutations_tested": 4,
  "topics_per_permutation": 3,
  "total_tests": 12,
  "estimated_completion": "2026-02-16T11:05:00Z"
}
```

**Get QA Results:**

```bash
curl -X GET "https://platty.boltathread.com/users/voice/qa/results/qa_suite_abc123/?workspace_id={workspace_id}" \
  -H "Authorization: Bearer bolta_sk_your_api_key_here"
```

**Response:**
```json
{
  "suite_id": "qa_suite_abc123",
  "status": "completed",
  "overall_score": 84.2,
  "results": [
    {
      "permutation": "default",
      "topic": "product_launch",
      "content_generated": "We just shipped multi-workspace support...",
      "compliance_score": 87,
      "deviations": [],
      "feedback": "Good alignment - direct tone, clear value prop"
    }
  ],
  "insights": {
    "best_permutation": "business_dna+platform_rules",
    "avg_score_by_permutation": {
      "default": 81.3,
      "business_dna": 84.7,
      "platform_rules": 83.2,
      "business_dna+platform_rules": 88.1
    },
    "common_issues": [
      "Tone slightly more playful than target on 2 tests",
      "CTA patterns need refinement for founder_lessons topic"
    ]
  }
}
```

## Integration with Other Skills

**Before validate:**
- Run `bolta.voice.bootstrap` or `bolta.voice.learn_from_samples` to create voice profile

**After validate:**
1. **If score >= 80: Approve content**
   - Ready for scheduling or publishing
   - Run `bolta.schedule.post` or `bolta.publish.now`

2. **If score 70-79: Review & refine**
   - Show deviation report to user
   - Use `bolta.rewrite.improve` with suggested changes

3. **If score < 70: Reject or rewrite**
   - Auto-rewrite with `bolta.rewrite.voice_align`
   - Or show user deviation report for manual fix

4. **For ongoing QA: bolta.voice.evolve**
   - Track validation scores over time
   - Identify voice drift
   - Trigger re-training when needed

## Example Workflows

### Workflow 1: Pre-Publish Validation

1. User drafts post in composer
2. Before scheduling, run `bolta.voice.validate`
3. Score = 92 → Auto-approve, schedule
4. Score = 75 → Show deviations, ask user to review
5. Score = 58 → Auto-rewrite, re-validate
6. If re-validation score > 80 → Approve

### Workflow 2: Autopilot QA Gate

1. Autopilot generates 10 posts for review queue
2. For each post, run `bolta.voice.validate`
3. Score >= 85 → Move to "Ready to Publish"
4. Score 70-84 → Move to "Needs Review"
5. Score < 70 → Move to "Rejected" or auto-rewrite

### Workflow 3: Voice Profile QA Testing

1. User creates new voice profile
2. Run `bolta.voice.validate` on 20 historical posts
3. Calculate average compliance score
4. If avg < 75: Voice profile needs refinement
5. Run `bolta.voice.learn_from_samples` to improve
6. Re-validate until avg >= 80

### Workflow 4: A/B Test Voice Profiles

1. Create 2 voice profiles: "Direct Founder" vs "Professional Brand"
2. Generate 5 posts with each
3. Run `bolta.voice.validate` on all 10
4. Compare compliance scores
5. Also compare engagement metrics after publishing
6. Choose winner based on combined score

## Notes

- **This skill does NOT modify content automatically** unless `suggest_rewrite = true` is explicitly requested
- **Compliance layer**: Provides quality gate for content workflows
- **Non-blocking**: Can be informational (show score) or blocking (reject if < threshold)
- **Versioning**: Track validation scores over time to detect voice drift
- **Platform-specific**: Consider different thresholds for different platforms
- **Human override**: Always allow manual approval even if score < threshold
- **False positives**: Some creative content may score low but be intentionally off-brand
- This skill provides a compliance layer and does not modify content automatically unless explicitly requested

## Compliance & Permissions

**Required API Permissions:**
- `voice:read` - Read voice profile for validation
- `posts:read` - Read content to validate (optional)

**Optional Permissions:**
- `ai:generate` - Generate rewrite suggestions

## Version History

- **v2.0** (2026-02-16): Full API integration, QA test suites, authenticity checks, deviation reporting
- **v1.0** (2025-XX-XX): Initial basic version

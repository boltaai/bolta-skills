---
organization: bolta.ai
author: Max Fritzhand
---

## bolta.voice.learn_from_samples

Purpose:
Extract structured voice rules from past content to refine or create a voice profile. Uses AI to analyze writing patterns, tone, structure, and style from existing posts, then either creates a new voice profile or updates an existing one.

When Used:
- Onboarding with existing content library
- Upgrading from bootstrap voice to data-driven voice
- Refining an existing voice profile based on approved content
- Migrating from another social media management tool
- Training voice profile from high-performing content

## Prerequisites

**Required:**
- Bolta API key (format: `bolta_sk_...`)
- Workspace ID (UUID format)
- Sample content (minimum 10-15 posts for meaningful analysis)

**Optional:**
- Existing voice profile ID (if refining rather than creating)
- Account ID (if analyzing from a specific social account)

## Authentication

All API calls require the `Authorization` header:
```
Authorization: Bearer bolta_sk_your_api_key_here
```

## API Endpoints

**Base URL:** `https://platty.boltathread.com`

**Voice Analysis Endpoints:**
- `POST /users/voice/workspaces/{workspace_id}/accounts/{account_id}/analyze/` - Analyze account voice from posts
- `POST /users/voice/workspaces/{workspace_id}/bulk-analyze/` - Analyze all workspace accounts
- `GET /users/voice/workspaces/{workspace_id}/accounts/{account_id}/context/` - Get voice context
- `POST /users/voice/workspaces/{workspace_id}/profiles/` - Create voice profile from analysis
- `PUT /users/voice/workspaces/{workspace_id}/profiles/{profile_id}/` - Update existing profile

## What This Skill Analyzes

### 1. Tone Detection (Automated)
- Playfulness score (0-10)
- Professionalism score (0-10)
- Directness score (0-10)
- Thoughtfulness score (0-10)

**Method:** Statistical analysis of:
- Sentence length variation
- Vocabulary complexity (Flesch-Kincaid)
- Punctuation patterns (exclamations, questions)
- Emoji usage frequency
- Personal pronouns vs passive voice

### 2. Sentence Structure Modeling
- Average sentence length
- Paragraph density
- Use of lists, bullets, line breaks
- Opening hook patterns
- Closing CTA patterns

### 3. Hook Pattern Extraction
Identifies common opening patterns:
- Question-based hooks ("Ever notice...")
- Pain point hooks ("Most founders struggle with...")
- Stat-based hooks ("73% of...")
- Story hooks ("Last week, I...")
- Contrarian hooks ("Everyone tells you to..., but...")

### 4. CTA Pattern Extraction
Identifies common closing patterns:
- Soft CTAs ("What do you think?", "Agree?")
- Direct CTAs ("Try this:", "Here's how:")
- Engagement CTAs ("Drop a comment", "Share your story")
- Link CTAs ("Read more:", "Check out:")
- No CTA (just value drop)

### 5. Vocabulary Frequency Modeling
- High-frequency words (signature phrases)
- Forbidden words (consistently avoided)
- Technical jargon level
- Industry-specific terminology
- Emoji patterns

### 6. Content Themes & Topics
- Common content themes
- Topic categories (tactical, strategic, personal)
- Pain points frequently addressed
- Value propositions emphasized

### 7. Founder Signals Extraction (If founder mode)
When analyzing content from a founder, extract:
- **Beliefs**: Core convictions about industry, strategy, product development
  - Example: "Most AI tools optimize for length, not clarity"
  - Example: "The best marketing is just solving real problems publicly"
- **Lessons**: Hard-won insights from building/failing
  - Example: "Shipping fast beats perfect planning"
  - Example: "Your first 100 users teach more than 100 strategy docs"
- **Contrarian Opinions**: Industry myths you push back on
  - Example: "Most 'thought leadership' is repackaged LinkedIn wisdom"
  - Example: "Engagement metrics are vanity. Pipeline metrics are sanity."
- **Scars**: Failures, mistakes, and what you learned
  - Example: "Built a feature no one asked for—wasted 3 months"
  - Example: "Hired for culture fit over skill—set team back 6 months"
- **Backstory Moments**: Experiences that shaped your thinking
  - Example: "Watched my first startup fail because we couldn't articulate our value"
  - Example: "Spent years ghostwriting for founders—saw the patterns that work"

## Step-by-Step Process

### Step 1: Analyze Account Content

**Option A: Analyze Specific Account**

```bash
curl -X POST "https://platty.boltathread.com/users/voice/workspaces/{workspace_id}/accounts/{account_id}/analyze/" \
  -H "Authorization: Bearer bolta_sk_your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "max_posts": 50,
    "days_back": 90,
    "force_refresh": false
  }'
```

**Parameters:**
- `max_posts` (int, default 50): Number of posts to analyze
- `days_back` (int, default 90): How far back to look
- `force_refresh` (bool, default false): Re-analyze even if cached

**Response:**
```json
{
  "status": "completed",
  "voice_analysis": {
    "tone_scores": {
      "playful": 4.2,
      "professional": 7.8,
      "direct": 8.5,
      "thoughtful": 6.3
    },
    "sentence_structure": {
      "avg_sentence_length": 12.4,
      "avg_paragraph_length": 3.2,
      "line_break_frequency": "high",
      "list_usage": "frequent"
    },
    "hook_patterns": [
      {
        "pattern": "question_hook",
        "frequency": 0.35,
        "examples": ["Ever notice...", "Why do..."]
      },
      {
        "pattern": "pain_point_hook",
        "frequency": 0.28,
        "examples": ["Most founders struggle with..."]
      }
    ],
    "cta_patterns": [
      {
        "pattern": "engagement_cta",
        "frequency": 0.42,
        "examples": ["What do you think?", "Agree?"]
      }
    ],
    "vocabulary": {
      "signature_phrases": ["ship fast", "real talk", "here's the thing"],
      "avoided_words": ["revolutionize", "synergy", "leverage"],
      "emoji_usage": "minimal"
    },
    "content_themes": [
      "product development",
      "startup lessons",
      "founder psychology"
    ]
  },
  "post_count": 48,
  "analysis_date": "2026-02-16T10:30:00Z"
}
```

**Option B: Bulk Analyze All Workspace Accounts**

```bash
curl -X POST "https://platty.boltathread.com/users/voice/workspaces/{workspace_id}/bulk-analyze/" \
  -H "Authorization: Bearer bolta_sk_your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "max_posts_per_account": 30,
    "days_back": 60
  }'
```

### Step 2: Review Analysis & Generate Voice Profile

**Interactive Workflow:**

1. **Show Analysis Summary**
   - Display tone scores
   - Show top 5 hook patterns
   - Show top 5 CTA patterns
   - Display signature phrases
   - List content themes

2. **Ask User for Refinements**
   - "Does this match your perception of your voice?"
   - "Any patterns you want to emphasize or avoid?"
   - "Should we add custom rules based on this analysis?"

3. **Construct Voice Profile Payload**

Combine automated analysis with user input. If founder mode, include founder_signals:

**Example: Brand Voice (learned from company content)**
```json
{
  "name": "Analyzed Voice Profile",
  "description": "Voice profile learned from 48 posts (Jan-Mar 2026)",
  "tone": {
    "playful": 4,
    "professional": 8,
    "direct": 9,
    "thoughtful": 6
  },
  "dos": [
    "Lead with questions or pain points",
    "Use short, punchy sentences (avg 12 words)",
    "Include line breaks for readability",
    "End with engagement CTAs ('What do you think?')",
    "Use lists and bullet points frequently"
  ],
  "donts": [
    "No corporate jargon ('synergy', 'leverage', 'revolutionize')",
    "Avoid long paragraphs (>4 sentences)",
    "No salesy language",
    "Minimal emoji usage"
  ],
  "customRules": "## Hook Patterns\n- 35% question hooks\n- 28% pain point hooks\n\n## Signature Phrases\n- \"ship fast\"\n- \"real talk\"\n- \"here's the thing\"\n\n## Content Themes\n- Product development\n- Startup lessons\n- Founder psychology",
  "styleKeywords": ["direct", "tactical", "founder-led", "honest"],
  "contentSize": "standard",
  "useEmojis": false,
  "language": "en",
  "speakerMode": "brand",
  "isDefault": true
}
```

**Example: Founder Voice (learned from founder's personal content)**
```json
{
  "name": "Max - Analyzed Founder Voice",
  "description": "Voice profile learned from 45 founder posts (Jan-Mar 2026)",
  "tone": {
    "playful": 3,
    "professional": 6,
    "direct": 10,
    "thoughtful": 7
  },
  "dos": [
    "Tell stories from the building experience",
    "Share specific failures and lessons",
    "Use concrete examples over abstractions",
    "Write like you're talking to another founder",
    "Lead with conviction, not hedging"
  ],
  "donts": [
    "No inspirational quotes without context",
    "Avoid humble-bragging",
    "Don't soften hard truths",
    "No theoretical advice—only battle-tested"
  ],
  "customRules": "## Hook Patterns (extracted from content)\n- 40% story hooks (sharing personal experience)\n- 35% lesson hooks (what I learned)\n- 25% contrarian hooks (pushback on industry norms)\n\n## Signature Phrases\n- \"real talk\"\n- \"here's what I learned\"\n- \"most founders think X, but actually Y\"",
  "speakerMode": "founder",
  "founderSignals": {
    "beliefs": [
      "Most AI content fails because it optimizes for length, not clarity",
      "The best marketing is just solving real problems publicly",
      "Brand voice isn't about tone—it's about what you refuse to say"
    ],
    "lessons": [
      "Shipping fast beats perfect planning every time",
      "Your first 100 users will teach you more than 100 strategy docs",
      "Technical debt is fine. Strategic debt will kill you"
    ],
    "contrarianOpinions": [
      "Most 'thought leadership' is just repackaged LinkedIn wisdom",
      "You don't need a content calendar—you need conviction",
      "Engagement metrics are vanity. Pipeline metrics are sanity."
    ],
    "scars": [
      "Built a feature no one asked for—wasted 3 months",
      "Hired for culture fit over skill—set team back 6 months",
      "Tried to be everything to everyone—diluted the product"
    ],
    "backstoryMoments": [
      "Watched my first startup fail because we couldn't articulate our value",
      "Realized most founders struggle with consistent voice at scale",
      "Spent years ghostwriting for founders—saw the patterns that work"
    ]
  },
  "styleKeywords": ["direct", "honest", "battle-tested", "founder-led"],
  "contentSize": "standard",
  "useEmojis": false,
  "language": "en",
  "isDefault": false
}
```

### Step 3: Create or Update Voice Profile

**Create New Profile:**

```bash
curl -X POST "https://platty.boltathread.com/users/voice/workspaces/{workspace_id}/profiles/" \
  -H "Authorization: Bearer bolta_sk_your_api_key_here" \
  -H "Content-Type: application/json" \
  -d @voice_profile_payload.json
```

**Update Existing Profile:**

```bash
curl -X PUT "https://platty.boltathread.com/users/voice/workspaces/{workspace_id}/profiles/{profile_id}/" \
  -H "Authorization: Bearer bolta_sk_your_api_key_here" \
  -H "Content-Type: application/json" \
  -d @voice_profile_update.json
```

### Step 4: Compare Against Existing Voice (If Updating)

If updating an existing voice profile, generate a **delta report**:

**Delta Report Structure:**
```typescript
{
  tone_changes: {
    playful: { old: 5, new: 4, change: -1 },
    professional: { old: 6, new: 8, change: +2 },
    direct: { old: 8, new: 9, change: +1 },
    thoughtful: { old: 7, new: 6, change: -1 }
  },
  new_dos: ["Include line breaks for readability"],
  removed_dos: [],
  new_donts: ["Minimal emoji usage"],
  removed_donts: [],
  signature_phrase_changes: {
    added: ["ship fast", "real talk"],
    removed: ["move fast and break things"]
  },
  confidence_improvement: +15  // % increase in voice consistency
}
```

## Inputs (Interactive Mode)

1. **workspace_id** (string, UUID, required)

2. **account_id** (string, UUID, optional)
   - If provided: analyze this specific account
   - If omitted: analyze all workspace accounts or use manual posts

3. **post_samples** (string[], optional)
   - Manually provided posts if not analyzing from account
   - Minimum 10-15 posts recommended

4. **max_posts** (int, optional, default 50)
   - How many posts to analyze from account

5. **days_back** (int, optional, default 90)
   - How far back to look for posts

6. **existing_voice_profile_id** (string, UUID, optional)
   - If provided: update this profile (shows delta report)
   - If omitted: create new profile

7. **refinement_mode** (enum: "auto" | "interactive", optional, default "interactive")
   - "auto": Generate voice profile automatically from analysis
   - "interactive": Show analysis, ask user for refinements

8. **custom_overrides** (object, optional)
   - User-provided overrides to automated analysis
   - Example: force certain dos/donts, adjust tone scores

## Behavior

1. **Fetch Content**
   - If account_id provided: fetch posts via API
   - If post_samples provided: use manual samples
   - Filter out retweets, replies (focus on original content)

2. **Run Voice Analysis**
   - Tone detection (statistical + NLP)
   - Sentence structure modeling
   - Hook/CTA pattern extraction
   - Vocabulary frequency analysis
   - Content theme clustering

3. **Extract Founder Signals (if applicable)**
   - Scan content for beliefs, lessons, contrarian opinions, scars, backstory moments
   - Extract direct quotes or paraphrased signals
   - Group by category
   - Filter for authenticity (real, verifiable experiences vs generic wisdom)
   - Identify 3-7 strongest signals per category

   **Extraction Examples:**
   ```
   Post: "Most founders waste months building features no one asked for..."
   → Belief: "Most founders build features without user validation"

   Post: "We tried to hire for culture fit and it set us back 6 months"
   → Scar: "Hired for culture fit over skill—damaged team velocity"

   Post: "I've learned that shipping fast beats perfect planning"
   → Lesson: "Shipping fast beats perfect planning every time"
   ```

4. **Generate Recommendations**
   - Automated dos/donts based on patterns
   - Suggested customRules from analysis
   - Founder signals (if extracting from content)
   - Confidence score for each recommendation

5. **Interactive Refinement (if mode = "interactive")**
   - Show automated recommendations
   - Show extracted founder signals (if founder mode)
   - Ask user to confirm, edit, or reject
   - Allow manual additions or corrections

5. **Create/Update Voice Profile**
   - POST if creating new
   - PUT if updating existing
   - Generate delta report if updating

6. **Version Control**
   - Tag profile with analysis date
   - Store analysis metadata
   - Enable rollback to previous version

## Outputs

1. **voice_profile_id** (string, UUID)
   - ID of created or updated profile

2. **delta_report** (object, conditional)
   - Only if updating existing profile
   - Shows differences from previous version
   - Tone changes, new/removed rules, confidence improvement

3. **strength_score** (number, 0-100)
   - Voice consistency metric
   - Based on:
     - Number of posts analyzed (more = better)
     - Consistency of patterns (low variance = better)
     - Comprehensiveness of analysis (all dimensions covered)
   - < 50: Weak signal, need more samples
   - 50-70: Moderate consistency, usable
   - 70-85: Strong consistency, production-ready
   - 85+: Highly consistent, premium quality

4. **analysis_summary** (string)
   - Human-readable summary
   - Example: "Analyzed 48 posts. Voice is direct (8.5/10) and professional (7.8/10) with minimal playfulness. Frequently uses question hooks (35%) and engagement CTAs (42%). Signature style: short sentences, tactical advice, honest founder stories."

5. **confidence_by_dimension** (object)
   ```typescript
   {
     tone: 85,              // High confidence (consistent tone)
     hooks: 72,             // Good confidence (clear patterns)
     ctas: 68,              // Moderate confidence (some variance)
     vocabulary: 91,        // Very high confidence (distinct signature)
     structure: 78          // Good confidence (consistent format)
   }
   ```

6. **founder_signals** (object, conditional - only if founder mode)
   ```typescript
   {
     beliefs?: string[];              // Extracted hot takes (3-7)
     lessons?: string[];              // Extracted hard-won lessons (3-7)
     contrarianOpinions?: string[];   // Extracted contrarian opinions (3-7)
     scars?: string[];                // Extracted failures/learnings (3-7)
     backstoryMoments?: string[];     // Extracted formative experiences (3-7)
     extraction_confidence?: number;  // 0-100: How confident in extractions
   }
   ```

7. **recommendations** (string[])
   - Next steps to improve voice profile
   - Examples:
     - "Add 2 more founder signal examples for deeper authenticity"
     - "Consider creating platform-specific rules (LinkedIn vs Twitter)"
     - "Test voice profile with bolta.voice.validate on held-out content"
     - "Review extracted founder signals—manually add any missing context"

## Voice Consistency Scoring

**Strength Score Formula:**

```
strength_score = (
  sample_size_score * 0.25 +        // 10+ posts = full score
  pattern_consistency_score * 0.35 + // Low variance = full score
  coverage_score * 0.20 +            // All dimensions covered = full score
  signature_clarity_score * 0.20     // Distinct voice = full score
)
```

**Sample Size Score:**
- < 10 posts: 30%
- 10-20 posts: 60%
- 20-40 posts: 80%
- 40+ posts: 100%

**Pattern Consistency Score:**
- High variance in tone (>3 SD): 40%
- Moderate variance (1-3 SD): 70%
- Low variance (<1 SD): 100%

## Error Handling

**Common Errors:**

1. **Insufficient Samples**
   - Error: "Need at least 10 posts for meaningful analysis"
   - Action: Request more samples or use bootstrap skill instead

2. **Account Has No Posts**
   - Error: "No posts found for account_id in the last 90 days"
   - Action: Increase days_back or provide manual samples

3. **Analysis Failed**
   - Error: "Voice analysis timed out or failed"
   - Action: Reduce max_posts or try again

4. **Inconsistent Voice**
   - Warning: "Voice analysis shows high variance - may indicate multiple authors or evolving style"
   - Action: Filter to specific date range or author

## Advanced: Platform-Specific Analysis

Analyze voice separately for each platform:

```bash
# Analyze LinkedIn voice
curl -X POST ".../analyze/" \
  -d '{
    "account_id": "{linkedin_account_id}",
    "platform_filter": "linkedin",
    "max_posts": 30
  }'

# Analyze Twitter voice
curl -X POST ".../analyze/" \
  -d '{
    "account_id": "{twitter_account_id}",
    "platform_filter": "twitter",
    "max_posts": 50
  }'
```

Then create platform-specific voice profiles or platform rules.

## Integration with Other Skills

**Before learn_from_samples:**
- Optionally run `bolta.voice.bootstrap` for baseline

**After learn_from_samples:**
1. **bolta.voice.validate**
   - Test the learned profile on held-out content
   - Validate consistency score

2. **bolta.draft.post**
   - Generate content using learned voice
   - Compare to original content

3. **bolta.voice.evolve**
   - Schedule periodic re-analysis
   - Track voice evolution over time

## Example Workflows

### Workflow 1: New User Onboarding (Has Content)

1. User connects Twitter account with 100+ posts
2. Run `bolta.voice.learn_from_samples` with account_id
3. Analyze 50 most recent posts
4. Generate voice profile automatically (auto mode)
5. Show user: "We analyzed your last 50 tweets and created a voice profile. Here's what we found..."
6. User confirms or refines
7. Set as default workspace voice

### Workflow 2: Refining Existing Voice

1. User has bootstrap voice profile (basic)
2. Run `bolta.voice.learn_from_samples` with existing_profile_id
3. Analyze 40 approved posts from composer
4. Generate delta report showing improvements
5. User reviews: "We found 3 new signature phrases and refined your hook patterns. Approve changes?"
6. Update voice profile with learned patterns
7. Strength score increases from 62 → 78

### Workflow 3: Multi-Platform Voice Setup

1. User has LinkedIn (professional) and Twitter (casual) accounts
2. Run `learn_from_samples` on LinkedIn → "Professional Brand Voice"
3. Run `learn_from_samples` on Twitter → "Casual Founder Voice"
4. Assign each voice to respective accounts
5. Use platformRuleIds to link platform-specific rules

## Notes

- **Garbage in, garbage out**: Quality of learned voice depends on quality of input posts
- **Sample size matters**: 10-20 posts = baseline, 40+ posts = high confidence
- **Filter strategically**: Use high-performing or approved posts only
- **Version profiles**: Save analysis metadata to enable rollback
- **Re-analyze periodically**: Voice evolves - re-run quarterly
- **Platform differences**: Consider separate analysis per platform
- **Author consistency**: If multiple authors, voice may be diluted
- This skill strengthens voice identity and should version voice profiles rather than overwrite silently

## Compliance & Permissions

**Required API Permissions:**
- `voice:read` - Read posts for analysis
- `voice:write` - Create/update voice profiles
- `accounts:read` - Access account posts

**Optional Permissions:**
- `posts:read` - Read post engagement metrics for quality filtering

## Version History

- **v2.0** (2026-02-16): Full API integration, delta reporting, strength scoring, platform-specific analysis
- **v1.0** (2025-XX-XX): Initial basic version

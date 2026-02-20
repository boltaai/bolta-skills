---
name: bolta.voice.bootstrap
version: 2.0.0
description: Create a comprehensive Voice Profile for a workspace. V2-ready - used by all agent types before content generation.
category: voice
roles_allowed: [Creator, Editor, Admin]
agent_types: [content_creator, reviewer, custom]
organization: bolta.ai
author: Max Fritzhand
---

## bolta.voice.bootstrap

Purpose:
Create a comprehensive Voice Profile for a workspace using the Bolta API. This skill creates production-ready voice profiles with full support for tone, founder signals, business DNA, platform rules, and custom guidelines.

## V2 Context
- **Hard dependency for content generation** — ALL content-creator agents require an active voice profile
- **Voice soft-delete in V2** — if voice profile deleted, all dependent jobs auto-pause
- **Agent memory integration** — agents can learn from voice feedback and refine over time
- **Voice is first-class primitive** — treated as core infrastructure, not configuration

When Used:
- First-time workspace onboarding
- Creating a new brand voice profile
- Migrating from basic to advanced voice setup
- Setting up founder vs brand voice modes

## Prerequisites

**Required:**
- Bolta API key (format: `bolta_sk_...`)
- Workspace ID (UUID format)

**Optional but Recommended:**
- Business DNA ID (for brand context)
- Platform rule IDs (for platform-specific adaptations)
- Product IDs (for product-aware content)

## Authentication

All API calls require the `Authorization` header:
```
Authorization: Bearer bolta_sk_your_api_key_here
```

## API Endpoints

**Base URL:** `https://platty.boltathread.com`

**Voice Profile Endpoints:**
- `POST /api/v1/workspaces/{workspace_id}/voice/profiles/` - Create voice profile
- `GET /api/v1/workspaces/{workspace_id}/voice/profiles/` - List voice profiles
- `PUT /api/v1/workspaces/{workspace_id}/voice/profiles/{profile_id}/` - Update voice profile

## Voice Profile Structure

### Core Fields

```typescript
{
  name: string;                    // Profile name (e.g., "Founder Voice", "Brand Voice")
  description?: string;            // When to use this profile

  // Tone (numeric scales 0-10)
  tone: {
    playful: number;               // 0 = serious, 10 = very playful
    professional: number;          // 0 = casual, 10 = very professional
    direct: number;                // 0 = diplomatic, 10 = very direct
    thoughtful: number;            // 0 = quick/surface, 10 = deep/reflective
  };

  // Content Guidelines
  customRules?: string;            // Freeform rules in markdown or plain text
  dos?: string[];                  // Things to do (max 7 items)
  donts?: string[];                // Things to avoid (max 7 items)
  styleKeywords?: string[];        // Voice style descriptors

  // Configuration
  contentSize?: string;            // "short", "standard", "long"
  useEmojis?: boolean | "auto";   // Emoji usage preference
  language?: string;               // ISO language code (e.g., "en", "es")

  // Advanced Features
  speakerMode?: "brand" | "founder";  // Who is speaking
  isDefault?: boolean;             // Set as workspace default
}
```

### Founder Signals (when speakerMode = "founder")

```typescript
founderSignals?: {
  beliefs?: string[];              // Hot takes, contrarian beliefs (max 7)
  lessons?: string[];              // Hard-won lessons from building (max 7)
  contrarianOpinions?: string[];   // Industry myths you push back on (max 7)
  scars?: string[];                // What failed, broke, embarrassed you (max 7)
  backstoryMoments?: string[];     // Experiences that shaped your thinking (max 7)
}
```

### Extended Fields (Advanced)

```typescript
{
  brandPersona?: string;           // Brand personality description
  rhetoricalDevices?: string[];    // Preferred rhetorical devices
  formality?: number;              // 0-10 scale
  pacing?: string;                 // "fast", "moderate", "slow"
  brandValues?: string[];          // Core brand values
  toneConstraints?: string[];      // Tone guardrails

  // Integration IDs
  businessDnaId?: string;          // Link to Business DNA profile
  platformRuleIds?: {              // Platform-specific rule overrides
    [platform: string]: string;
  };
  productIds?: string[];           // Associated product IDs
  topics?: string[];               // Content topic preferences
}
```

## Step-by-Step Bootstrap Process

### Step 1: Gather Voice Inputs

Ask the user for:

1. **Basic Info**
   - Voice profile name
   - Description (when to use)
   - Is this a founder voice or brand voice?

2. **Tone Settings** (0-10 scale)
   - Playful vs Serious
   - Professional vs Casual
   - Direct vs Diplomatic
   - Thoughtful vs Quick

3. **Content Guidelines**
   - 3-7 Dos (e.g., "Lead with pain points", "Use short sentences")
   - 3-7 Don'ts (e.g., "No corporate jargon", "Avoid hedging language")
   - Custom rules (freeform text)

4. **Content Preferences**
   - Content size: short/standard/long
   - Emoji usage: true/false/auto
   - Language: en/es/etc

5. **Founder Mode (if applicable)**
   - Beliefs (hot takes)
   - Lessons learned
   - Contrarian opinions
   - Scars (failures)
   - Backstory moments

### Step 2: Create Voice Profile via API

**Example: Brand Voice**

```bash
curl -X POST "https://platty.boltathread.com/api/v1/workspaces/{workspace_id}/voice/profiles/" \
  -H "Authorization: Bearer bolta_sk_your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Bolta Brand Voice",
    "description": "Bold, founder-led voice for Bolta social content",
    "tone": {
      "playful": 3,
      "professional": 7,
      "direct": 9,
      "thoughtful": 6
    },
    "dos": [
      "Lead with the pain point or outcome",
      "Use short, punchy sentences",
      "Be specific with numbers and examples",
      "Write in active voice",
      "Make claims you can back up"
    ],
    "donts": [
      "No corporate jargon or buzzwords",
      "Avoid hedging (\"maybe\", \"possibly\", \"could\")",
      "No \"revolutionize\" or \"game-changing\"",
      "Don'\''t bury the lede",
      "No vague promises"
    ],
    "styleKeywords": ["direct", "confident", "specific", "founder-led"],
    "contentSize": "standard",
    "useEmojis": false,
    "language": "en",
    "speakerMode": "brand",
    "isDefault": true
  }'
```

**Example: Founder Voice with Signals**

```bash
curl -X POST "https://platty.boltathread.com/api/v1/workspaces/{workspace_id}/voice/profiles/" \
  -H "Authorization: Bearer bolta_sk_your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Max - Founder Voice",
    "description": "Personal founder voice for thought leadership",
    "tone": {
      "playful": 2,
      "professional": 5,
      "direct": 10,
      "thoughtful": 8
    },
    "speakerMode": "founder",
    "founderSignals": {
      "beliefs": [
        "Most AI content fails because it optimizes for length, not clarity",
        "The best marketing is just solving real problems publicly",
        "Brand voice isn'\''t about tone - it'\''s about what you refuse to say"
      ],
      "lessons": [
        "Shipping fast beats perfect planning every time",
        "Your first 100 users will teach you more than 100 strategy docs",
        "Technical debt is fine. Strategic debt will kill you"
      ],
      "contrarianOpinions": [
        "Most \"thought leadership\" is just repackaged LinkedIn wisdom",
        "You don'\''t need a content calendar - you need conviction",
        "Engagement metrics are vanity. Pipeline metrics are sanity"
      ],
      "scars": [
        "Built a feature no one asked for - wasted 3 months",
        "Hired for culture fit over skill - set team back 6 months",
        "Tried to be everything to everyone - diluted the product"
      ],
      "backstoryMoments": [
        "Watched my first startup fail because we couldn'\''t articulate our value",
        "Realized most founders struggle with the same thing: consistent voice at scale",
        "Spent years ghostwriting for founders - saw the patterns that work"
      ]
    },
    "dos": [
      "Tell stories from the building experience",
      "Share specific failures and lessons",
      "Use concrete examples over abstract concepts",
      "Write like you'\''re talking to another founder"
    ],
    "donts": [
      "No inspirational quotes without context",
      "Avoid humble-bragging",
      "Don'\''t soften hard truths",
      "No theoretical advice - only battle-tested"
    ],
    "contentSize": "standard",
    "useEmojis": false,
    "language": "en",
    "isDefault": false
  }'
```

### Step 3: Verify Profile Creation

**List all voice profiles:**

```bash
curl -X GET "https://platty.boltathread.com/api/v1/workspaces/{workspace_id}/voice/profiles/" \
  -H "Authorization: Bearer bolta_sk_your_api_key_here"
```

**Response:**
```json
{
  "profiles": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "name": "Bolta Brand Voice",
      "description": "Bold, founder-led voice for Bolta social content",
      "tone": {
        "playful": 3,
        "professional": 7,
        "direct": 9,
        "thoughtful": 6
      },
      "is_default": true,
      "created_at": "2026-02-16T10:30:00Z",
      "updated_at": "2026-02-16T10:30:00Z"
    }
  ],
  "count": 1
}
```

## Inputs (Interactive Mode)

When running this skill interactively, gather:

1. **voice_name** (string, required)
   - Example: "Founder Voice", "Brand Voice", "Product Updates Voice"

2. **voice_description** (string, optional)
   - Example: "Personal founder voice for LinkedIn thought leadership"

3. **speaker_mode** (enum: "brand" | "founder", required)
   - "brand" = Company speaking
   - "founder" = Individual founder speaking

4. **tone_scores** (object, required)
   - playful: 0-10
   - professional: 0-10
   - direct: 0-10
   - thoughtful: 0-10

5. **dos** (string[], recommended, 3-7 items)
   - Example: ["Lead with outcomes", "Use short sentences", "Be specific"]

6. **donts** (string[], recommended, 3-7 items)
   - Example: ["No jargon", "Avoid hedging", "No vague promises"]

7. **content_preferences** (object, optional)
   - contentSize: "short" | "standard" | "long"
   - useEmojis: true | false | "auto"
   - language: ISO code (default: "en")

8. **founder_signals** (object, conditional - required if speaker_mode = "founder")
   - beliefs: string[] (3-7 hot takes)
   - lessons: string[] (3-7 hard-won lessons)
   - contrarianOpinions: string[] (3-7 industry myths)
   - scars: string[] (3-7 failures/embarrassments)
   - backstoryMoments: string[] (3-7 formative experiences)

9. **is_default** (boolean, optional, default: true)
   - Set as workspace default voice profile

## Behavior

1. **Validate Inputs**
   - Ensure workspace_id is a valid UUID
   - Ensure API key is in format `bolta_sk_...`
   - Validate tone scores are 0-10
   - Ensure dos/donts have 3-7 items each
   - If founder mode, ensure at least 3 items in each founder signal category

2. **Construct API Payload**
   - Build JSON payload matching VoiceCreationPayload structure
   - Include all provided fields
   - Set sensible defaults for optional fields

3. **Make API Request**
   - POST to `/api/v1/workspaces/{workspace_id}/voice/profiles/`
   - Include Authorization header
   - Handle errors gracefully (show user-friendly error messages)

4. **Parse Response**
   - Extract voice_profile_id from response
   - Save profile metadata for reference
   - Display success confirmation

5. **Generate Summary**
   - Show voice profile name, ID, and key characteristics
   - Display confidence/completeness score
   - Suggest next steps (learn from samples, validate content, etc.)

## Outputs

1. **voice_profile_id** (string, UUID)
   - The unique ID of the created voice profile
   - Used in subsequent API calls for content generation

2. **summary_of_voice** (string)
   - Human-readable summary of the voice characteristics
   - Example: "Direct, professional voice with minimal playfulness. Founder-led tone with emphasis on specific examples and battle-tested lessons."

3. **confidence_score** (number, 0-100)
   - Estimated completeness of the voice profile
   - Based on: presence of dos/donts, founder signals, custom rules
   - < 50: Basic setup, needs refinement
   - 50-75: Good foundation, ready for testing
   - 75-90: Well-defined, ready for production
   - 90+: Comprehensive, production-ready

4. **next_steps** (string[])
   - Recommended actions to improve or use the voice profile
   - Examples:
     - "Run bolta.voice.learn_from_samples to refine based on existing content"
     - "Test content generation with bolta.draft.post"
     - "Validate against existing posts with bolta.voice.validate"
     - "Create platform-specific rules for LinkedIn, Twitter, etc."

## Integration with Other Skills

**After bootstrap, recommend:**

1. **bolta.voice.learn_from_samples**
   - Feed existing content to refine the voice profile
   - Automatically extract style patterns from past posts

2. **bolta.voice.validate**
   - Test the voice profile by scoring existing content
   - Identify gaps or inconsistencies

3. **bolta.draft.post**
   - Generate test content using the new voice profile
   - Iterate on voice settings based on output quality

4. **bolta.voice.evolve**
   - Schedule periodic refinement based on user feedback
   - Track voice drift over time

## Error Handling

**Common Errors:**

1. **401 Unauthorized**
   - Message: "Invalid API key. Ensure your key starts with 'bolta_sk_' and is active."
   - Action: Verify API key in workspace settings

2. **400 Bad Request - Missing workspace_id**
   - Message: "Workspace ID is required and must be a valid UUID."
   - Action: Verify workspace_id format

3. **400 Bad Request - Invalid tone values**
   - Message: "Tone scores must be numbers between 0 and 10."
   - Action: Validate tone inputs

4. **422 Validation Error - Missing required fields**
   - Message: "Voice profile requires: name, tone, and at least 3 dos and 3 donts."
   - Action: Ensure all required fields are provided

## Advanced: Business DNA Integration

If a Business DNA profile exists, include it in the voice profile:

```json
{
  "businessDnaId": "dna_123abc",
  "brandValues": ["Innovation", "Speed", "Transparency"],
  "brandPersona": "Bold, technical founder who ships fast and talks candidly about failures"
}
```

**How to create Business DNA first:**

```bash
curl -X POST "https://platty.boltathread.com/api/v1/workspaces/{workspace_id}/dna/" \
  -H "Authorization: Bearer bolta_sk_your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Bolta Brand DNA",
    "website_url": "https://bolta.ai",
    "brand_values": ["Speed", "Clarity", "Authenticity"]
  }'
```

Then use the returned `id` in the voice profile as `businessDnaId`.

## Notes

- Voice profiles are **persistent** and stored in the Bolta backend (not local)
- Each workspace can have **multiple voice profiles** (e.g., founder voice, brand voice, product updates voice)
- One profile can be marked as **default** for the workspace
- Voice profiles can be **updated** after creation using PUT endpoint
- This skill must be run **before content-generation skills** if no voice profile exists
- **Founder mode** generates more personal, story-driven content vs brand mode
- **Founder signals** are the secret sauce for authentic founder-led content - invest time here

## Compliance & Permissions

**Required API Permission:**
- `voice:write` - Allows creation and modification of voice profiles

**Optional Permissions (for advanced features):**
- `voice:read` - List and view voice profiles
- `ai:generate` - Generate content using voice profiles
- `workspace:read` - Access workspace metadata

## Example Workflows

### Workflow 1: First-time Founder Setup

1. Run `bolta.voice.bootstrap` with founder mode
2. Provide 5+ items in each founder signal category
3. Create profile with `isDefault: true`
4. Run `bolta.draft.post` to test voice with a topic
5. Iterate on dos/donts based on generated content

### Workflow 2: Brand + Founder Voice Setup

1. Run `bolta.voice.bootstrap` for brand voice (isDefault: true)
2. Run `bolta.voice.bootstrap` again for founder voice (isDefault: false)
3. Use brand voice for company updates, announcements
4. Use founder voice for thought leadership, personal stories
5. Assign voice profiles to specific accounts via `/api/voice/assign`

### Workflow 3: Voice Migration (from external tool)

1. Export content from previous tool
2. Run `bolta.voice.learn_from_samples` with exported content
3. Review auto-generated voice profile
4. Run `bolta.voice.bootstrap` to create production profile with refinements
5. Run `bolta.voice.validate` on historical content to ensure alignment

## Version History

- **v2.0** (2026-02-16): Complete rewrite with full API integration, founder signals, Business DNA support
- **v1.0** (2025-XX-XX): Initial basic version with local generation only

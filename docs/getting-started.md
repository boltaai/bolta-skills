# Getting Started with Bolta Skills

**Complete quickstart guide to get you creating AI-powered content in 15 minutes.**

---

## Prerequisites

Before you begin, ensure you have:

- [ ] **Bolta Account** - Sign up at [bolta.ai](https://bolta.ai)
- [ ] **Workspace Created** - Create a workspace in your Bolta account
- [ ] **Admin/Owner Role** - You need admin access to create API keys

---

## Step 1: Get Your API Key

### Register Your Agent

1. Visit **[bolta.ai/register](https://bolta.ai/register)**
2. Select your workspace
3. Create an agent principal:
   - **Name:** `Claude Content Agent` (or your choice)
   - **Role:** `creator` (recommended for first agent)
   - **Permissions:** Check `posts:write` and `voice:read`

4. Copy your API key:
   ```
   API Key: sk_live_your_key_here_64_characters
   Workspace ID: 550e8400-e29b-41d4-a716-446655440000
   ```

⚠️ **Save your API key immediately** - It cannot be recovered (only regenerated)

---

## Step 2: Install the Bolta Skills Pack

### Option A: Full Installation (Recommended)

```bash
# Clone the complete skills repository
git clone https://github.com/boltaai/bolta-skills.git
cd bolta-skills

# Verify installation
ls skills/*/SKILL.md
# Should show 21+ skill files
```

### Option B: Quick Test (Single Skill)

```bash
# Download just the registry skill
curl -L https://raw.githubusercontent.com/boltaai/bolta-skills/main/skills/bolta.skills.index/SKILL.md \
  -o bolta.skills.index.md
```

---

## Step 3: Configure Environment

### For Claude Desktop (MCP)

1. **Find your MCP config file:**
   ```bash
   # macOS/Linux
   ~/.config/Claude/claude_desktop_config.json

   # Windows
   %APPDATA%\Claude\claude_desktop_config.json
   ```

2. **Add Bolta MCP server:**
   ```json
   {
     "mcpServers": {
       "bolta": {
         "command": "npx",
         "args": ["-y", "@boltaai/mcp-server"],
         "env": {
           "BOLTA_API_KEY": "sk_live_your_actual_key_here",
           "BOLTA_WORKSPACE_ID": "your-workspace-id-here"
         }
       }
     }
   }
   ```

3. **Restart Claude Desktop**

4. **Verify installation:**
   - Look for Bolta in the MCP servers list (hammer icon)
   - Should show "Connected" status

### For Terminal/API Use

```bash
# Add to your shell profile (~/.bashrc, ~/.zshrc)
export BOLTA_API_KEY="sk_live_your_actual_key_here"
export BOLTA_WORKSPACE_ID="your-workspace-id-here"

# Reload shell
source ~/.bashrc  # or ~/.zshrc
```

---

## Step 4: Test Your Setup

### Quick API Test

```bash
# Test API connectivity
curl https://platty.boltathread.com/v1/workspaces/${BOLTA_WORKSPACE_ID} \
  -H "Authorization: Bearer ${BOLTA_API_KEY}"

# Expected response:
{
  "id": "550e8400-...",
  "name": "My Workspace",
  "safe_mode": true,
  "autonomy_mode": "managed",
  "max_posts_per_day": 100
}
```

### Via Claude Desktop

Open Claude Desktop and ask:

```
Can you check my Bolta workspace policy?
```

**Expected response:**
```
Your Bolta workspace configuration:
- Safe Mode: ON
- Autonomy Mode: managed
- Daily Post Limit: 100 posts
- Hourly API Limit: 1000 requests

This means posts will be routed to Pending Approval for human review before scheduling.
```

---

## Step 5: Create Your First Voice Profile

**Every workspace needs a voice profile before creating content.**

### Via Claude Desktop

```
Can you help me create a voice profile for my brand?
```

The agent will run `bolta.voice.bootstrap` and ask you:
1. Brand name
2. Industry
3. Target audience
4. Brand personality traits
5. Tone description
6. Content dos and don'ts

**Complete the questionnaire** - takes 5-10 minutes.

### Via API (Non-Interactive)

```bash
curl https://platty.boltathread.com/v1/voice-profiles \
  -H "Authorization: Bearer ${BOLTA_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "workspace_id": "'${BOLTA_WORKSPACE_ID}'",
    "brand_name": "TechFlow Solutions",
    "industry": "B2B SaaS",
    "target_audience": "Software engineers",
    "brand_personality": ["professional", "empathetic", "educational"],
    "tone_description": "Friendly but professional. We explain complex concepts simply.",
    "content_dos": [
      "Use technical terms accurately",
      "Include practical examples",
      "Link to documentation"
    ],
    "content_donts": [
      "Never oversimplify",
      "Avoid marketing jargon",
      "Don't make claims without evidence"
    ]
  }'
```

**Save the returned `voice_profile_id`** - you'll need it for creating posts.

---

## Step 6: Create Your First Post

### Via Claude Desktop

```
Create a draft post about productivity tips for remote workers using my voice profile.
```

The agent will:
1. Load your voice profile
2. Generate content matching your tone
3. Create a post in Draft status (Safe Mode routing)
4. Return the post ID

**Expected response:**
```
Created draft post: [post_id]
Status: Draft
Voice Profile: TechFlow Brand Voice (v1)

Content preview:
"Struggling with focus while working from home? Here's what actually works..."

Next steps:
- Review the post at bolta.ai/posts/[post_id]
- Edit if needed
- Schedule when ready
```

### Via API

```bash
curl https://platty.boltathread.com/v1/posts \
  -H "Authorization: Bearer ${BOLTA_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "workspace_id": "'${BOLTA_WORKSPACE_ID}'",
    "voice_profile_id": "your-voice-profile-id",
    "prompt": "Share a productivity tip for remote workers",
    "requested_action": "draft_only"
  }'
```

---

## Step 7: Review and Schedule

### Via Web UI

1. Go to [bolta.ai/posts](https://bolta.ai/posts)
2. Find your draft post
3. Review content
4. Click "Schedule" and pick a time
5. Post moves to "Scheduled" status

### Via Claude Desktop

```
Show me my draft posts
```

Then:

```
Schedule post [post_id] for tomorrow at 2pm
```

---

## Next Steps

### 🎯 Recommended Learning Path

**Week 1: Learn the Basics**
1. ✅ Create voice profile
2. ✅ Create 3-5 draft posts
3. ✅ Learn the review workflow
4. ✅ Schedule your first post

**Week 2: Use Templates**
1. Create a content template
2. Use `bolta.loop.from_template` to generate 10 posts
3. Bulk review and schedule

**Week 3: Automation**
1. Read [autonomy-modes.md](./autonomy-modes.md)
2. Set up `bolta.cron.generate_to_review` (daily generation)
3. Configure daily digest emails

**Week 4: Scale Up**
1. Increase autonomy mode (assisted → managed)
2. Create multiple voice profiles (different content types)
3. Set up team members

---

## Common First-Time Issues

### Issue: "Voice Profile Not Found"

**Cause:** No voice profile created yet

**Solution:**
```
Run: bolta.voice.bootstrap
Before running: bolta.draft.post
```

### Issue: "API Key Invalid"

**Causes:**
- API key copied incorrectly (extra spaces)
- Using key from wrong workspace
- Key was rotated

**Solutions:**
1. Verify `BOLTA_API_KEY` exactly matches registration
2. Check workspace ID matches
3. Generate new key at bolta.ai/register

### Issue: "Posts Always Go to Draft"

**Cause:** Assisted autonomy mode + Safe Mode ON

**Solution:**
- This is expected behavior (safest mode)
- To schedule directly: Change autonomy mode to "managed" or "autopilot"
- Requires admin access to change workspace policy

### Issue: "Cannot Schedule Posts"

**Cause:** Creator role lacks `posts:schedule` permission

**Solutions:**
1. Request upgrade to "editor" role
2. OR: Use `requested_action: "send_to_review"` and let admin schedule

---

## Quick Reference

### Key Concepts

| Term | Definition |
|------|------------|
| **Voice Profile** | Your brand's tone, style, and content rules |
| **Safe Mode** | Routes all scheduled posts to human review |
| **Autonomy Mode** | Controls how autonomous your agent can be |
| **Principal** | An actor (human or agent) with permissions |
| **Quota** | Daily/hourly limits on post creation |

### Essential Skills

| Skill | Purpose |
|-------|---------|
| `bolta.voice.bootstrap` | Create initial voice profile |
| `bolta.draft.post` | Create a single post |
| `bolta.loop.from_template` | Bulk post generation |
| `bolta.inbox.triage` | Organize pending posts |
| `bolta.review.approve_and_route` | Bulk approve posts |

### API Endpoints

| Endpoint | Purpose |
|----------|---------|
| `GET /v1/workspaces/{id}` | Get workspace config |
| `GET /v1/voice-profiles` | List voice profiles |
| `POST /v1/posts` | Create a post |
| `GET /v1/posts` | List posts |
| `PATCH /v1/posts/{id}` | Update post status |

---

## Need Help?

- **Documentation:** [bolta.ai/docs](https://bolta.ai/docs)
- **GitHub Issues:** [github.com/boltaai/bolta-skills/issues](https://github.com/boltaai/bolta-skills/issues)
- **Email Support:** support@bolta.ai
- **Community:** [discord.gg/bolta](https://discord.gg/bolta) (coming soon)

---

## Congratulations! 🎉

You've completed the Bolta quickstart. You should now be able to:

- ✅ Create voice profiles
- ✅ Generate AI-powered content
- ✅ Review and schedule posts
- ✅ Understand workspace policies

**Next:** Read [autonomy-modes.md](./autonomy-modes.md) to learn how to scale your content automation.

---
name: wordpress-blog
description: >
  Research, write, visually art-direct, QA, and publish a genuinely high-quality
  long-form SEO article to the WordPress account connected through Bolta. Use this
  skill when the user asks to "write a blog post", "publish an article", "create an
  SEO article", "write this week's Bolta blog", "post this to WordPress", or wants
  a complete editorial workflow from search intent through verified publication.
  ChatGPT owns the editorial strategy, writing, and hero-image concept; Bolta
  provides brand context, WordPress connection, media delivery, publishing state,
  and verification. For recurring article creation, save the behavior as a Routine
  using the weekly_blog_article template.
---

# WordPress Blog

Create one publication-quality article from idea to verified WordPress publication.

This is an editorial operating procedure, not a generic content-generation call.

The skill owns:

**strategy → research → article → SEO package → visual concept → hero-image QA → WordPress delivery → verification**

Bolta is the execution and state layer. The AI client remains responsible for editorial judgment.

## Core principles

1. **Write for the searcher first.**
   The article must answer a real problem or query before introducing the product.

2. **Use Bolta's current brand context.**
   Never assume the voice, positioning, audience, or product capabilities from memory.

3. **ChatGPT writes the article.**
   Do not ask Bolta's generic content generator to create the long-form article.

4. **The image is part of the editorial work.**
   A new file is not enough. The visual concept must be meaningfully different from recent hero imagery.

5. **Publishing is not complete until verified.**
   Drafted, approved, queued, or uploaded is not the same as Published.

6. **Do not destroy good work because one delivery step fails.**
   Preserve the finished article, SEO package, and approved image so the failed step can be retried.

---

# When to use

Use this skill when the user wants:

- a new SEO article for the connected WordPress site;
- a long-form Bolta blog article;
- a publication-ready article rather than an outline;
- an article researched and written in the workspace's brand voice;
- a hero image generated specifically for the article;
- direct WordPress publication through Bolta;
- a repeatable weekly blog operation.

Do not use this skill for:

- a social-media post → use `social-publishing`;
- replying to conversations → use `reddit-engagement`, `cross-platform-engagement`, or `social-inbox`;
- a performance recap → use `analytics-review`.

---

# Tools this skill uses

| Tool | Why |
|-|-|
| `list-workspaces` | Resolve the workspace when the connector does not already scope it. |
| `list-accounts` | Confirm a connected WordPress account and avoid guessing among multiple accounts. |
| `get-voice-context` | Load the resolved Voice Profile + Business DNA context before editorial work. |
| `list-business-dna` | Find the current/default DNA entry when deeper visual brand fields are needed. |
| `get-business-dna` | Pull visual identity, aesthetics, logo guidance, and positioning for image art direction. |
| `list-workspace-posts` | Inspect recent WordPress articles and their media before choosing a topic/image concept. |
| `create-wordpress-blog-post` | Create the article, SEO fields, WordPress media, and requested publication action in one canonical delivery path. |
| `get-post` | Verify the complete Bolta post state after delivery/publication. |
| `get-post-platform-details` | Inspect WordPress-specific fields when troubleshooting or verifying metadata. |
| `update-post-platform-details` | Correct WordPress metadata on an existing post if needed. |
| `update-post` | Repair article/media state in place rather than deleting and recreating the post. |
| `submit-for-review` | Use when the workspace/user requires review instead of direct publication. |
| `approve-post` | Approve the exact reviewed revision when the approval path is active. |
| `publish-post` | Publish an already-created Bolta post when direct WordPress creation did not perform the final publish step. |
| `list-routine-templates` | Discover the recurring blog template. |
| `create-routine` | Save this behavior as a repeatable background operation. |
| `activate-routine` | Arm the saved blog routine. |
| `run-routine-now` | Prove the saved routine dispatches through the same runtime. |
| `list-routine-runs` | Inspect execution history of the routine. |

Image generation is performed by the host AI client's image-generation capability, not by inventing an MCP tool.

Web/search research may be used when current external information materially improves the article. Do not fabricate sources, statistics, market claims, or customer examples.

---

# Prerequisites

Before writing:

- Resolve the Bolta workspace.
- Confirm a healthy connected WordPress account.
- Load `get-voice-context`.
- If deeper Business DNA fields are needed, use the DNA id from the resolved context or `list-business-dna`, then `get-business-dna`.
- Inspect recent WordPress posts with `list-workspace-posts`.
- If there are multiple WordPress accounts, ask the user which account to use rather than guessing.
- Never ask the user for raw WordPress credentials; Bolta owns the connection.

If no WordPress account is connected, use the appropriate Bolta connection flow and stop before writing/publishing unless the user explicitly only wants the article draft.

---

# Workflow

## 1. Understand the brand

Call `get-voice-context`.

Capture:

- what the business actually does;
- who it serves;
- positioning;
- tone;
- dos;
- don'ts;
- banned patterns;
- persona/speaker mode;
- platform adaptations;
- what information is missing.

If the voice context is empty or incomplete, say so. Do not silently invent a brand voice.

For deeper brand/visual context:

`list-business-dna` → select the current/default DNA → `get-business-dna`.

Use DNA for:

- visual aesthetics;
- colors;
- brand values;
- visual tone;
- logo guidance;
- positioning facts.

Do not force social-post brevity onto long-form editorial writing. Preserve the brand's character while allowing the depth required by search intent.

---

## 2. Inspect recent editorial history

Before choosing a topic, inspect recent WordPress content:

`list-workspace-posts(workspace_id, status="published", platform="wordpress", ...)`

Review at least the most recent 10 when available.

Identify:

- recent article topics;
- repeated keywords/search intents;
- obvious cannibalization risk;
- repeated structures;
- recent CTA patterns;
- recent hero-image concepts;
- attached media patterns.

Do not choose essentially the same article twice because the wording differs.

A new article should either:

- answer a distinct search intent;
- go materially deeper;
- serve a different stage of the buyer journey;
- or deliberately update/expand an older article.

---

## 3. Choose the SEO opportunity

Independently choose a meaningful customer pain point the product actually helps solve.

Define before drafting:

### Primary search intent

Examples:

- informational;
- commercial investigation;
- comparison;
- how-to;
- problem/solution.

### Primary query / keyword

One main search question the article should clearly satisfy.

### Supporting query cluster

A small coherent set of related questions/sub-intents.

Do not build a keyword salad.

Prefer topics that make sense for someone who has never heard of the brand.

The article should still be worth reading if every product mention were removed.

### Topic quality test

Do not proceed until all are true:

- a real person could plausibly search this;
- the query reflects a problem the brand can credibly help with;
- the article can provide substantive help without product hype;
- the topic is not a near-duplicate of a recent article;
- no required factual claim must be invented.

---

## 4. Research before writing

Research enough to write accurately.

Use current external research when the topic depends on:

- platform/API behavior;
- current regulations;
- recent market changes;
- current product behavior outside Bolta;
- statistics;
- named competitors;
- time-sensitive SEO context.

Prefer primary or high-authority sources.

Do not research merely to decorate the article with citations.

Never invent:

- statistics;
- customer outcomes;
- quotes;
- partnerships;
- regulatory requirements;
- platform capabilities;
- competitor features.

If a useful fact cannot be verified, write around it.

---

## 5. Build the editorial thesis

Before drafting, state internally:

- the reader's problem;
- the misconception or failure mode;
- the useful solution model;
- why the solution matters;
- where Bolta naturally fits;
- the single action the reader should understand by the end.

This prevents generic "10 tips" writing.

A strong article should make one coherent argument while satisfying several related search questions.

---

## 6. Write the canonical article

The AI client writes the complete article itself.

Do not outsource the canonical copy to Bolta's generic writer.

The article should usually include:

- one SEO-focused H1;
- a fast introduction that answers why the reader should care;
- logical H2/H3 hierarchy;
- concrete explanations;
- practical workflows/examples;
- tradeoffs and failure modes;
- clear next steps;
- FAQ/search-intent section where useful;
- a contextual CTA.

### Writing rules

Preserve the resolved brand voice.

For Bolta-style SaaS editorial writing, prefer:

- plain language;
- natural contractions;
- useful specifics;
- calm confidence;
- one clear point at a time;
- practical examples;
- understated product positioning.

Avoid:

- corporate jargon;
- "AI-powered revolution" language;
- excessive hype;
- fake profundity;
- empty inspirational conclusions;
- keyword stuffing;
- repeated summary sections;
- obvious AI cadence;
- rhetorical-question-then-answer hooks used mechanically;
- em dashes when the voice forbids them;
- shallow listicles;
- product mentions in every section.

The reader should receive real value before the product is introduced.

---

## 7. Keep a canonical document

The complete publication-ready article should exist as one canonical editable document in the AI client.

If the client supports a dedicated writing/document experience, use it.

Keep outside the canonical article:

- keyword notes;
- SEO reasoning;
- research notes;
- image prompts;
- QA commentary;
- MCP/tool chatter;
- publishing status.

The body sent to WordPress must be the full canonical article, not a summary or shortened derivative.

Before delivery, compare the outgoing body against the canonical document for truncation.

---

# SEO package

Prepare separately:

- primary keyword/query;
- supporting keyword/query cluster;
- search intent;
- SEO title / meta title;
- meta description;
- suggested slug;
- excerpt;
- categories;
- tags;
- focus keyphrase when useful;
- post type = post;
- natural internal-link opportunities.

## Internal linking

Prefer contextually useful links to relevant:

- product pages;
- feature pages;
- public tools;
- comparisons;
- educational articles;
- agent/automation pages where still product-relevant.

Use descriptive anchors.

Never invent a URL.

If the exact URL cannot be confidently resolved, leave an explicit internal-link recommendation for review rather than fabricating one.

---

# Hero image

The image workflow is:

**article → recent visual audit → unique physical concept → generation → visual QA → WordPress media**

The image is not an afterthought.

## 8. Audit recent hero imagery first

Inspect the recent WordPress posts and attached/featured media.

Build a mental inventory of recurring:

- subject;
- gender/presentation;
- setting;
- activity;
- camera angle;
- framing;
- composition;
- props;
- lighting;
- visual metaphor;
- aesthetic.

A new image file depicting essentially the same setup is a failure.

### Temporary exclusions

When recent heroes already overuse something, temporarily exclude it.

Example:

If recent articles already show:

- a woman seated at a desk;
- a laptop;
- notebook/papers;
- plants;
- warm home-office light;
- three-quarter desk composition;

do NOT generate another variation of that scene.

A slightly different pose, crop, room, plant, shirt, or laptop does not make it a new concept.

---

## 9. Derive a unique physical visual concept

Translate the article's **unique thesis** into a physical scene.

Do not translate the broad category.

Bad:

> Social media automation article → founder working on laptop.

Good:

> Approval workflow → overhead physical editorial process where a human hand physically holds the final item before release.

A Visual Concept should specify:

- WHO or WHAT is visible;
- WHAT is happening;
- WHERE it happens;
- WHAT objects are present;
- the emotional mood;
- the visual metaphor;
- why this metaphor belongs to this article;
- how it differs from recent hero images.

### Rotate visual archetypes

Actively vary the form.

Possible archetypes:

- overhead process scene;
- close-up hand/action;
- editorial still life;
- real small-business location;
- workshop/studio;
- physical metaphor;
- outdoor/location scene;
- collaborative group;
- object-led composition;
- sequence/progression;
- spatial organization;
- tactile material/process.

Do not mechanically cycle through a fixed list. Use the article's idea.

---

## 10. Generate from the visual concept only

The image-generation instruction should contain only what is necessary to render the scene.

Do NOT feed the image generator:

- article body;
- article title;
- SEO metadata;
- WordPress details;
- CMS context;
- phrases like "image of this blog post";
- website/dashboard language.

Default direction, adjusted to the concept:

- premium editorial photography or high-quality editorial illustration;
- realistic/natural where photographic;
- sophisticated but approachable;
- wide landscape / approximately 16:9;
- one clear focal subject/action;
- uncluttered composition;
- useful negative space.

Do NOT force:

- warm home-office lighting;
- laptop;
- desk;
- plants;
- single seated founder;
- generic "productivity" stock-photo aesthetics.

---

## 11. Hero-image content rules

The output must read as a standalone editorial visual.

Reject:

- article screenshots;
- browser windows;
- dashboards;
- CMS/WordPress screens;
- app interfaces;
- social-media interfaces;
- fake UI;
- device mockups showcasing software;
- presentation slides;
- infographics;
- posters;
- large headlines;
- labels;
- slogans;
- logos as focal content;
- prominent intentional text.

### Realism exception

Do not reject a good editorial photograph because physical objects contain tiny incidental text.

Allowed when natural and non-focal:

- notebook scribbles;
- book spines;
- keyboard keys;
- paper markings;
- package printing;
- distant signs;
- calendar marks;
- blurred documents.

Laptop/phone screens may appear incidentally when they are dark, turned away, obscured, blank, or out of focus and not presenting recognizable UI as the subject.

---

## 12. Visual QA

Inspect the actual generated image.

PASS only when all are true:

1. It reads as a standalone editorial scene.
2. No prominent intentional text dominates it.
3. No recognizable/focal software UI.
4. The subject/action meaningfully represents the article.
5. It makes sense even without the article title.
6. It is polished enough for a professional SaaS publication.
7. It is materially different from recent heroes.

### Originality test

The image should differ from recent Bolta heroes in at least **three** of:

- subject;
- setting;
- activity;
- camera angle;
- composition;
- props;
- lighting;
- visual metaphor.

If it fails originality, explicitly name what repeated.

Example:

> Same seated woman, same desk, same laptop/papers, same warm home office.

Then generate a **different concept**, not a minor variation.

### Attempts

Allow up to three image-generation attempts.

Regenerate for:

- UI/mockup failure;
- prominent text;
- weak relation to article;
- low visual quality;
- repetitive visual concept.

Do not regenerate merely to eliminate harmless incidental markings.

If all three attempts fail, stop the publication step. Preserve the article and SEO package and report the image as the blocker.

Never publish a bad/repetitive hero just to make the run green.

---

# WordPress delivery

## 13. Prefer the canonical WordPress tool

When the article and hero image are final, use `create-wordpress-blog-post` as the preferred delivery path.

Provide:

- full article title;
- complete Markdown body;
- excerpt;
- slug;
- categories;
- tags;
- SEO object;
- the exact QA-approved image as featured media;
- requested action.

The tool is designed to:

- resolve the WordPress account;
- create the post;
- set WordPress article fields;
- upload media into the actual WordPress Media Library;
- assign the featured image;
- submit/schedule/publish when requested.

Do not split the workflow into many lower-level calls unless needed for recovery or verification.

### Media object

`media` is an array of objects, not bare URLs:

```
{ source, role: "featured"|"inline", alt_text, filename, caption,
  placement: { type: "after_heading"|"before_heading"|"after_paragraph"|"append",
               heading | paragraph_index } }
```

`source` is the image itself — a file you generated in this conversation (a file
attachment with a `download_url`), `{"url": "https://..."}`, or a plain URL
string. Each is uploaded into WordPress's real Media Library; the
`wordpress_media_id` that comes back is what WordPress uses, never an internal
Bolta media id.

For the hero:

- `role: "featured"`;
- meaningful `alt_text`;
- clean `filename`;
- the exact approved image as `source`.

Never substitute an older similar image because upload is easier.

### Exact parameters

`create-wordpress-blog-post(title, content, content_format="markdown", excerpt,
slug, categories, tags, seo, media, requested_action, scheduled_time, timezone,
idempotency_key)`.

`title` and `content` are the only required fields, and both are yours — the
tool takes the article you wrote and does not generate one. `content_format`
currently supports `markdown` only. `seo` is advisory: it informs
`seo_validation` warnings in the response and never blocks the request, so read
those warnings rather than assuming silence means the SEO package was good.
`requested_action` is `draft` (the default), `submit_for_review`, `schedule` or
`publish`. `idempotency_key` makes a retry safe after a timeout — use it rather
than re-issuing a bare create, which would produce a second article.

---

## 14. Review policy

Respect the user's instruction and workspace safety policy.

### Draft-only request

Use requested action = draft.

### User wants review

Use the review path and do not publish until approved.

### User explicitly requested publication

Publish when permitted.

If workspace Safe Mode or permissions prevent direct publish:

- submit for review;
- explain what blocked immediate publication;
- do not bypass the guardrail.

For automated recurring article routines, default to review unless the workspace already explicitly permits the requested autonomy.

---

## 15. Verify the final post

After creation/publishing:

`get-post(post_id)`

Verify:

- full article body is present;
- no truncation;
- correct WordPress account;
- correct title;
- correct status;
- hero media attached;
- expected metadata present;
- publication state is Published when publication was requested.

When needed:

`get-post-platform-details(post_id, platform="wordpress")`

Verify WordPress-specific fields.

Success is NOT:

- draft created;
- review approved;
- queued;
- publish task started;
- image uploaded;
- featured media id assigned.

Success for a publish request is:

**the final post is Published, with the complete article and the intended hero image attached/assigned.**

When a public WordPress URL is available, report it.

---

# Pre-publish QA checklist

Before publication, explicitly check:

### Editorial
- Search intent is clear.
- Primary query is answered.
- Article is substantial, useful, and properly structured.
- No fabricated claims.
- Brand voice was loaded before writing.
- Bolta/product positioning appears only where natural.
- Canonical article is complete.

### SEO
- SEO title prepared.
- Meta description prepared.
- Slug prepared.
- Excerpt prepared.
- Categories/tags appropriate.
- Internal links are valid or clearly marked as recommendations.

### Hero
- Recent hero history inspected.
- New concept derives from the article's unique thesis.
- Image passed text/UI QA.
- Image passed originality QA.
- Exact approved image is being used.
- Alt text describes the image accurately.

### WordPress
- Correct account selected.
- Full article body sent.
- Hero uploaded to WordPress media.
- Featured image corresponds to the approved hero.
- WordPress metadata is present.
- Requested action matches the user's instruction.

Fix failures before publishing.

---

# Failure handling

## No WordPress account

Do not guess credentials.

Provide the Bolta connection path and stop the publication leg.

## Multiple WordPress accounts

Ask which destination to use.

## Brand context missing

State that the brand context is incomplete.

Do not pretend the resulting writing is voice-matched.

## Article creation succeeds, image fails

Preserve the article and SEO package.

Do not publish with a knowingly bad or repetitive image.

## Media upload fails

Do not regenerate the article.

Retry only the media/delivery step after diagnosing the upload.

## Metadata error

Repair WordPress fields in place.

Do not recreate the article.

## Quality block

Use the returned reason, repair the affected content with `update-post`, and re-run the validation.

Do not change status manually to bypass quality controls.

## Safe Mode

Route to review instead of trying to work around it.

## Permission error

Use `get-my-capabilities` if available in the active MCP surface, explain the missing permission, and stop.

## Publish partially fails

Report the exact state.

Never describe queued/processing as Published.

## Image originality failure

A new binary file is not enough.

If the new image repeats a recent concept, treat it as failed QA and regenerate from a different visual metaphor.

---

# Definition of done

For a full publish request:

- current Voice Context was loaded;
- recent editorial history was inspected;
- a distinct search opportunity was selected;
- the AI client wrote the complete article;
- one canonical article body exists;
- SEO package is complete;
- recent hero imagery was audited;
- the hero image is conceptually distinct;
- the hero passed visual QA;
- exact hero was delivered to WordPress;
- complete article was delivered without truncation;
- WordPress metadata is set;
- final post state is Published;
- publication result/URL is reported when available.

If any public-facing step cannot be verified, report it as incomplete.

---

# Quality bar

A successful run should feel like an editor, SEO strategist, art director, and publishing operator completed one piece of work together.

Do not optimize for producing "a blog post."

Optimize for producing **one article worth publishing**.

---

# Save this as a Routine

When the user wants this to happen repeatedly, do not build an Agent.

Use the existing Routine layer.

## Discover

`list-routine-templates()`

Find:

`weekly_blog_article`

The live template is designed to create a researched long-form article draft in the brand voice on a schedule.

## Create

Conceptually:

`create-routine(...)`

with:

- template_key = weekly_blog_article;
- the user's outcome in their own words;
- trigger_type = schedule;
- wall-clock schedule;
- workspace/user timezone;
- instructions capturing editorial preferences;
- approval_policy = review_every_artifact unless the user explicitly requests otherwise and workspace policy permits it;
- output_config appropriate for one article.

Routine operations are connector/workspace-scoped in the current MCP surface; do not invent a `workspace_id` argument where the live tool schema does not expose one.

## Activate

`activate-routine(routine_id)`

Creating a Routine does not arm it.

## Prove dispatch

When the user wants a test:

`run-routine-now(routine_id)`

Then inspect:

`list-routine-runs(routine_id)`

The recurring server-side routine and this interactive skill should share the same brand context, execution infrastructure, approval policy, and publication path.

### Important distinction

The `weekly_blog_article` RoutineTemplate currently produces a reviewable article artifact. This interactive `wordpress-blog` skill owns the richer editorial behavior, hero-image generation/QA, and direct WordPress delivery when the AI client is present.

If the server-side Routine does not yet execute every step in this skill, report that distinction honestly rather than implying perfect parity.

---

# Scheduled-run behavior

For a standing scheduled blog operation:

- never disable or pause the recurring schedule because one run failed;
- preserve successful intermediate work;
- identify the exact blocker;
- let the next scheduled run remain armed;
- avoid duplicate topics and duplicate hero concepts across runs;
- maintain an editorial history rather than treating each run as stateless.

The long-term target is parity:

**run interactively through this skill now**
and
**save the same outcome as a Routine for durable execution later**.

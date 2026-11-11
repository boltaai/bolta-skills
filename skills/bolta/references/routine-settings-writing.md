# Bolta routine settings: how it writes

`settings`, inside `output_config` on `create-routine` and `update-routine`, steers the writer itself: the strongest lever on quality after `goal` and `instructions`. Set what the user said; leave the rest out (each block is optional). Labels as in [routine-settings.md](routine-settings.md). Back to [routine-settings-output.md](routine-settings-output.md).

## Which routine takes which

| Block | Taken by |
|-|-|
| `editorial`, `tone` | Post routines: weekly posts, founder stories, customer wins, LinkedIn positions, Square, best posts again |
| `storyteller` | Founder stories, customer wins, merged pull requests only |
| `longform` | Research series and the weekly article only |
| `repurposing` | Best posts again and threads (below) |

`storyteller` or `longform` anywhere else is refused at save, as is any other key.

## `editorial`: what the posts cover and look like

- `contentPillars`: up to 20 themes, 200 characters each. Rotation is the point: 3-5 the user names ("pricing mistakes", "client results", "behind the scenes") (advice). Never pillars the business didn't give.
- `contentTypes`: any of `text_post`, `hook_story`, `listicle`, `carousel`, `thread`, `poll`. `thread`: X only, exactly one X account, no pictures. `poll`: X only. `carousel`: only with carousel pictures. Leave it out to let Bolta vary the shape.
- `hashtagStrategy`: `none`, `minimal`, `moderate` or `heavy`. `minimal` suits LinkedIn and X; `moderate` Instagram (advice).
- `promotionalAngle`: true or false, whether posts may sell. False for founder and thought-leadership routines (advice).
- `includeProductCta` with `productId`: mention one of the brand's products. Only with a product id the user or Bolta's page gave; nothing here lists products.

## `tone`

One of `educational`, `bold`, `insightful`, `conversational`. Only on the user's word ("make it punchier" is `bold`, advice); the voice already carries tone, so leave it out by default.

## `storyteller`: stories from real events

- `storySources`: any of `milestones`, `metrics_wins`, `failures_lessons`, `team_moments`, `customer_stories`, `industry_takes`. Founder stories: `milestones` and `failures_lessons` (Bolta's planner). Customer wins: `customer_stories` only.
- `narrativeThemes`: up to 20 themes ("hiring our first engineer").
- `contentStyle`: `raw` (unpolished, first person) or `polished`. `storyLength`: `short`, `medium` or `long`.
- These shape a story; they are not the story. Put the real events in `instructions` ("We lost our biggest client in March; we rebuilt onboarding"). With none, the posts turn generic: never run a story routine without real material (Bolta: "cannot stand in for evidence").

## `longform`: researched writing

- `topic` (up to 1000 characters): the one subject, specific: "Why physio clinics lose patients after visit three."
- `researchDepth`: `quick` or `deep`.
- `sourceUrls`: up to 3 public pages to work from. Every one is read at each run; one that can't be read refuses the run, so give stable pages. Not together with a different `source_urls` list.
- `outputFormat`: the weekly article takes only `article` (or none). A research series takes `thread` (X only, exactly one X account) or none for posts on any network; never `article` or `carousel`.

## `repurposing`: best posts again

`{"sourceAccountId": "<account id>", "lookbackDays": 90, "minEngagement": 1, "maxSourcesPerRun": 1, "postsPerSource": 3}` (the defaults; `lookbackDays` at most 365). `count` must equal `maxSourcesPerRun` times `postsPerSource`, at most 8. Text only, no voice. Without posts that earned likes, comments or shares in that window, the run is skipped.

## Always

- Fill settings only from what the user said or their documents show; ask before inventing pillars, themes or a product mention.
- Put the real facts and events in `instructions`; settings shape writing, they never supply facts.

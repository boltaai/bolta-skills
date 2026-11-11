# Saving a workflow and putting it on Claude's schedule

## The saved file

- A folder holding `<name>/SKILL.md`. The name: lowercase letters, numbers and hyphens, 64 characters at most, same as the folder. Never synced, and never starting with anthropic-skills (both are taken).
- Frontmatter: `name`, and a `description` (1,024 characters at most) with what it does and the user's own phrase: "Use when Jane says run my newsletter posts."
- Body: workspace and accounts by name, the steps in the user's words, what to do when a source is missing, the "already made this week?" check, then the two closing lines, word for word.
- No questions mid-run: nobody can answer. Anything needing the user becomes a suggestion in the run's reply.

## Where to save it

| Host | How | Reaches |
|-|-|-|
| claude.ai or Cowork | Zip the folder (the folder itself at the top), name it `<name>.skill`, and present it as a file (`present_files`, or `SendUserFile` where the host has that instead). The user taps **Save skill**. | Their claude.ai account: chat, Cowork, scheduled runs, and Claude Code signed in to it. |
| Claude Code | Write `~/.claude/skills/<name>/SKILL.md`. It loads in this session; if that folder didn't exist at the start, the user runs `/reload-skills`. | This machine only: the terminal and the Desktop app's local jobs. |

No **Save skill** button: skill creation may be off for the organization, or no file can be shown. Give the text and one line: "Upload it at Customize > Skills on claude.ai." A cloud job from Claude Code needs it saved there too.

## Putting it on a schedule

Say "Claude weekly job". Claude calls its own schedulers "routines" too, so never a bare "routine".

| Where | What to know |
|-|-|
| claude.ai (new experience) and Cowork | Runs in the cloud on paid plans, even with the computer asleep, with the user's connected apps, skills and installed plugins. Claude proposes name, schedule and instructions; the user clicks **Schedule**. Hourly, daily, weekdays, weekly or manual. Tasks Claude creates may approve every step on their own. |
| Claude Code Desktop app, local job (Claude's own Routines page) | Runs only while the app is open and the computer awake. A missed time runs once on wake, possibly hours late. A permission prompt stalls the run: suggest **Run now** once and allowing the draft steps. |
| Claude Code cloud job (`/schedule`) | No permission prompts and no installed plugins, so Bolta's checks don't run. Needs the skill on the claude.ai account and Bolta connected at claude.ai. At most hourly. |
| `/loop` or an in-session timer | Not a weekly job: it stops with the session, and repeats end after 7 days. |

- The job's instructions: "Run my newsletter-posts workflow for Acme.", then the two closing lines, word for word.
- Confirm only what the host shows was created: "Set: Fridays 2:00 pm, a Claude weekly job. It saves drafts to Acme and sends them for review."
- Nothing created, or no scheduler here: say so in one line and offer the honest substitute: "It isn't scheduled. On Fridays, say 'run my newsletter posts'."

## Why drafts only

During a scheduled run, Bolta's check may not run, may stall the run, or may be passed automatically. The file's own lines travel everywhere. On the default setting, drafts and sending for review need no check, so the run never stalls and the user still decides every post. On careful, saving several drafts at once still asks.

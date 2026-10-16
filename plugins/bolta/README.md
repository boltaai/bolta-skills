# Bolta

Plan, draft, schedule, review and measure social content in your Bolta workspace, from a conversation. The plugin drafts first and moves a post forward only when you say so for that exact post. It works with the social accounts, voice and approval rules already set up in Bolta; it does not replace them.

Version 0.1.0 (beta). Built for supervised use: read the limits below before you rely on it for anything that must be audited.

## Install

**Claude Code**

```
/plugin marketplace add boltaai/bolta-skills
/plugin install bolta@bolta-marketplace
```

Then run `/mcp`, choose the `bolta` server (shown as `plugin:bolta:bolta`) and sign in to Bolta in the browser. The sign-in page has a workspace dropdown that is pre-selected to the first workspace in your list. Pick the one you mean. Then run `/bolta:setup`.

**Cowork and Claude chat (claude.ai, desktop, mobile)**

Add this repository as a marketplace from your account's plugin settings, or upload a zip of the `plugins/bolta` folder, then connect Bolta on the plugin's Connectors tab. These two hosts are listed in Anthropic's documentation as supported but have not yet been tested end to end with this plugin.

## What it does

Ask in plain words. In Claude Code and Cowork the same jobs are also available as commands:

| Command | Does |
|-|-|
| `/bolta:setup` | Checks the connection, workspace, timezone, Safe Mode, accounts and voice. Read-only. |
| `/bolta:draft <topic>` | Writes one post and saves it as a Draft. Nothing is scheduled or published. |
| `/bolta:plan-week [focus]` | Looks at what is scheduled, finds the gaps and proposes a week. Creates Drafts only after you agree. |
| `/bolta:review` | Works the approval queue one item at a time. |
| `/bolta:inbox` | Reads mentions and reply drafts and helps you answer. |
| `/bolta:report [days]` | Reports performance and what to do about it. Read-only. |
| `/bolta:status` | Shows what is going out and what needs you. Read-only. |

Behind them are thirteen skills: publishing, approvals, inbox, outbound engagement (Reddit, Threads, Bluesky, Mastodon, plus links you paste for X and LinkedIn), analytics, content planning, routines, brand voice setup and check, accounts and buckets, WordPress articles, workspace setup, and undo and recovery. Four subagents are available in Claude Code and Cowork: an approval batch reviewer, a performance analyst and a community triage agent (all read-only, none can approve, send or publish), and a content calendar planner that can only save Drafts.

## How it keeps you in control

- **Drafts first.** New content is saved as a Draft. Moving it forward follows a fixed ladder: show it, wait for your go-ahead naming that post, submit for review, approve with an explicit time, read back what actually happened.
- **Confirmation prompts (Claude Code, and possibly Cowork).** Before anything that goes public, approves a post, changes the brand profile, starts automation or deletes, a prompt titled "Confirmation needed (Bolta plugin safety check)" appears. Allow rules and bypass-permissions mode cannot switch it off. In non-interactive runs (`claude -p`, CI, scheduled sessions) these calls are denied, so unattended Claude can read and draft but never approve, schedule or publish. A normal "write a post and schedule it" conversation shows one prompt; "publish now" shows two; reviewing N posts shows N.
- **Chat has no prompts.** Hooks do not run in claude.ai chat, desktop or mobile. There the skills ask you in words and wait, and the server's own approval gate for sign-in connections still applies. If a person must sign off, keep Safe Mode on and approve in the Bolta Hub yourself.
- **Server gate.** This plugin connects through the browser sign-in. Bolta's server then sends anything that is not a Draft to Pending Approval and refuses to schedule or publish an unapproved post. A connection made with a pasted `bolta_sk_` API key skips that gate, so do not use one with this plugin. The server cannot tell your approval from Claude's: an `approve-post` call from the conversation counts as yours if you are an admin or owner. That is why the plugin asks first.
- **Other people's text is data.** Comments, mentions, Reddit threads and fetched pages are treated as material to read, never as instructions. If such text tries to steer Claude, it tells you.
- **Read tools prompt once in Claude Code.** Allow the read tools by name (`list-workspaces`, `get-workspace`, `get-my-capabilities`, `list-accounts`, `get-voice-context`, `get-post`, `list-scheduled-posts`, `list-workspace-posts`, `list-inbox-items`). Do not allow the whole server: that would also silence the host's own prompt on tools the plugin does not guard.

Setting (Claude Code, `/plugin configure bolta@bolta-marketplace`): **Confirmation level**. `all-external-effects` (default) also confirms routines, deletes, brand-profile edits and campaign status changes. `publish-only` confirms only what goes public or approves a post. Skipping the setting keeps the default.

## What is sent where

- **To Bolta (mcp.bolta.ai), through the Bolta connector:** what you ask for as tool arguments, such as post text, account choices, times, URLs you give it, your approvals, and Bolta's replies to them. Claude reads results from your workspace (posts, accounts, analytics, inbox rows) to answer you. Sign-in is OAuth, handled by the host; the plugin never sees or stores a password or key.
- **By the plugin itself:** nothing. Its only executable parts are two short shell scripts (`scripts/`) that read the tool call from standard input and print a decision or a note. They make no network requests, write no files and read no credentials.
- Policies: [privacy](https://bolta.ai/privacy-policy), [terms](https://bolta.ai/tos), [support](https://bolta.ai/support).

## Limits you should know about

These are properties of the Bolta tools as of this release, verified against the server code. The skills state them to you where they matter.

- **One connection is one workspace.** An agency adds one connector per client, names it after the client and keeps "bolta" in the name (for example `claude mcp add --transport http bolta-acme https://mcp.bolta.ai/mcp`) so the safety prompts still apply. There is no cross-client view.
- **No media upload.** Claude can attach a public https image or video URL you provide. Local files and images generated in the conversation cannot be attached from here; use the Bolta dashboard library.
- **Comments on your own posts are not listed.** Paste the comment's link and Claude drafts a reply with Bolta's writer. Replies need a Premium plan.
- **Standard team posts cannot be rejected from here,** only routine drafts. Claude will say so and point you to the Hub. It never deletes a post as a stand-in.
- **Per-account publish results are not visible.** A post can show as Published although one platform failed. Claude compares what it intended with what it can see and says when it cannot tell.
- **No audit trail.** Claude cannot show who approved a post or when. For regulated records use the Bolta dashboard.
- **Voice context is rules, not examples** (tone, persona, dos and donts). Bolta's own drafting learns from your edits and approvals better than pasted-in text does.
- **Times are wall clock in the workspace timezone** and publishing lands within a few minutes of them. If the workspace timezone is still the UTC default, Claude asks once.
- **Approving a post Claude wrote** schedules it; the plugin always passes an explicit schedule mode so your confirmed time is used.
- **A WordPress Draft in Bolta means nothing exists on your site yet;** scheduling or publishing makes a live post.
- **Hooks need `sh`.** macOS, Linux and WSL are fine; native Windows needs Git Bash. If a hook cannot run, the confirmation prompt is silently absent, so the first time you approve something, check that the prompt actually appears.

## Troubleshooting

- **"Invalid API key", "API key expired" or "API key inactive":** the connection has lapsed. Claude Code: run `/mcp`, select the server and sign in again. Cowork and chat: disconnect and reconnect the Bolta connector. Claude will not retry the call.
- **Two Bolta servers listed:** you also have the Bolta connector enabled on your account. Keep one.
- **A prompt says "Confirmation needed" and Claude then stops:** that is the plugin's check, not an error from Bolta. Say yes to continue, or ask for something else.
- **An account will not connect inside Claude:** connecting social accounts happens in the browser. Ask Claude for the connect link, and make sure the right workspace is selected in Bolta first.

## Licence

MIT. See `LICENSE`.

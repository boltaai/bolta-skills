"""Generate the uiprompts cases that use the final "In your AI app" prompts (web PR #2661).

Re-run after the panel prompts change: python3 tools/ui_cases/gen_ui.py evals/claude-plugin/ui-final-prompts.md
(the rendered buildAiAppPrompt text: one "## <Brand>" section per world, "### Brand|Routine|Campaign" under it).
Each case copies a world's mocks from an existing ui-* case and swaps the prompt.
"""
import json, re, shutil, sys, pathlib
from evkit import EV, wrap, tool_used, regex, llm, setup_done

PROMPTS = pathlib.Path(sys.argv[1]).read_text()


def prompt(brand, kind):
    sec = PROMPTS.split(f"## {brand}")[1].split("\n## ")[0]
    body = sec.split(f"### {kind}")[1].split("\n### ")[0]
    lines = [l for l in body.split("\n")[1:] if l.strip()]
    return "\n\n".join(lines).strip()


def quote(text):
    return "\n".join("> " + l if l else ">" for l in text.split("\n"))


def convo(turns, now):
    out = ["This conversation so far:", ""]
    for who, text in turns:
        out += [f"**{who}:**", quote(text), ""]
    out += ["**Me now:**", now]
    return "\n".join(out)


SKILL = """  - name: skill-fired
    # The Bolta skill owns this ask.
    type: 'tool_used'
    tool: 'Skill'
    input_match: '"skill"\\s*:\\s*"(?:[\\w-]+:)?(bolta)"'
    min: 1
"""
PUBLIC = regex("nothing-public", r'"name"\s*:\s*"mcp__plugin_bolta_bolta__(publish-post|schedule-post|approve-post|approve-many-posts|activate-routine|resume-routine|run-routine-now|set-content-campaign-status|voice-generate)"',
               "Nothing published, scheduled, approved, switched on, run or started.", target="trace", match="not_contains")
NOIDS = regex("no-ids", r'(?<![/=])\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b|(?<![/=])\b(linkedin_org|facebook_page)_\d+',
              "No ids in what the user reads (ids inside a Bolta link are fine).", flags="i", match="not_contains")
PLAIN = regex("plain-words", r'\b(MCP|workspace_id|proposal_id|source_bindings?|approval_policy|review_every_artifact|extract-business-dna|create-voice-profile|update-voice-profile|confirm-plan|create-routine|activate-routine|plan-campaign|get-connect-link|list-routine-templates|switch_on|is_default|replace_voice|writing_samples)\b',
              "No tool names or internal field names in what the user reads.", match="not_contains")
TWOQ = regex("at-most-two-questions", r'(?:^(?![ \t]*>)[^\n]*\?(?=[\s*_)\]]|$)[^\n]*(?:\n|$)[\s\S]*?){3}',
              "At most 2 lines asking the user something. Lines quoted with > (a sample post) are not questions to the user.", flags="m", match="not_contains")
SAVES = r'"name"\s*:\s*"mcp__plugin_bolta_bolta__(save-post|bulk-create-posts|create-post|create-routine|confirm-plan|create-content-campaign|create-voice-profile|update-voice-profile|update-business-dna)"'
NOSAVE = regex("nothing-saved", SAVES, "A preview or a question, not a save.", target="trace", match="not_contains")
NO_SETUP = tool_used("no-setup-yet", "extract-business-dna", r'^(?![\s\S]*"(?:preview|check)"\W{1,6}true)', 0, 0,
                     "Only a preview (or a status check) before the yes: never a setup or a saving read.")
BASED_ON = regex("says-what-its-based-on", r"based on|from (what|everything) you('ve)? (told|said|shared)|from our chats|what I know|from what I (know|have)|here'?s what I (found|know|have)",
                 "Owner: show what the plan or setup is based on before it.", flags="i")


def case(name, src, description, expected, prompt_text, graders, mocks=None, drop_mocks=(), timeout=480):
    d = EV / name
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(EV / src / "mocks", d / "mocks")
    for m in drop_mocks:
        (d / "mocks" / "bolta" / f"{m}.md").unlink(missing_ok=True)
    for tool, (data, step) in (mocks or {}).items():
        (d / "mocks" / "bolta" / f"{tool}.md").write_text(wrap(data, step))
    y = ['schema_version: "1.1"', f"name: {name}", f"description: {json.dumps(description)}", "tags: [uiprompts]",
         f"expected_outcome: {json.dumps(expected)}", "execution:", "  prompt: |"]
    y += ["    " + l if l else "" for l in prompt_text.split("\n")]
    y += [f"  max_turns: 25", f"  timeout_seconds: {timeout}", "  allowed_tools: [Skill, Read]", "graders:"]
    (d / "case.yaml").write_text("\n".join(y) + "\n" + SKILL + "".join(g.rstrip("\n") + "\n" for g in graders))


HARBOR_PREVIEW = {
    "success": True, "preview": True, "saved": False,
    "dna_preview": {
        "name": "Harbor Physio", "tagline": "Get back to what you love.", "logo_url": "", "colors": ["#0E4D64", "#F4A261"],
        "fonts": ["Lato"], "visual_aesthetics": ["bright clinic photos"], "brand_images": [],
        "business_overview": "Harbor Physio is a physiotherapy clinic in Williamstown, Melbourne: sports injuries, back and neck pain, post-surgery rehab and small-group Pilates, with physios Anna Ruiz and Tom Hale. Book online; open Monday to Saturday.",
        "website_url": "https://harborphysio.example",
        "dos": ["Explain the cause in plain words before the fix", "Encourage people to keep moving"],
        "donts": ["Medical jargon without explaining it"],
        "tone_constraints": ["Plain words"], "brand_values": ["Movement is medicine"], "tone_of_voice": ["warm", "encouraging", "plain"],
    },
    "would_update_existing": False,
}
PREVIEW_STEP = "Nothing is saved yet. Show the user what Bolta read. On a yes, call extract-business-dna with setup=true and the same url: it sets up the Business DNA and the voice the way bolta.ai does."

HARBOR_CHAT = [("Me", "Quick one before Bolta: I'm Anna Ruiz and I run Harbor Physio in Williamstown. Most of our people are weekend runners, tradies and new mums getting back to exercise. We do sports massage, rehab plans and small-group Pilates. I write short and plain, like a friendly coach, never like a medical brochure, and I hate hashtag walls."),
               ("You", "Got it, Anna: Harbor Physio, Williamstown, for weekend runners, tradies and new mums; sports massage, rehab plans and small-group Pilates; short, plain, friendly-coach writing, no hashtag walls.")]
HARBOR_SITE_CHAT = [("Me", HARBOR_CHAT[0][1] + " Our site is harborphysio.example."), ("You", HARBOR_CHAT[1][1] + " Site: harborphysio.example.")]


def build():
    dev_brand, harbor_brand = prompt("DevConsole", "Brand"), prompt("Harbor Physio", "Brand")
    dev_routine, harbor_routine = prompt("DevConsole", "Routine"), prompt("Harbor Physio", "Routine")
    dev_campaign = prompt("DevConsole", "Campaign")
    ferro_brand = dev_brand.replace("DevConsole", "Ferro Bikes").replace("devconsole.example", "ferrobikes.example")
    SETUP = r'"setup"\W{1,6}true'

    # B1 DevConsole: site known, accounts connected -> preview only.
    src = EV / "ui-brand-site-preview" / "case.yaml"
    g = src.read_text().split("\ngraders:\n")[1]
    g = "".join(b for b in re.split(r"(?m)^(?=  - name: )", g) if b and not b.startswith("  - name: skill-fired"))
    case("ui-final-brand-site-preview", "ui-brand-site-preview",
         "The final Brand prompt (web #2661) for DevConsole, site on file, LinkedIn and X connected: preview only, the five parts, accounts named, asks before saving.",
         "bolta fires; extract-business-dna preview true; nothing saved; five parts; assumptions; accounts named; asks before saving.",
         dev_brand, [g, TWOQ])

    # B2 DevConsole save after the preview -> setup:true once, no separate voice.
    src = (EV / "ui-brand-site-save" / "case.yaml").read_text()
    you = src.split("**You:**\n")[1].split("\n\n    **Me now:**")[0]
    you = "\n".join(l[4:] if l.startswith("    ") else l for l in you.split("\n"))
    you = "\n".join(l[2:] if l.startswith("> ") else ("" if l == ">" else l) for l in you.split("\n"))
    g = src.split("\ngraders:\n")[1]
    g = "".join(b for b in re.split(r"(?m)^(?=  - name: )", g) if b and not b.startswith("  - name: skill-fired"))
    case("ui-final-brand-site-save", "ui-brand-site-save",
         "After the final Brand prompt's preview, DevConsole says save: one setup with the site, no separate voice, accounts named, Brand page link.",
         "bolta fires; one extract-business-dna setup:true; no create-voice-profile; names LinkedIn/X; Bolta link.",
         convo([("Me", dev_brand), ("You", you.strip())], "Looks good, save it."), [g])

    # B3 Ferro Bikes: nothing connected -> connect link FIRST in the reply, then the preview.
    src = (EV / "ui-brand-web-preview-noaccount" / "case.yaml").read_text()
    g = src.split("\ngraders:\n")[1]
    g = "".join(b for b in re.split(r"(?m)^(?=  - name: )", g) if b and not b.startswith("  - name: skill-fired"))
    case("ui-final-brand-connect-first", "ui-brand-web-preview-noaccount",
         "The final Brand prompt for Ferro Bikes with nothing connected: the connect link leads the reply, before the preview.",
         "bolta fires; get-connect-link; the link appears before the positioning; preview only; nothing saved.",
         ferro_brand, [g, regex("connect-link-first", r'^(?:(?!positioning|products?\b|writing rules|sample post)[\s\S]){0,700}bolta\.ai/dashboard/account/socials',
                                "Owner: the connect link comes first, before the brand preview.", flags="i"), TWOQ])

    harbor_src = "ui-brand-site-notes-save"   # Harbor world: Starter Voice, Instagram + Facebook.
    nodna = {"list-business-dna": ({"success": True, "dnas": [], "count": 0}, None)}

    # B4 (a) the site is in the history -> used as a finding, previewed, never re-asked.
    case("ui-final-brand-site-in-history", harbor_src,
         "Final no-site Brand prompt for Harbor Physio, but the user named the site earlier in the chat: the AI shows it as a finding and previews it, never asks for it.",
         "bolta fires; extract-business-dna preview with harborphysio.example; no website question; nothing saved.",
         convo(HARBOR_SITE_CHAT, harbor_brand),
         [tool_used("previews-the-site", "extract-business-dna", r'harborphysio\.example[\s\S]*"preview"\W{1,6}true|"preview"\W{1,6}true[\s\S]*harborphysio\.example', 1, None, "The site from the history, previewed."),
          NO_SETUP, NOSAVE, PUBLIC,
          regex("does-not-ask-for-site", r"(what'?s|what is|share|send|have)[^?\n]{0,40}(your|a) (web)?site[^?\n]{0,60}\?", "The site was already given: never asked again.", flags="i", match="not_contains"),
          regex("shows-findings", r"runners|tradies|new mums", "Shows what it knows from the chat.", flags="i"),
          TWOQ, NOIDS, PLAIN],
         mocks={"extract-business-dna": (HARBOR_PREVIEW, PREVIEW_STEP), **nodna})

    # B5 (b) no site in the history -> findings shown, the website asked once, nothing read or saved.
    case("ui-final-brand-asks-site", harbor_src,
         "Final no-site Brand prompt for Harbor Physio; the chat has the business but no site: findings shown, the website asked once (with the no-site option), nothing read or saved.",
         "bolta fires; shows findings; asks for the website once; no extract-business-dna setup or save; no voice saved.",
         convo(HARBOR_CHAT, harbor_brand),
         [tool_used("no-site-guessed", "extract-business-dna", None, 0, 0, "No site known: never guess one."),
          NOSAVE, PUBLIC,
          regex("shows-findings", r"runners|tradies|new mums", "Shows what it knows from the chat.", flags="i"),
          regex("asks-for-website", r"web ?site[^?\n]{0,120}\?|\?[^\n]{0,40}web ?site", "Asks for the website.", flags="i"),
          regex("offers-no-site-path", r"(don'?t|do not|no) (have )?(one|a (web)?site)|without (one|a (web)?site)|if (there'?s|you have) no", "Says it can build it without one.", flags="i"),
          TWOQ, NOIDS, PLAIN],
         mocks=nodna)

    findings_reply = ("From our chats: you run Harbor Physio in Williamstown, for weekend runners, tradies and new mums; "
                      "you do sports massage, rehab plans and small-group Pilates; you write short and plain, like a friendly coach, no hashtag walls. "
                      "Right? What's your website? If you don't have one, I'll build it from what you've told me.")
    # B6 (c) "we don't have one" -> preview built from the findings, nothing invented, nothing saved yet.
    case("ui-final-brand-no-website", harbor_src,
         "Harbor Physio has no website: the brand is previewed from the chat findings alone, with nothing invented, and nothing saved before a yes.",
         "bolta fires; no extract-business-dna; nothing saved; a preview from the findings; no invented facts; asks before saving.",
         convo(HARBOR_CHAT + [("Me", harbor_brand), ("You", findings_reply)], "That's right. We don't have a website."),
         [tool_used("no-site-guessed", "extract-business-dna", None, 0, 0, "No website: never read or guess one."),
          NOSAVE, PUBLIC,
          regex("asks-before-saving", r"(save|set (it )?up|go ahead)[^?\n]{0,80}\?", "Preview first; asks before saving.", flags="i"),
          llm("nothing-invented", "The user, Anna Ruiz, runs Harbor Physio (Williamstown), for weekend runners, tradies and new mums, offering sports massage, rehab plans and small-group Pilates, and writes short and plain like a friendly coach, no hashtag walls. They have no website. PASS if the reply previews a brand profile built only from these facts (a sample post may illustrate the voice but must not state new facts such as prices, opening hours, years in business, awards, other staff or services) and saves nothing yet. FAIL if it states any business fact the user did not give, or invents a website."),
          TWOQ, NOIDS, PLAIN],
         mocks=nodna)

    # B7 (c, save) the manual preview approved -> the thin Starter Voice filled from the findings; colours asked once.
    manual_preview = ("Here's your brand from what you told me. Nothing is saved yet.\n\n**Positioning:** a Williamstown physio clinic that gets weekend runners, tradies and new mums moving again.\n"
                      "**Services:** sports massage, rehab plans, small-group Pilates.\n**Writing rules** DO: short and plain, like a friendly coach · DON'T: medical-brochure language · hashtag walls\n"
                      "**Topics:** keeping runners running · desk-to-tools recovery for tradies · getting back to exercise after a baby.\n"
                      "**Sample post:** \"Long run left your calves tight? Two easy moves tonight, and when it's time to see Anna.\"\n\n"
                      "**Assumptions:** the topics are mine. A website would add your opening hours and booking link.\n\nSave this to Harbor Physio?")
    case("ui-final-brand-no-website-save", harbor_src,
         "Harbor Physio (no website, no voice yet) approves the brand built from chat: Bolta's setup with no url from their words (no website guessed, no separate voice), the accounts named, and colours, fonts or a logo asked once.",
         "bolta fires; one extract-business-dna setup:true with no url and notes from the chat; no create-voice-profile; asks once for colours or a logo; names the accounts.",
         convo(HARBOR_CHAT + [("Me", harbor_brand), ("You", findings_reply), ("Me", "That's right. We don't have a website."), ("You", manual_preview)], "Looks good, save it."),
         [tool_used("sets-up-without-site", "extract-business-dna", r'^(?![\s\S]*"url"\s*:\s*"[^"])(?=[\s\S]*"setup"\W{1,6}true)', 1, 1, "Bolta-Server #1482: no website, so setup:true with no url, from their words."),
          tool_used("notes-from-chat", "extract-business-dna", r'"notes"\s*:\s*"[^"]*(runners|tradies|mums|Pilates|massage)', 1, None, "Their words as notes."),
          tool_used("no-site-guessed", "extract-business-dna", r'"url"\s*:\s*"[^"]', 0, 0, "No website: never a guessed url."),
          tool_used("no-separate-voice", "create-voice-profile", None, 0, 0, "The setup makes the voice."),
          PUBLIC,
          regex("asks-visuals-once", r"(colou?rs?|fonts?|logo)[^?\n]{0,160}\?", "Owner: no site means no colours, fonts or logo; asked once, optionally.", flags="i"),
          regex("names-voice-accounts", r"(Instagram|Facebook)", "Names the accounts that use the voice.", flags="i"),
          NOIDS, PLAIN],
         mocks={**nodna, "extract-business-dna": setup_done("5a1d0000-0000-4000-8000-0000000000a2", "Harbor Physio", "",
                  "d7a00000-0000-4000-8000-0000000000b2", "9b000000-0000-4000-8000-0000000000b2", "Harbor Physio",
                  "Weekend runners, tradies and new mums getting back to exercise", ["runner niggles", "tradies' backs", "exercise after a baby"],
                  ["plain", "friendly", "coach-like"], ["ac000000-0000-4000-8000-0000000000a1", "facebook_page_5512098834"],
                  ["Sports massage", "Rehab plans", "Small-group Pilates"], ["Turn on Topic insights", "Add inspiration (favorite creators)"],
                  ["Add brand colors or fonts"], 2, without_website=["colors", "fonts", "logo", "tagline"])})

    # B9 colours after a no-site setup: pasted hex codes saved exactly; B10 none given: nothing invented.
    saved_reply = ("Harbor Physio is set up from what you told me: about your business, your three services, and your voice "
                   "(short and plain, like a friendly coach, for weekend runners, tradies and new mums); your Instagram and Facebook use it. "
                   "Voice setup 82%, business 80%. A website would add your colours, fonts and more detail; share it any time and it only fills gaps.\n\n"
                   "Have brand colours, fonts or a logo? Paste them, or share an image of your logo.")
    dna = {"success": True, "dnas": [{"id": "d7a00000-0000-4000-8000-0000000000b2", "name": "Harbor Physio", "website_url": "", "tagline": "",
            "business_overview": "Harbor Physio in Williamstown for weekend runners, tradies and new mums: sports massage, rehab plans and small-group Pilates.",
            "colors": [], "fonts": [], "logo_url": "", "visual_aesthetics": [], "is_default": True}], "count": 1}
    upd = {"success": True, "dna": {**dna["dnas"][0], "colors": ["#0E4D64", "#F4A261"], "fonts": ["Lato"]},
           "dashboard_url": "https://bolta.ai/dashboard/knowledge-base?tab=overview&workspaceId=5a1d0000-0000-4000-8000-0000000000a2&ref=claude_link"}
    hist = HARBOR_CHAT + [("Me", harbor_brand), ("You", findings_reply), ("Me", "That's right. We don't have a website."),
                          ("You", manual_preview), ("Me", "Looks good, save it."), ("You", saved_reply)]
    case("ui-final-brand-colours-pasted", harbor_src,
         "After a no-site setup the user pastes two hex codes and a font: saved exactly as given on the brand's record, nothing else changed.",
         "bolta fires; update-business-dna with colors exactly #0E4D64 and #F4A261 and fonts Lato; no other write.",
         convo(hist, "Our colours are #0E4D64 and #F4A261, and we use Lato."),
         [tool_used("saves-colours-exactly", "update-business-dna", r'"colors"\s*:\s*\[\s*"#0E4D64"\s*,\s*"#F4A261"\s*\]', 1, None, "Hex codes saved as given."),
          tool_used("saves-font", "update-business-dna", r'"fonts"\s*:\s*\[\s*"Lato"\s*\]', 1, None, "The font as given."),
          regex("no-other-writes", r'"name"\s*:\s*"mcp__plugin_bolta_bolta__(extract-business-dna|create-voice-profile|update-voice-profile|save-post|create-routine|confirm-plan)"', "Only the visuals change.", target="trace", match="not_contains"),
          PUBLIC, NOIDS, PLAIN],
         mocks={"list-business-dna": (dna, None), "update-business-dna": (upd, None)})
    case("ui-final-brand-no-colours", harbor_src,
         "After a no-site setup the user has no colours, fonts or logo: nothing saved, nothing invented, and where to add them later said once.",
         "bolta fires; no update-business-dna; no colour or font invented; says they can add them later.",
         convo(hist, "No, nothing like that yet."),
         [tool_used("saves-nothing", "update-business-dna", None, 0, 0, "Nothing given, nothing saved."),
          regex("no-invented-hex", r'#[0-9A-Fa-f]{6}\b', "Never invents a colour.", match="not_contains"),
          regex("says-later", r"later|any ?time|Brand page|when you (have|do)|whenever", "Says they can add them later.", flags="i"),
          regex("does-not-ask-again", r"(colou?rs?|fonts?|logo)[^?\n]{0,120}\?", "Asked once already: not again.", flags="i", match="not_contains"),
          PUBLIC, NOIDS, PLAIN],
         mocks={"list-business-dna": (dna, None), "update-business-dna": (upd, None)})

    # B8 (d) a finding corrected -> the correction is used.
    corrected = convo(HARBOR_SITE_CHAT + [("Me", harbor_brand),
                      ("You", "From our chats: you run Harbor Physio in Williamstown, for weekend runners, tradies and new mums; you do sports massage, rehab plans and small-group Pilates; you write short and plain; your site is harborphysio.example. Right?")],
                      "Nearly. We stopped the rehab plans in October; it's sports massage and Pilates now. The rest is right.")
    case("ui-final-brand-correction", harbor_src,
         "The user corrects a finding (no more rehab plans): the preview and anything passed on use the correction.",
         "bolta fires; preview of harborphysio.example; nothing saved; rehab plans never offered as a current service.",
         corrected,
         [tool_used("previews-the-site", "extract-business-dna", r'"preview"\W{1,6}true', 1, None, "The site from the history."),
          NO_SETUP, NOSAVE, PUBLIC,
          llm("uses-the-correction", "The user said Harbor Physio stopped offering rehab plans in October and now offers sports massage and Pilates. PASS if the reply's preview lists the services as sports massage and Pilates (and anything the website read adds, if it marks rehab as no longer offered or leaves it out), and does not present rehab plans as a current service the user offers. FAIL if rehab plans appear as a current service in the positioning, products or sample post."),
          TWOQ, NOIDS, PLAIN],
         mocks={"extract-business-dna": (HARBOR_PREVIEW, PREVIEW_STEP), **nodna})

    # R1 existing brand: a running routine and a strong post type -> the plan builds on them, no duplicate.
    rsrc = "ui-routine-recommend-preview"
    running = {"routines": [{"id": "e5000000-0000-4000-8000-0000000000aa", "name": "Release notes", "status": "active",
                             "template_key": "weekly_social_posts", "goal": "A LinkedIn post about each week's release",
                             "schedule": {"interval": "weekly", "day": "friday", "time": "10:00"}, "timezone": "America/Los_Angeles",
                             "next_run_at": "2026-11-13T10:00:00-08:00", "accounts": ["DevConsole (company page)"]}], "count": 1, "total": 1}
    case("ui-final-routine-builds-on", rsrc,
         "Final Routine prompt for DevConsole, which already runs a weekly Release notes routine: says what the plan is based on (the brand in Bolta and what's running), passes it as context, never proposes Release notes again.",
         "bolta fires; reads routines; plan recommend with context; a based-on line; Release notes named as already running, not proposed; nothing saved.",
         dev_routine,
         [regex("reads-routines", r'"name"\s*:\s*"mcp__plugin_bolta_bolta__list-routines"', "What's already running.", target="trace"),
          tool_used("plans-with-context", "plan", r'"context"\s*:\s*"[^"]{20,}', 1, None, "Owner: what Bolta holds and what they said, passed as context."),
          BASED_ON,
          regex("names-running", r"release notes[^.\n]{0,120}(already|running|keep|on)|(already|running)[^.\n]{0,120}release notes", "Says Release notes is already running.", flags="i"),
          regex("no-duplicate", r"(?:^|\n)\s*(\*\*)?\d[.)]\s*(\*\*)?release notes", "Never proposes the running routine again.", flags="i", match="not_contains"),
          NOSAVE, PUBLIC, TWOQ, NOIDS, PLAIN],
         mocks={"list-routines": (running, None)})

    # R2 no details in the prompt, the history has them -> the plan reflects the history, nothing invented.
    harbor_rsrc = "ui-routine-instagram-preview"
    case("ui-final-routine-from-history", harbor_rsrc,
         "Final Routine prompt for Harbor Physio with no details; the earlier chat has the audience, services, review time (about 3 a week) and a dislike: the plan's context and the reply carry them, nothing invented.",
         "bolta fires; plan recommend with context naming runners/tradies and 3 a week; a based-on line; sized to about 3 drafts a week; nothing saved; no invented facts.",
         convo(HARBOR_CHAT + [("Me", "I can review about 3 posts a week, max."), ("You", "Noted: about 3 drafts a week to review.")], harbor_routine),
         [tool_used("context-from-history", "plan", r'"context"\s*:\s*"[^"]*(runners|tradies|mums)', 1, None, "The history's facts reach the planner."),
          tool_used("review-time-in-context", "plan", r'"context"\s*:\s*"[^"]*(\b3\b|three)', 1, None, "Their review time reaches the planner."),
          BASED_ON, NOSAVE, PUBLIC, TWOQ,
          llm("reflects-history", "Earlier in the chat the user (Anna Ruiz) said: Harbor Physio, Williamstown; clients are weekend runners, tradies and new mums; services are sports massage, rehab plans and small-group Pilates; short, plain friendly-coach writing, no hashtag walls; they can review about 3 posts a week. PASS if the recommended routines are about these clients and services, total about 3 drafts a week or fewer, and the reply states no business fact that neither the user nor Bolta's brand record gave (the record holds: physios Anna Ruiz and Tom Hale, online booking, health-fund rebates on the spot, open Monday to Saturday, sports injuries, back and neck pain, post-surgery rehab, Pilates; anything else, such as prices or awards, is invented). FAIL if it ignores these facts, plans well over 3 drafts a week without saying why, or invents a business fact. (Grader fix: the first version counted the brand record's own facts as invented.)"),
          NOIDS, PLAIN])

    # C1 campaign with no event anywhere -> one question.
    csrc = "ui-campaign-ask"
    g = (EV / csrc / "case.yaml").read_text().split("\ngraders:\n")[1]
    g = "".join(b for b in re.split(r"(?m)^(?=  - name: )", g) if b and not b.startswith("  - name: skill-fired"))
    case("ui-final-campaign-ask", csrc,
         "Final Campaign prompt for DevConsole with no event in the chat: one question, which launch and when; nothing saved.",
         "bolta fires; asks which launch and when in one question; nothing saved.", dev_campaign, [g])

    # C2 the event and date are in the history -> no re-ask; planned with context.
    case("ui-final-campaign-date-in-history", "ui-campaign-outline",
         "Final Campaign prompt for DevConsole; earlier in the chat the user said DevConsole 2.0 launches Tue Dec 8 with a page: planned with that as context, never asked again.",
         "bolta fires; plan campaign with context naming Dec 8; never asks which event or when; outline shown; nothing saved.",
         convo([("Me", "Heads up: DevConsole 2.0 launches Tuesday Dec 8. The page is devconsole.example/2. Main thing is the new Request Replay diff view."),
                ("You", "Noted: DevConsole 2.0 on Tue Dec 8, page devconsole.example/2, headline feature the Request Replay diff view.")], dev_campaign),
         [tool_used("plans-campaign", "plan", r'"kind"\s*:\s*"campaign"', 1, None, "One campaign plan."),
          tool_used("date-in-context", "plan", r'Dec(ember)?\W{0,3}8|12[-/]08|2026-12-08', 1, None, "The date from the history reaches the planner."),
          regex("no-reask", r"(which|what) (launch|event)[^?\n]{0,80}\?|when (is|does)[^?\n]{0,60}\?|what date[^?\n]{0,60}\?", "The date was given: never asked again.", flags="i", match="not_contains"),
          BASED_ON, NOSAVE, PUBLIC, TWOQ, NOIDS, PLAIN])

    # S1 start with nothing connected -> connect link first, with why.
    case("ui-start-connect-first", "ui-brand-web-preview-noaccount",
         "Set me up with nothing connected: the connect link is in the opening lines with why, before the brand and the routines.",
         "bolta fires; get-connect-link; the link in the first lines with a why; nothing saved or public.",
         "Set me up on Bolta. We're Ferro Bikes, ferrobikes.example.",
         [tool_used("connect-link", "get-connect-link", None, 1, None, "Nothing connected: the link, unasked."),
          regex("connect-link-first", r'^(?:(?!positioning|routine)[\s\S]){0,700}bolta\.ai/dashboard/account/socials', "Owner: connect an account FIRST, before brand and routines.", flags="i"),
          regex("says-why", r"(drafts?|posts?)[^.\n]{0,80}(somewhere|go|need)|learns? from|voice[^.\n]{0,60}(learn|account)", "One line of why.", flags="i"),
          NO_SETUP, NOSAVE, PUBLIC, TWOQ, NOIDS, PLAIN],
         timeout=540)

    # S2 start: the launch question asked proactively.
    case("ui-start-campaign-question", "ui-routine-recommend-preview",
         "Get me going on an existing brand (accounts and voice set): routines proposed, and ONE question about a launch, sale or event asked unprompted.",
         "bolta fires; routines proposed from the planner; a launch/sale/event question; at most 2 questions; nothing saved.",
         "Get DevConsole going on Bolta. I want this to run itself as much as possible.",
         [regex("plans-routines", r'"name"\s*:\s*"mcp__plugin_bolta_bolta__(plan|list-routine-templates)"', "Routines proposed.", target="trace"),
          regex("asks-about-launch", r"(launch|sale|event|promotion|webinar|release)[^?\n]{0,160}\?", "Owner: one proactive question about something dated.", flags="i"),
          NOSAVE, PUBLIC, TWOQ, NOIDS, PLAIN])

    # V1 a person voice from samples pasted earlier -> created from them, as "I".
    posts = ['"Shipped the diff view at 1:40 am. Not proud of the hour, proud of the diff. If your replay ever lied to you, this is for you."',
             '"Three things I got wrong about logging: I logged everything, I logged nothing useful, and I never logged the request body. Fixed all three."']
    case("ui-voice-founder-from-samples", "ui-routine-recommend-preview",
         "Earlier the founder pasted two of her posts and confirmed the findings; she says save. Her person voice is made from those posts (her own words as the sample), writing as I, not the default, on her X.",
         "bolta fires; create-voice-profile with a pasted post as writing_sample, speaker_mode founder, not default; no website read; nothing public.",
         convo([("Me", "Here are two posts I wrote on X:\n" + "\n".join(posts)),
                ("Me", "Make a voice for me (Maya, founder) for my X, separate from the DevConsole voice."),
                ("You", "From your two posts: short lines, first person, a specific hour or number up front, dry self-deprecation, no hashtags. It would write as \"I\" on your X and leave the DevConsole voice as the default. Right?")],
               "Yes, that's me. Save it."),
         [tool_used("makes-person-voice", "create-voice-profile", None, 1, 1, "One person voice."),
          tool_used("her-words-as-sample", "create-voice-profile", r'"writing_sample"\s*:\s*"[^"]*(diff view|logged everything|1:40)', 1, None, "Her pasted post, never one written for her."),
          tool_used("writes-as-i", "create-voice-profile", r'"speaker_mode"\s*:\s*"founder"', 1, None, "A founder writing as I."),
          tool_used("not-default", "create-voice-profile", r'"is_default"\W{1,6}true', 0, 0, "The brand voice stays the default."),
          tool_used("no-site-read", "extract-business-dna", None, 0, 0, "A person voice reads no website."),
          PUBLIC, NOIDS, PLAIN])


build()
print("generated")

# Harbor Physio with no website: nothing in its world may carry the site or a business record.
for c in ("ui-final-brand-asks-site", "ui-final-brand-no-website", "ui-final-brand-no-website-save"):
    mb = EV / c / "mocks" / "bolta"
    for f in ("update-business-dna.md", "get-voice-profile.md", "update-voice-profile.md") + (() if c.endswith("-save") else ("extract-business-dna.md",)):
        (mb / f).unlink(missing_ok=True)
    # No voice yet (as a brand with no website and no setup has): Lumen's no-voice world, renamed.
    lumen = EV / "ui-brand-notes-save" / "mocks" / "bolta"
    for f in ("get-voice-context.md", "create-voice-profile.md"):
        t = (lumen / f).read_text().replace("Lumen Dental Studio", "Harbor Physio").replace("5a1d0000-0000-4000-8000-0000000000c4", "5a1d0000-0000-4000-8000-0000000000a2")
        t = t.replace('"facebook_page_7731904456"', '"facebook_page_5512098834"').replace("facebook_page_7731904456", "facebook_page_5512098834")
        (mb / f).write_text(t)
    for f in ("create-voice-profile.md",):
        t = (mb / f).read_text()
        t = t.replace('"business_dna_id": "d7a00000-0000-4000-8000-0000000000a2"', '"business_dna_id": null').replace("https://harborphysio.example", "").replace("harborphysio.example", "")
        (mb / f).write_text(t)

# Harbor Physio's planner answers a recommendation (the copied world's plan is one Instagram routine).
src = (EV / "ui-routine-recommend-preview" / "mocks" / "bolta" / "plan.md").read_text()
head, body = src[:src.find("{")], json.loads(src[src.find("{"):])
IG, FB = "ac000000-0000-4000-8000-0000000000a1", "facebook_page_5512098834"
spec = [("Runner niggles", "Easy fixes for weekend runners' niggles", ["instagram"], [IG], "tuesday", "07:30", "Runners are your biggest group."),
        ("Back on the tools", "Looking after backs and shoulders for tradies", ["facebook"], [FB], "thursday", "06:30", "Tradies read Facebook before work."),
        ("Back to exercise", "Getting back to exercise after a baby", ["instagram"], [IG], "saturday", "09:00", "New mums are a group you named.")]
plans = []
for i, (name, goal, plats, accs, day, time, why) in enumerate(spec):
    p = json.loads(json.dumps(body["data"]["plans"][i]))
    p["payload"].update({"name": name, "goal": goal, "schedule": {"interval": "weekly", "days": [day], "time": time},
                         "timezone": "Australia/Melbourne", "output_config": {"artifact_type": "post", "count": 1, "platforms": plats},
                         "account_ids": accs, "voice_profile_id": "9b000000-0000-4000-8000-0000000001a2"})
    p["display"] = {"title": name, "summary": why}
    p["why"] = why
    plans.append(p)
body["data"]["plans"] = plans
body["data"]["skipped"] = []
(EV / "ui-final-routine-from-history" / "mocks" / "bolta" / "plan.md").write_text(head + json.dumps(body, indent=2) + "\n")

# Mocks a world lacks for the calls its new case makes.
for f in ("plan.md", "revise-plan.md", "confirm-plan.md", "_data"):
    s, d = EV / "ui-routine-missing-account" / "mocks" / "bolta" / f, EV / "ui-start-connect-first" / "mocks" / "bolta" / f
    (shutil.copytree if s.is_dir() else shutil.copy)(s, d)
shutil.copy(EV / "ui-brand-site-save" / "mocks" / "bolta" / "create-voice-profile.md", EV / "ui-voice-founder-from-samples" / "mocks" / "bolta" / "create-voice-profile.md")
print("mocks added")

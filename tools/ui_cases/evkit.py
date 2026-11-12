"""Helpers for editing eval cases (text-level, keeps comments) and writing mocks."""
import json, re, pathlib, shutil

EV = pathlib.Path(__file__).resolve().parents[2] / 'evals' / 'claude-plugin'

def grader_blocks(text):
    i = text.index('\ngraders:\n') + len('\ngraders:\n')
    head, body = text[:i], text[i:]
    parts = re.split(r'(?m)^(?=  - name: )', body)
    return head, [p for p in parts if p]

def gname(block):
    return re.match(r'  - name: ([\w-]+)', block).group(1)

def edit_graders(case, drop=(), replace=None, add=()):
    p = EV / case / 'case.yaml'
    head, blocks = grader_blocks(p.read_text())
    replace = replace or {}
    out = []
    for b in blocks:
        n = gname(b)
        if n in drop:
            continue
        if n in replace:
            b = replace[n].rstrip('\n') + '\n'
        out.append(b)
    for a in add:
        out.append(a.rstrip('\n') + '\n')
    p.write_text(head + ''.join(out))

def set_field(case, key, value):
    p = EV / case / 'case.yaml'
    s = p.read_text()
    s, n = re.subn(rf"(?m)^{key}: .*$", f"{key}: {value}", s, count=1)
    assert n == 1, (case, key)
    p.write_text(s)

def wrap(data, next_step=None):
    return json.dumps({"ok": True, "data": data, "error": None, "error_kind": None, "meta": None,
                       "next_step": next_step}, indent=2, ensure_ascii=False) + "\n"

def write_mock(case, tool, data, next_step=None):
    (EV / case / 'mocks' / 'bolta' / f'{tool}.md').write_text(wrap(data, next_step))

def tool_used(name, tool, input_match=None, mn=None, mx=None, comment=None):
    s = f"  - name: {name}\n"
    if comment: s += f"    # {comment}\n"
    s += f"    type: 'tool_used'\n    tool: 'mcp__plugin_bolta_bolta__{tool}'\n"
    if input_match is not None: s += "    input_match: '" + input_match.replace("'", "''") + "'\n"
    if mn is not None: s += f"    min: {mn}\n"
    if mx is not None: s += f"    max: {mx}\n"
    return s

def regex(name, pattern, comment=None, target=None, flags=None, match=None):
    s = f"  - name: {name}\n"
    if comment: s += f"    # {comment}\n"
    s += "    type: 'regex'\n    pattern: '" + pattern.replace("'", "''") + "'\n"
    if target: s += f"    target: '{target}'\n"
    if flags: s += f"    flags: '{flags}'\n"
    if match: s += f"    match: '{match}'\n"
    return s

def llm(name, criteria, comment=None):
    s = f"  - name: {name}\n"
    if comment: s += f"    # {comment}\n"
    s += "    type: 'llm'\n    criteria: |\n" + ''.join('      ' + l + '\n' for l in criteria.strip().split('\n'))
    return s

SETUP_DONE_STEP = ("The brand is set up. Show the user what Bolta made (setup: the Business DNA, the voice, its "
    "language and topics, the products) and the two scores (setup.voice_setup, setup.business_setup, with what is "
    "missing), and the dashboard_url. Then call get-voice-context before writing. Changes go through "
    "update-voice-profile or update-business-dna.")
CONNECT_FIRST = ("FIRST: no social account is connected to this brand yet. Before anything else, offer "
    "get-connect-link (share the link; they connect in their browser), then list-accounts to check: drafts need an "
    "account to go to, and the voice learns from that account's own posts. Setting up without one still works; it "
    "just comes second. Then: ")

def setup_done(ws, brand, site, dna_id, voice_id, voice_name, audience, topics, tone, accounts, products,
               voice_missing, business_missing, connected, language="en"):
    vs = 100 - sum({"Give it documents to read": 15, "Assign an account": 10,
                    "Add inspiration (favorite creators)": 2, "Turn on Topic insights": 8}.get(m, 10) for m in voice_missing)
    bs = 100 - sum({"Add brand colors or fonts": 20, "Describe who you reach": 25,
                    "Add what you offer (products)": 30}.get(m, 25) for m in business_missing)
    data = {
        "mode": "setup", "status": "succeeded", "url": site, "dna_id": dna_id, "voice_profile_id": voice_id,
        "setup": {
            "business_dna": {"id": dna_id, "name": brand, "website_url": site, "tagline": "", "has_colors": True,
                             "has_fonts": True, "dos": 3, "donts": 2, "writing_samples": 0},
            "voice": {"id": voice_id, "name": voice_name, "is_default": True, "speaker_mode": "brand",
                      "language": language, "description": "", "voice_characteristics": "",
                      "target_audience": audience, "topics": topics, "tone_of_voice": tone, "dos": 4, "donts": 3,
                      "assigned_account_ids": accounts},
            "products": products, "social_accounts_in_brand": connected,
            "business_setup": {"score": bs, "missing": business_missing},
            "voice_setup": {"score": vs, "missing": voice_missing},
            "dashboard_url": f"https://bolta.ai/dashboard/knowledge-base?tab=voice-profiles&profile={voice_id}&workspaceId={ws}&ref=claude_link",
            "dashboard_url_shows": "this voice's editor on the Brand page. Tell the user to have the workspace named in dashboard_workspace_name open.",
            "dashboard_workspace_name": brand,
        },
        "social_accounts_connected": connected,
    }
    step = SETUP_DONE_STEP
    if voice_missing:
        step += (" If the user has already shared writing, notes, products or creators they like in this chat, run "
                 "setup=true again with the same url and those fields to fill what is missing. Never make them up.")
    if connected == 0:
        step = CONNECT_FIRST + step
    elif accounts:
        step += (" Its social accounts are assigned (assigned_account_ids); mention which, and offer "
                 "get-connect-link for any other network the user wants.")
    return data, step

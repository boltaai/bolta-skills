#!/usr/bin/env python3
"""Build tools/fixtures/coverage_keys.json: every capability the Bolta skill must teach.

"Every capability is in the skill" is a claim until something checks it. This
script reads the server (statically: ast and the MCP golden, never Django) and
writes one key per thing a caller can set, each with the literal token(s) that
must appear in plugins/bolta/skills/bolta/references/*.md. The coverage section
of tools/check_claude_plugin.py then fails for every key no reference teaches.

Groups:
  tool_param   brand setup (extract-business-dna), routine and campaign tool inputs (create/update-routine, plan,
               revise-plan changes, confirm-plan, create/update-content-campaign,
               set-content-campaign-status, analyze-content-campaign-source), save-post,
               publish-post, list-suggestions and decide-suggestion, recursively, with the enum values
               worth teaching. Where the golden schema is an opaque object
               (output_config, schedule, changes, content_mix) the keys come from
               the server's own validators and constants.
  post_details per-network fields save-post platform_details accepts
               (posts/post_details_api_v1_views.py derives them from the
               *PostDetails models: editable, non-system fields, FK _id aliases,
               many-to-many) and their closed-set choice values.
  platform_specific
               every platform_specific key the publishers read
               (posts/platform_specific.py, posts/tasks/publishing/*.py,
               pinterest_api_handler/media.py).
  tool         every MCP tool name in the golden.

Regenerate when the server changes (new tool, new parameter, new model field,
new publisher read), then commit the fixture with the skill change that teaches
the new keys:

    python3 -I tools/build_coverage_fixture.py [SERVER_PATH]
    python3 -I tools/check_claude_plugin.py --coverage-only

SERVER_PATH defaults to ~/Projects/GitHub/BOLT-SERVER/SERVER-release2. The
script exits non-zero when a source it expects yields nothing (a renamed file
or function would otherwise shrink the fixture and "prove" coverage vacuously).
"""

from __future__ import annotations

import ast
import json
import pathlib
import re
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
OUT = REPO / "tools" / "fixtures" / "coverage_keys.json"
DEFAULT_SERVER = pathlib.Path.home() / "Projects" / "GitHub" / "BOLT-SERVER" / "SERVER-release2"

# Tool -> id prefix. Tools sharing a prefix share keys (create and update take the same fields).
TOOL_PREFIX = {
    "create-routine": "routine",
    "update-routine": "routine",
    "plan": "plan",
    "revise-plan": "revise-plan",
    "confirm-plan": "confirm-plan",
    "create-content-campaign": "campaign",
    "update-content-campaign": "campaign",
    "set-content-campaign-status": "campaign-status",
    "analyze-content-campaign-source": "campaign-source",
    # Release 2's folded post tools and Bolta's suggestions
    "save-post": "save-post",
    "publish-post": "publish-post",
    "list-suggestions": "suggestions",
    "decide-suggestion": "decide-suggestion",
    # Brand setup: the website pipeline bolta.ai's first run uses (Bolta-Server #1482)
    "extract-business-dna": "brand-setup",
}
SKIP_PARAMS = {"workspace_id"}  # on every tool; the checker's universal param

PUBLISHER_SKIP = {"__init__.py", "base.py", "router.py", "utm.py", "env_guard.py", "all_platforms.py"}
NOT_CALLER_KEYS = {"accounts"}  # structure, not a setting (taught as platform_specific.accounts)

errors: list[str] = []


def fail(msg):
    errors.append(msg)


# --------------------------------------------------------------------------- #
# ast helpers
# --------------------------------------------------------------------------- #

_trees: dict[pathlib.Path, ast.Module] = {}


def tree(path: pathlib.Path) -> ast.Module:
    if path not in _trees:
        _trees[path] = ast.parse(path.read_text(), filename=str(path))
    return _trees[path]


def strs(node) -> list[str]:
    """String constants of a literal tuple/list/set/frozenset({...}) (Starred skipped)."""
    if isinstance(node, ast.Call) and getattr(node.func, "id", None) in ("frozenset", "set", "tuple") and node.args:
        return strs(node.args[0])
    if isinstance(node, (ast.Tuple, ast.List, ast.Set)):
        return [e.value for e in node.elts if isinstance(e, ast.Constant) and isinstance(e.value, str)]
    return []


def module_assign(mod: ast.Module, name: str):
    for node in mod.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == name for t in node.targets):
            return node.value
        if isinstance(node, ast.AnnAssign) and getattr(node.target, "id", None) == name:
            return node.value
    return None


def find_class(mod: ast.Module, name: str):
    return next((n for n in ast.walk(mod) if isinstance(n, ast.ClassDef) and n.name == name), None)


def find_func(mod: ast.Module, name: str):
    return next((n for n in ast.walk(mod) if isinstance(n, ast.FunctionDef) and n.name == name), None)


def module_const(path: pathlib.Path, name: str) -> list[str]:
    value = module_assign(tree(path), name)
    out = strs(value) if value is not None else []
    if not out:
        fail(f"{path.name}: constant {name} not found or empty")
    return out


def class_all(path: pathlib.Path, cls_name: str, attr: str = "ALL") -> list[str]:
    """Class.ALL = (A, B) where A = "a" are class attributes."""
    cls = find_class(tree(path), cls_name)
    if cls is None:
        fail(f"{path.name}: class {cls_name} not found")
        return []
    consts = {}
    target = None
    for node in cls.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            n = node.targets[0].id
            if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                consts[n] = node.value.value
            if n == attr:
                target = node.value
    out = []
    if isinstance(target, (ast.Tuple, ast.List, ast.Set)):
        for e in target.elts:
            if isinstance(e, ast.Name) and e.id in consts:
                out.append(consts[e.id])
            elif isinstance(e, ast.Constant) and isinstance(e.value, str):
                out.append(e.value)
    if not out:
        fail(f"{path.name}: {cls_name}.{attr} not resolved")
    return out


def set_minus_literal(func: ast.FunctionDef) -> list[str]:
    """Strings in `set(x) - {...}` inside func: the allowed keys (Starred state keys skipped)."""
    out = []
    for n in ast.walk(func):
        if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Sub) and isinstance(n.right, ast.Set):
            if isinstance(n.left, ast.Call) and getattr(n.left.func, "id", None) == "set":
                out += strs(n.right)
    return out


def snake(name: str) -> str:
    return re.sub(r"(?<=[a-z0-9])([A-Z])", r"_\1", name).lower()


# --------------------------------------------------------------------------- #
# keys
# --------------------------------------------------------------------------- #

keys: dict[str, dict] = {}


def add(kid, group, source, tokens_any, context_any=(), scope="file", example=None, note=None):
    """tokens_any: list of alternative groups; every token of one group must be in a code span.
    context_any: any one of these words in prose in the same scope (file or heading section)."""
    tokens_any = [list(dict.fromkeys(g)) for g in tokens_any if g]
    if kid in keys:
        k = keys[kid]
        for g in tokens_any:
            if g not in k["tokens_any"]:
                k["tokens_any"].append(g)
        k["context_any"] = sorted(set(k["context_any"]) | set(context_any))
        if source not in k["source"]:
            k["source"] += "; " + source
        return
    k = {"id": kid, "group": group, "source": source, "tokens_any": tokens_any,
         "context_any": sorted(set(context_any)), "scope": scope}
    if example:
        k["example"] = example
    if note:
        k["note"] = note
    keys[kid] = k


# --------------------------------------------------------------------------- #
# (a) routine and campaign tool inputs
# --------------------------------------------------------------------------- #

def golden_tools(server: pathlib.Path) -> dict[str, dict]:
    files = subprocess.run(["git", "-C", str(server), "ls-files"], capture_output=True, text=True, check=True).stdout.split()
    golden = [f for f in files if "mcp_tools_list.golden" in f]
    if len(golden) != 1:
        raise SystemExit(f"expected one mcp_tools_list.golden file, found {golden}")
    data = json.loads((server / golden[0]).read_text())
    tools = data.get("result", data).get("tools", data) if isinstance(data, dict) else data
    return {t["name"]: t for t in tools}, golden[0]


def tools_for(prefix):
    return sorted(t for t, p in TOOL_PREFIX.items() if p == prefix)


def walk_schema(prefix, path, schema, parent_leaf):
    ctx = tools_for(prefix)
    for name, sub in (schema.get("properties") or {}).items():
        if not path and name in SKIP_PARAMS:
            continue
        kid = f"{prefix}.{'.'.join(path + [name])}"
        toks = [[parent_leaf, name]] if parent_leaf else [[name]]
        add(kid, "tool_param", "mcp golden schema", toks, ctx)
        for v in sub.get("enum") or []:
            add(f"{kid}={v}", "tool_param", "mcp golden enum", [[name, str(v)]], ctx)
        walk_schema(prefix, path + [name], sub, name)
        items = sub.get("items")
        if isinstance(items, dict):
            for v in items.get("enum") or []:
                add(f"{kid}={v}", "tool_param", "mcp golden enum", [[name, str(v)]], ctx)
            walk_schema(prefix, path + [name], items, name)


def prose_list(desc: str, lead: str) -> list[str]:
    """Identifiers after `lead` up to the sentence end: 'One of: a, b, c.'"""
    m = re.search(re.escape(lead) + r"\s*([a-z0-9_, ]+?)\.", desc or "")
    return [w.strip() for w in m.group(1).split(",") if re.fullmatch(r"[a-z][a-z0-9_]*", w.strip())] if m else []


def tool_params(server, tools):
    for tool, prefix in TOOL_PREFIX.items():
        if tool not in tools:
            fail(f"golden lacks {tool}")
            continue
        walk_schema(prefix, [], tools[tool]["inputSchema"], None)

    rc = server / "workflows" / "routine_contract.py"
    rs = server / "workflows" / "routine_service.py"
    rm = server / "workflows" / "routine_media.py"
    routine_ctx = tools_for("routine")

    def enum(kid_base, field, values, source, ctx=routine_ctx):
        if not values:
            fail(f"no values for {kid_base}")
        for v in values:
            add(f"{kid_base}={v}", "tool_param", source, [[field, v]], ctx)

    enum("routine.outcome_category", "outcome_category", class_all(rc, "OutcomeCategory"), "routine_contract.OutcomeCategory")
    enum("routine.trigger_type", "trigger_type", class_all(rc, "TriggerType"), "routine_contract.TriggerType")
    enum("routine.approval_policy", "approval_policy", class_all(rc, "ApprovalPolicy"), "routine_contract.ApprovalPolicy")

    # schedule: the validator's allowed keys and interval words
    f = find_func(tree(rs), "_validate_schedule")
    sched_keys = set_minus_literal(f) if f else []
    if not sched_keys:
        fail("routine_service._validate_schedule: allowed keys not found")
    for k in sched_keys:
        add(f"routine.schedule.{k}", "tool_param", "routine_service._validate_schedule", [["schedule", k]], routine_ctx)
    enum("routine.schedule.interval", "interval", module_const(rs, "_SCHEDULE_INTERVALS"), "routine_service._SCHEDULE_INTERVALS")

    # output_config: allowed_fields in _validate_output_config + MEDIA_CONFIG_KEYS
    f = find_func(tree(rs), "_validate_output_config")
    oc = []
    if f:
        for n in ast.walk(f):
            if isinstance(n, ast.Assign) and any(getattr(t, "id", None) == "allowed_fields" for t in n.targets):
                oc += strs(n.value)
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and getattr(n.func.value, "id", None) == "allowed_fields":
                for a in n.args:
                    if isinstance(a, ast.Constant) and isinstance(a.value, str):
                        oc.append(a.value)
                    elif isinstance(a, ast.BinOp):
                        oc += strs(a.left) + strs(a.right)
                    elif isinstance(a, ast.Name) and a.id == "MEDIA_CONFIG_KEYS":
                        oc += module_const(rm, "MEDIA_CONFIG_KEYS")
    if "count" not in oc:
        fail("routine_service._validate_output_config: allowed_fields not parsed")
    for k in oc:
        add(f"routine.output_config.{k}", "tool_param", "routine_service._validate_output_config", [["output_config", k]], routine_ctx)
    enum("routine.output_config.artifact_type", "artifact_type", class_all(rc, "ArtifactType"), "routine_contract.ArtifactType")
    media_modes = []
    mm = module_assign(tree(rm), "MEDIA_MODES")
    if isinstance(mm, ast.Tuple):
        for e in mm.elts:
            v = module_assign(tree(rm), e.id) if isinstance(e, ast.Name) else e
            if isinstance(v, ast.Constant):
                media_modes.append(v.value)
    enum("routine.output_config.media_mode", "media_mode", media_modes, "routine_media.MEDIA_MODES")

    for func, sub in (("_validate_library_config", "library"), ("_validate_library_companion", "library"),
                      ("_validate_story_config", "story"), ("_validate_review_config", "review")):
        f = find_func(tree(rs), func)
        ks = set_minus_literal(f) if f else []
        if not ks:
            fail(f"routine_service.{func}: allowed keys not found")
        for k in ks:
            add(f"routine.output_config.{sub}.{k}", "tool_param", f"routine_service.{func}", [[sub, k]], routine_ctx)

    cs = server / "agents" / "carousel_job_settings.py"
    f = find_func(tree(cs), "validate_carousel_settings")
    ck = set_minus_literal(f) if f else []
    if not ck:
        # `set(value) - {...}` inside a boolean expression
        for n in ast.walk(f) if f else []:
            if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Sub) and isinstance(n.right, ast.Set):
                ck += strs(n.right)
    if not ck:
        fail("carousel_job_settings.validate_carousel_settings: keys not found")
    for k in ck:
        add(f"routine.output_config.carousel_config.{k}", "tool_param", "carousel_job_settings.validate_carousel_settings",
            [["carousel_config", k]], routine_ctx)
    wm = server / "workflows" / "models.py"
    for field, const in (("visualStyle", "CAROUSEL_VISUAL_STYLES"), ("aspectRatio", "CAROUSEL_ASPECT_RATIOS"),
                         ("continuity", "CAROUSEL_CONTINUITY")):
        enum(f"routine.output_config.carousel_config.{field}", field, module_const(wm, const), f"workflows.models.{const}")

    # revise-plan changes: the structured fields per plan kind
    ps = server / "agents" / "plan_shaping.py"
    for kind, const in (("routine", "ROUTINE_CHANGE_KEYS"), ("campaign", "CAMPAIGN_CHANGE_KEYS")):
        for k in module_const(ps, const):
            add(f"revise-plan.changes.{kind}.{k}", "tool_param", f"plan_shaping.{const}", [["changes", k]], ["revise-plan"])

    # campaigns
    camp_ctx = tools_for("campaign")
    st = server / "workflows" / "strategies.py"
    strategies = [kw.value.value for n in ast.walk(tree(st)) if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "Strategy"
                  for kw in n.keywords if kw.arg == "key" and isinstance(kw.value, ast.Constant)]
    enum("campaign.strategy_key", "strategy_key", strategies, "workflows/strategies.py Strategy(key=)", camp_ctx)
    mix_desc = tools["create-content-campaign"]["inputSchema"]["properties"]["content_mix"]["description"]
    m = re.search(r"Formats Bolta can make:\s*(.+?)\.\s", mix_desc)
    formats = [re.match(r"[a-z_]+", w.strip()).group(0) for w in m.group(1).split(",")] if m else []
    for k in formats:
        add(f"campaign.content_mix.{k}", "tool_param", "create-content-campaign content_mix description", [["content_mix", k]], camp_ctx)
    if not formats:
        fail("content_mix formats not found in the description")
    action_desc = tools["set-content-campaign-status"]["inputSchema"]["properties"]["action"]["description"]
    enum("campaign-status.action", "action", prose_list(action_desc, "Exactly one of:"), "set-content-campaign-status action description",
         ["set-content-campaign-status"])
    targets = tools["create-content-campaign"]["inputSchema"]["properties"]["context_sources"]["description"]
    m = re.search(r"Brand-kit sections:\s*(.+?)\.\s", targets)
    if not m:
        fail("context_sources brand-kit sections not found in the create-content-campaign description")
    for k in ([w.strip() for w in m.group(1).split(",")] if m else []):
        add(f"campaign.context_sources.brand_kit={k}", "tool_param", "create-content-campaign context_sources description",
            [["brand_kit", k]], camp_ctx)


# --------------------------------------------------------------------------- #
# (b) per-network fields and platform_specific keys
# --------------------------------------------------------------------------- #

FIELD_CALLS = {"CharField", "TextField", "BooleanField", "IntegerField", "PositiveIntegerField", "BigIntegerField",
               "FloatField", "DecimalField", "URLField", "JSONField", "DateTimeField", "DateField", "UUIDField",
               "SlugField", "EmailField", "SmallIntegerField", "PositiveSmallIntegerField", "ForeignKey",
               "OneToOneField", "ManyToManyField", "ArrayField", "ImageField", "FileField", "DurationField", "TimeField"}
SYSTEM_DETAIL_FIELDS = {"id", "created_at", "updated_at"}


def resolve_choices(node, cls, mod) -> list[str]:
    def pairs(n):
        out = []
        if isinstance(n, (ast.List, ast.Tuple)):
            for e in n.elts:
                if isinstance(e, (ast.Tuple, ast.List)) and e.elts and isinstance(e.elts[0], ast.Constant):
                    out.append(str(e.elts[0].value))
        return out
    if isinstance(node, ast.Name):
        for body_node in cls.body:
            if isinstance(body_node, ast.Assign) and any(getattr(t, "id", None) == node.id for t in body_node.targets):
                return pairs(body_node.value)
        v = module_assign(mod, node.id)
        return pairs(v) if v is not None else []
    if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):  # OtherModel.CHOICES
        other = find_class(mod, node.value.id)
        if other is not None:
            return resolve_choices(ast.Name(id=node.attr), other, mod)
    return pairs(node)


def model_fields(path: pathlib.Path, cls_name: str):
    mod = tree(path)
    cls = find_class(mod, cls_name)
    if cls is None:
        fail(f"{path}: class {cls_name} not found")
        return [], {}
    fields, choices = [], {}
    for node in cls.body:
        if not (isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)):
            continue
        call = node.value
        if not isinstance(call, ast.Call):
            continue
        fname = call.func.attr if isinstance(call.func, ast.Attribute) else getattr(call.func, "id", "")
        if fname not in FIELD_CALLS:
            if isinstance(call.func, ast.Attribute) and getattr(call.func.value, "id", None) == "models" \
                    and fname.endswith(("Field", "Key")):
                fail(f"{cls_name}.{node.targets[0].id}: unknown field type models.{fname}; add it to FIELD_CALLS")
            continue
        name = node.targets[0].id
        kw = {k.arg: k.value for k in call.keywords}

        def true(k):
            return isinstance(kw.get(k), ast.Constant) and kw[k].value is True
        if name in SYSTEM_DETAIL_FIELDS or true("primary_key") or true("auto_now") or true("auto_now_add") \
                or (isinstance(kw.get("editable"), ast.Constant) and kw["editable"].value is False):
            continue
        fields.append(name)
        if fname == "ForeignKey":
            fields.append(f"{name}_id")
        if "choices" in kw:
            vals = resolve_choices(kw["choices"], cls, mod)
            if vals:
                choices[name] = vals
            else:
                fail(f"{cls_name}.{name}: choices not resolved")
    return fields, choices


def post_details(server):
    view = server / "posts" / "post_details_api_v1_views.py"
    mod = tree(view)
    imports = {a.name: n.module for n in mod.body if isinstance(n, ast.ImportFrom) and n.module for a in n.names}
    func = find_func(mod, "_build_platform_config")
    ret = next((n.value for n in ast.walk(func) if isinstance(n, ast.Return)), None) if func else None
    if not isinstance(ret, ast.Dict):
        fail("post_details_api_v1_views._build_platform_config not parsed")
        return {}
    nets = {}
    for k, v in zip(ret.keys, ret.values):
        net = k.value
        entry = {kk.value: vv for kk, vv in zip(v.keys, v.values)}
        model = entry["model"].id
        display = entry["display_name"].value
        path = server / (imports[model].replace(".", "/") + ".py")
        fields, choices = model_fields(path, model)
        if not fields:
            fail(f"{net}: no updatable fields parsed from {model}")
        nets[net] = display
        ctx = sorted({net, display})
        for fld in fields:
            alts = [[fld]]
            if fld.endswith("_id") and fld[:-3] in fields:
                alts.append([fld[:-3]])
            elif f"{fld}_id" in fields:
                alts.append([f"{fld}_id"])
            add(f"{net}.{fld}", "post_details", f"{model} (save-post platform_details)", alts, ctx, "section",
                example={"network": net, "field": fld, "where": "fields"})
        for fld, vals in choices.items():
            for val in vals:
                add(f"{net}.{fld}={val}", "post_details", f"{model}.{fld} choices", [[fld, val]], ctx, "section")
    return nets


def str_arg(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return [node.value]
    return strs(node)


def platform_specific(server, nets):
    found = {}  # (net, snake) -> set(spellings)

    def note(net, *spellings, source):
        spellings = [s for s in spellings if s and s not in NOT_CALLER_KEYS]
        if not spellings:
            return
        base = snake(spellings[0])
        found.setdefault((net, base), [set(), set()])
        found[(net, base)][0].update(spellings)
        found[(net, base)][1].add(source)

    pub = server / "posts" / "tasks" / "publishing"
    for path in sorted(pub.glob("*.py")):
        if path.name in PUBLISHER_SKIP or path.name.startswith("test_"):
            continue
        file_net = path.stem
        for n in ast.walk(tree(path)):
            if not isinstance(n, ast.Call):
                continue
            fn = n.func.attr if isinstance(n.func, ast.Attribute) else getattr(n.func, "id", "")
            if fn == "get_effective_field" and len(n.args) >= 3:
                net = n.args[1].value if isinstance(n.args[1], ast.Constant) else file_net
                note(net, *str_arg(n.args[2]), source=f"publishing/{path.name} get_effective_field")
            elif fn == "get" and isinstance(n.func, ast.Attribute) and getattr(n.func.value, "id", None) == "platform_options" and n.args:
                note(file_net, *str_arg(n.args[0]), source=f"publishing/{path.name} platform_options.get")
            elif fn == "_resolved_bool" and len(n.args) >= 2 and getattr(n.args[0], "id", None) == "platform_options":
                note(file_net, *str_arg(n.args[1]), source=f"publishing/{path.name} _resolved_bool")
    for k in module_const(pub / "wordpress.py", "WORDPRESS_PLATFORM_SPECIFIC_KEYS"):
        note("wordpress", k, source="publishing/wordpress.py WORDPRESS_PLATFORM_SPECIFIC_KEYS")

    # Pinterest: account_pin_options(...) is passed to resolve_pin_media as `options`
    media = server / "pinterest_api_handler" / "media.py"
    f = find_func(tree(media), "resolve_pin_media")
    for n in ast.walk(f) if f else []:
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "get" \
                and getattr(n.func.value, "id", None) == "options" and n.args:
            note("pinterest", *str_arg(n.args[0]), source="pinterest_api_handler/media.py resolve_pin_media")

    # Instagram: platformSpecific.instagram copied onto the row (instagram_row_fields)
    psf = server / "posts" / "platform_specific.py"
    f = find_func(tree(psf), "instagram_row_fields")
    for n in ast.walk(f) if f else []:
        if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "_first_present":
            names = [a.value for a in n.args[1:] if isinstance(a, ast.Constant) and isinstance(a.value, str)]
            if names:
                note("instagram", *sorted(names, key=lambda s: s != snake(s)), source="platform_specific.instagram_row_fields")
        if isinstance(n, ast.Tuple) and len(n.elts) >= 2 and isinstance(n.elts[0], ast.Constant) \
                and isinstance(n.elts[0].value, str) and isinstance(n.elts[1], ast.Tuple):
            note("instagram", n.elts[0].value, *strs(n.elts[1]), source="platform_specific.instagram_row_fields")
    for field, const in (("content_type", "_IG_CONTENT_TYPES"), ("media_type", "_IG_MEDIA_TYPES"),
                         ("trial_graduation_strategy", "_IG_TRIAL_STRATEGIES")):
        for v in sorted(module_const(psf, const)):
            add(f"instagram.platform_specific.{field}={v}", "platform_specific", f"platform_specific.{const}",
                [[field, v], [re.sub(r"_([a-z])", lambda m: m.group(1).upper(), field), v]],
                ["instagram", "Instagram"], "section")

    known = module_const(psf, "KNOWN_NETWORKS")
    for (net, base), (spellings, sources) in sorted(found.items()):
        if net not in known:
            fail(f"publisher key {base} for unknown network {net}")
        display = nets.get(net, net)
        add(f"{net}.platform_specific.{base}", "platform_specific", "; ".join(sorted(sources)),
            [[s] for s in sorted(spellings, key=lambda s: (s != base, s))], sorted({net, display}), "section",
            example={"network": net, "field": base, "spellings": sorted(spellings), "where": "platform_specific"})
    # the shape itself: per-network text override and per-account entries (posts/tasks/publishing/base.py)
    add("platform_specific.text", "platform_specific", "publishing/base.py get_effective_content", [["platform_specific", "text"]])
    add("platform_specific.accounts", "platform_specific", "posts/platform_specific.py shape", [["platform_specific", "accounts"]])
    with_keys = {net for net, _ in found}
    for net in ("x", "threads", "instagram", "linkedin", "reddit", "tiktok", "youtube", "pinterest", "wordpress"):
        if net not in with_keys:
            fail(f"no publisher keys parsed for {net}")


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    server = pathlib.Path(argv[0]).expanduser().resolve() if argv else DEFAULT_SERVER
    if not (server / "posts" / "platform_specific.py").is_file():
        print(f"ERROR not a Bolta server checkout: {server}")
        return 2
    tools, golden = golden_tools(server)
    tool_params(server, tools)
    nets = post_details(server)
    platform_specific(server, nets)
    for name in sorted(tools):
        add(f"tool.{name}", "tool", "mcp golden", [[name]])
    if errors:
        for e in errors:
            print(f"ERROR {e}")
        print("Not written: a source yielded nothing, so the fixture would under-count.")
        return 1
    sha = subprocess.run(["git", "-C", str(server), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    counts = {}
    for k in keys.values():
        counts[k["group"]] = counts.get(k["group"], 0) + 1
    out = {
        "generated_by": "tools/build_coverage_fixture.py",
        "server_commit": sha,
        "golden": golden,
        "counts": counts,
        "keys": sorted(keys.values(), key=lambda k: (k["group"], k["id"])),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print(f"wrote {OUT.relative_to(REPO)}: {len(keys)} keys {counts} from server {sha}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

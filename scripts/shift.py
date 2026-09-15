#!/usr/bin/env python3
"""shift: bookkeeping for the First Shift and the local self-improvement loop.

  shift.py status [--brief]        overlay location, setup state, journal count since distill, staleness
  shift.py init                    create the overlay from templates (idempotent)
  shift.py discover                inventory local connectors and context files; write overlay/discovery.md
  shift.py window <7|14|30|YYYY-MM-DD..YYYY-MM-DD>   record the review window the operator chose
  shift.py answer <key> "<text>"   record an interview answer (marks the question done)
  shift.py journal --moment M --channel C --outcome O --score N --lesson "..." [--diff "..."]
  shift.py distill                 print journal entries since the last distill, grouped; records the marker
  shift.py learn "<rule>" --moment M --evidence N     add a learned rule (expires in 90 days)
  shift.py learn --reinforce <n>   bump evidence + expiry on rule n
  shift.py learn --drop <n>        remove rule n
  shift.py in-motion --touch       record that overlay/in-motion.md was refreshed now

Overlay resolution: $FOH_OVERLAY, then ./overlay, then ~/.front-of-house/overlay.
Nothing here reads customer data. It only keeps the overlay's state files tidy.
"""
import argparse
import datetime as dt
import json
import os
import re
import shutil
import sys
from pathlib import Path

CANON = Path(__file__).resolve().parent.parent
TODAY = dt.date.today()
DISTILL_THRESHOLD = 5
IN_MOTION_STALE_DAYS = 7
RULE_TTL_DAYS = 90
RULE_CAP = 30


def question_keys():
    """Keys from first-shift/questions.md, so the count is never hardcoded."""
    p = CANON / "first-shift" / "questions.md"
    keys = re.findall(r"^\| *\d+ *\| *`([a-z_]+)`", p.read_text(), re.M) if p.exists() else []
    return keys or ["operator_name"]


def overlay_dir():
    env = os.environ.get("FOH_OVERLAY")
    if env:
        return Path(env).expanduser()
    local = Path.cwd() / "overlay"
    if local.exists():
        return local
    return Path.home() / ".front-of-house" / "overlay"


def state_path(o):
    return o / "STATE.md"


def read_state(o):
    p = state_path(o)
    st = {"setup": "incomplete", "answered": [], "last_distill": None, "in_motion_refreshed": None, "adapter": None, "host": None, "preshift": "offer", "window": None, "discovered": None}
    if not p.exists():
        return st
    m = re.search(r"```json\n(.*?)\n```", p.read_text(), re.S)
    if m:
        try:
            st.update(json.loads(m.group(1)))
        except json.JSONDecodeError:
            pass
    return st


def write_state(o, st):
    o.mkdir(parents=True, exist_ok=True)
    body = (
        "# Overlay state (managed by scripts/shift.py)\n\n"
        f"setup: {st['setup']}\n\n"
        "```json\n" + json.dumps(st, indent=2, default=str) + "\n```\n"
    )
    state_path(o).write_text(body)


def journal_entries(o, since=None):
    jd = o / "journal"
    out = []
    if not jd.exists():
        return out
    for f in sorted(jd.glob("*.md")):
        day = f.stem
        if since and day <= since:
            continue
        for block in f.read_text().split("\n- ")[1:]:
            out.append((day, "- " + block.strip()))
    return out


def learned_rules(o):
    p = o / "learned.md"
    if not p.exists():
        return []
    return [l for l in p.read_text().splitlines() if l.startswith("- [")]


def cmd_status(a):
    o = overlay_dir()
    st = read_state(o)
    since = st.get("last_distill")
    entries = journal_entries(o, since)
    im = o / "in-motion.md"
    im_age = None
    if st.get("in_motion_refreshed"):
        im_age = (TODAY - dt.date.fromisoformat(st["in_motion_refreshed"])).days
    rules = learned_rules(o)
    expiring = [r for r in rules if _expires(r) and (_expires(r) - TODAY).days <= 7]
    warranted = []
    if len(entries) >= DISTILL_THRESHOLD:
        warranted.append(f"{len(entries)} journal entries to distill")
    if im.exists() and (im_age is None or im_age > IN_MOTION_STALE_DAYS):
        warranted.append(f"in-motion read is {im_age} days old" if im_age is not None else "in-motion read has never been refreshed")
    if expiring:
        warranted.append(f"{len(expiring)} learned rule(s) expiring within 7 days")
    if a.brief:
        if st["setup"] != "complete":
            nxt = "start with `python3 scripts/shift.py discover`" if not st.get("discovered") else f"{len(st.get('answered', []))}/{len(question_keys())} answered; resume the interview"
            print(f"Front of House: overlay setup incomplete. Run the First Shift (FIRST-SHIFT.md); {nxt}.")
        elif warranted:
            print("Front of House pre-shift warranted: " + "; ".join(warranted) + ". Offer a two-minute pre-shift.")
        else:
            print(f"Front of House: overlay ready at {o}. {len(rules)} learned rules. No pre-shift needed.")
        return 0
    print(f"overlay:            {o} ({'exists' if o.exists() else 'missing'})")
    print(f"setup:              {st['setup']}  (answered {len(st.get('answered', []))}/{len(question_keys())} interview questions)")
    print(f"host / adapter:     {st.get('host') or '?'} / {st.get('adapter') or '?'}")
    print(f"discovery:          {('done ' + st['discovered']) if st.get('discovered') else 'not run (python3 scripts/shift.py discover)'}")
    print(f"review window:      {st.get('window') or 'not chosen'}")
    print(f"journal since last distill: {len(entries)} (threshold {DISTILL_THRESHOLD}; last distill {since or 'never'})")
    print(f"in-motion:          {'present' if im.exists() else 'missing'}, refreshed {st.get('in_motion_refreshed') or 'never'}" + (f" ({im_age}d ago)" if im_age is not None else ""))
    print(f"learned rules:      {len(rules)}/{RULE_CAP}, {len(expiring)} expiring within 7 days")
    print("pre-shift:          " + ("WARRANTED: " + "; ".join(warranted) if warranted else "not needed"))
    return 0


def _expires(rule_line):
    m = re.search(r"expires: (\d{4}-\d{2}-\d{2})", rule_line)
    return dt.date.fromisoformat(m.group(1)) if m else None


def cmd_init(a):
    o = overlay_dir()
    o.mkdir(parents=True, exist_ok=True)
    (o / "journal").mkdir(exist_ok=True)
    for t in (CANON / "overlay").glob("*.template.*"):
        dest = o / t.name.replace(".template", "")
        if not dest.exists():
            shutil.copy(t, dest)
            print(f"created {dest}")
    if not (o / "learned.md").exists():
        (o / "learned.md").write_text("# Learned rules (local, managed by scripts/shift.py)\n\nLoaded after the canon and the overlay. Can narrow anything; never loosens a guardrail.\n\n")
        print(f"created {o / 'learned.md'}")
    st = read_state(o)
    st.setdefault("host", a.host)
    if a.host:
        st["host"] = a.host
    write_state(o, st)
    print(f"overlay ready at {o}")
    return 0


def cmd_answer(a):
    o = overlay_dir()
    st = read_state(o)
    o.mkdir(parents=True, exist_ok=True)
    p = o / "interview.md"
    if not p.exists():
        p.write_text("# Interview answers (raw, one per key; the agent folds these into the overlay files)\n\n")
    with p.open("a") as f:
        f.write(f"## {a.key} ({TODAY})\n{a.text}\n\n")
    if a.key not in st["answered"]:
        st["answered"].append(a.key)
    if a.key == "context_layer":
        st["adapter"] = a.text.strip()[:60]
    keys = question_keys()
    if a.key == "time_window":
        st["window"] = a.text.strip()[:40]
    if all(k in st["answered"] for k in keys):
        st["setup"] = "complete"
    write_state(o, st)
    print(f"saved {a.key} ({len(st['answered'])}/{len(keys)})")
    return 0


def cmd_journal(a):
    o = overlay_dir()
    jd = o / "journal"
    jd.mkdir(parents=True, exist_ok=True)
    p = jd / f"{TODAY}.md"
    if not p.exists():
        p.write_text(f"# Journal {TODAY}\n\n")
    line = f"- {dt.datetime.now().strftime('%H:%M')} {a.moment} / {a.channel} / {a.outcome} / score {a.score}: {a.lesson}"
    if a.diff:
        line += f"\n  diff: {a.diff}"
    with p.open("a") as f:
        f.write(line + "\n")
    print("journaled")
    return 0


def cmd_distill(a):
    o = overlay_dir()
    st = read_state(o)
    entries = journal_entries(o, st.get("last_distill"))
    if not entries:
        print("nothing to distill")
        return 0
    by = {}
    for day, e in entries:
        m = re.match(r"- \d\d:\d\d (\S+) / (\S+) / (\S+) / score (\d+)", e)
        key = m.group(1) if m else "unknown"
        by.setdefault(key, []).append((day, e))
    for moment, items in sorted(by.items(), key=lambda kv: -len(kv[1])):
        outcomes = {}
        for _, e in items:
            m = re.match(r"- \d\d:\d\d \S+ / \S+ / (\S+)", e)
            oc = m.group(1) if m else "?"
            outcomes[oc] = outcomes.get(oc, 0) + 1
        print(f"\n## {moment}  ({len(items)} entries: {', '.join(f'{k} {v}' for k, v in outcomes.items())})")
        for day, e in items:
            print(f"[{day}] {e}")
    print("\nLook for lessons that repeat with the same shape. Propose each as one line; add with `shift.py learn`.")
    st["last_distill"] = str(TODAY)
    write_state(o, st)
    return 0


def cmd_learn(a):
    o = overlay_dir()
    p = o / "learned.md"
    if not p.exists():
        cmd_init(argparse.Namespace(host=None))
    lines = p.read_text().splitlines()
    rules = [i for i, l in enumerate(lines) if l.startswith("- [")]
    if a.reinforce is not None or a.drop is not None:
        n = a.reinforce if a.reinforce is not None else a.drop
        if n < 1 or n > len(rules):
            print(f"no rule {n}; there are {len(rules)}")
            return 1
        idx = rules[n - 1]
        if a.drop is not None:
            print("dropped: " + lines[idx])
            del lines[idx]
        else:
            l = lines[idx]
            ev = int(re.search(r"evidence: (\d+)", l).group(1)) + 1
            l = re.sub(r"evidence: \d+", f"evidence: {ev}", l)
            l = re.sub(r"reinforced: \d{4}-\d{2}-\d{2}", f"reinforced: {TODAY}", l)
            l = re.sub(r"expires: \d{4}-\d{2}-\d{2}", f"expires: {TODAY + dt.timedelta(days=RULE_TTL_DAYS)}", l)
            lines[idx] = l
            print("reinforced: " + l)
        p.write_text("\n".join(lines) + "\n")
        return 0
    if not a.rule:
        print("rule text required")
        return 2
    if len(rules) >= RULE_CAP:
        print(f"learned.md has {RULE_CAP} rules; retire one first (shift.py learn --drop N)")
        return 1
    line = f"- [{TODAY}] {a.moment or 'all'}: {a.rule.strip()} (evidence: {a.evidence}, reinforced: {TODAY}, expires: {TODAY + dt.timedelta(days=RULE_TTL_DAYS)})"
    lines.append(line)
    p.write_text("\n".join(lines) + "\n")
    print("learned: " + line)
    return 0


def cmd_in_motion(a):
    o = overlay_dir()
    st = read_state(o)
    st["in_motion_refreshed"] = str(TODAY)
    write_state(o, st)
    print(f"in-motion marked refreshed {TODAY}")
    return 0


# ---------------------------------------------------------------------------
# discover: what context is already reachable from this machine
# ---------------------------------------------------------------------------

# Known connector families. Order inside each family is "prefer first" when recommending
# a customer-context source. Matched against MCP server names, commands, and URLs.
CONNECTOR_FAMILIES = [
    ("customer context / CRM", ["moonbase", "yavin", "hubspot", "attio", "salesforce", "pipedrive", "close", "folk", "twenty", "clay"]),
    ("support desk", ["intercom", "zendesk", "front", "helpscout", "plain", "freshdesk", "gorgias", "pylon", "linear-support"]),
    ("conversations", ["slack", "gmail", "google-workspace", "outlook", "microsoft-365", "imessage", "whatsapp", "discord"]),
    ("meetings", ["granola", "gong", "fireflies", "otter", "fathom", "circleback", "zoom"]),
    ("product usage", ["posthog", "mixpanel", "amplitude", "segment", "june", "heap"]),
    ("billing", ["stripe", "chargebee", "paddle", "recurly"]),
    ("work tracking", ["linear", "jira", "github", "notion", "asana"]),
]

SECRET = re.compile(r"(Bearer\s+|sk_|mb_|phx_|pat_|xoxb-|xoxp-|ghp_|key[-_]?)[A-Za-z0-9_\-\.]{8,}", re.I)


def _mask(text):
    return SECRET.sub(lambda m: m.group(1) + "***", str(text))


def _family(name, blob):
    hay = (name + " " + blob).lower()
    for fam, needles in CONNECTOR_FAMILIES:
        for n in needles:
            if n in hay:
                return fam
    return "other"


def _mcp_from_json(path, keys=("mcpServers", "mcp_servers", "servers")):
    """Return [(server_name, summary)] from a JSON config, tolerating nested project maps."""
    out = []
    try:
        data = json.loads(path.read_text())
    except Exception:
        return out

    def walk(d, depth=0):
        if not isinstance(d, dict) or depth > 4:
            return
        for k in keys:
            if isinstance(d.get(k), dict):
                for name, cfg in d[k].items():
                    if isinstance(cfg, dict):
                        summ = cfg.get("url") or cfg.get("httpUrl") or " ".join([cfg.get("command", "")] + [str(x) for x in cfg.get("args", [])])
                        out.append((name, _mask(summ)))
        for v in d.values():
            if isinstance(v, dict):
                walk(v, depth + 1)
    walk(data)
    return out


def _mcp_from_toml(path):
    out = []
    try:
        txt = path.read_text()
    except Exception:
        return out
    for m in re.finditer(r"\[mcp_servers\.([^\]]+)\]\s*(.*?)(?=\n\[|\Z)", txt, re.S):
        name, body = m.group(1), m.group(2)
        u = re.search(r'(?:url|command)\s*=\s*"([^"]+)"', body)
        out.append((name, _mask(u.group(1) if u else "")))
    return out


def _context_files(cwd, home):
    """Local files that usually say who the operator is and who they sell to."""
    hits = []
    names = ["CLAUDE.md", "AGENTS.md", "GEMINI.md", "README.md", "CONTRIBUTING.md", ".cursorrules", "copilot-instructions.md"]
    for n in names:
        for p in [cwd / n, cwd / ".github" / n]:
            if p.is_file():
                hits.append(("project file", p))
    for d in ["docs", "kb", "knowledge", "context", "notes", "customers", "playbooks", ".cursor/rules"]:
        p = cwd / d
        if p.is_dir():
            hits.append(("project dir", p))
    for p in [home / ".claude" / "CLAUDE.md", home / ".codex" / "AGENTS.md", home / ".gemini" / "GEMINI.md", home / ".cursor" / "rules"]:
        if p.exists():
            hits.append(("user-level instructions", p))
    mem = home / ".claude" / "projects"
    if mem.is_dir():
        for idx in sorted(mem.glob("*/memory/MEMORY.md"))[:5]:
            hits.append(("agent memory index", idx))
    for d in [home / ".front-of-house" / "overlay", cwd / "overlay"]:
        if (d / "README.md").exists():
            hits.append(("overlay", d))
    return hits


def cmd_discover(a):
    o = overlay_dir()
    cwd, home = Path.cwd(), Path.home()
    configs = [
        ("cursor (global)", home / ".cursor" / "mcp.json", "json"),
        ("cursor (project)", cwd / ".cursor" / "mcp.json", "json"),
        ("claude code (user)", home / ".claude.json", "json"),
        ("claude code (project)", cwd / ".mcp.json", "json"),
        ("claude desktop", home / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json", "json"),
        ("claude desktop", home / ".config" / "Claude" / "claude_desktop_config.json", "json"),
        ("codex", home / ".codex" / "config.toml", "toml"),
        ("gemini cli", home / ".gemini" / "settings.json", "json"),
        ("vs code / copilot", cwd / ".vscode" / "mcp.json", "json"),
        ("windsurf", home / ".codeium" / "windsurf" / "mcp_config.json", "json"),
        ("cline", home / "Library" / "Application Support" / "Code" / "User" / "globalStorage" / "saoudrizwan.claude-dev" / "settings" / "cline_mcp_settings.json", "json"),
    ]
    servers = {}  # name -> (family, summary, [hosts])
    for host, path, kind in configs:
        if not path.exists():
            continue
        found = _mcp_from_json(path) if kind == "json" else _mcp_from_toml(path)
        for name, summ in found:
            fam = _family(name, summ)
            entry = servers.setdefault(name, [fam, summ, []])
            if host not in entry[2]:
                entry[2].append(host)
    files = _context_files(cwd, home)

    by_fam = {}
    for name, (fam, summ, hosts) in servers.items():
        by_fam.setdefault(fam, []).append((name, summ, hosts))
    order = [f for f, _ in CONNECTOR_FAMILIES] + ["other"]

    lines = [f"# Discovery, as of {TODAY}", "", f"Working directory: `{cwd}`. Secrets masked. Nothing here was sent anywhere.", ""]
    lines += ["## Connectors already configured on this machine", ""]
    if not servers:
        lines.append("None found in any known host config. Ask the operator where customer context lives.")
    for fam in order:
        if fam not in by_fam:
            continue
        lines.append(f"### {fam}")
        for name, summ, hosts in sorted(by_fam[fam]):
            lines.append(f"- `{name}` via {', '.join(hosts)}" + (f" ({summ[:90]})" if summ else ""))
        lines.append("")
    lines += ["## Local files that likely say who we are and who we sell to", ""]
    if not files:
        lines.append("None found. Ask.")
    for kind, p in files:
        lines.append(f"- {kind}: `{p}`")
    lines += ["", "## Recommendation (agent fills in after reading the above)", ""]
    rec = []
    for fam in ["customer context / CRM", "support desk", "conversations", "meetings", "product usage"]:
        if fam in by_fam:
            rec.append(f"- **{fam}:** " + ", ".join(f"`{n}`" for n, _, _ in sorted(by_fam[fam])))
    if rec:
        lines.append("Candidates for the customer's file, best family first. Propose the top one; ask the operator to confirm or point elsewhere.")
        lines += rec
    else:
        lines.append("No customer-context connector found. Ask: \"Where does customer context live? A CRM, a support desk, a shared inbox, a folder of notes?\" Then help wire it (docs/setup/context-layer.md).")
    lines += ["", "## Customer identification", "", "Not yet decided. Ask whether the operator has a way to tell customers from prospects, vendors, and teammates; otherwise take a quick pass and propose heuristics into `overlay/customers.md`.", ""]

    o.mkdir(parents=True, exist_ok=True)
    (o / "discovery.md").write_text("\n".join(lines))
    st = read_state(o)
    st["discovered"] = str(TODAY)
    write_state(o, st)
    print("\n".join(lines))
    print(f"\nwrote {o / 'discovery.md'}")
    return 0


def cmd_window(a):
    o = overlay_dir()
    st = read_state(o)
    w = a.window.strip()
    if w in ("7", "14", "30"):
        start = TODAY - dt.timedelta(days=int(w))
        label = f"last {w} days ({start}..{TODAY})"
    elif re.fullmatch(r"\d{4}-\d{2}-\d{2}\.\.\d{4}-\d{2}-\d{2}", w):
        label = f"custom ({w})"
    else:
        print("window must be 7, 14, 30, or YYYY-MM-DD..YYYY-MM-DD", file=sys.stderr)
        return 2
    st["window"] = label
    if "time_window" not in st["answered"]:
        st["answered"].append("time_window")
    if all(k in st["answered"] for k in question_keys()):
        st["setup"] = "complete"
    write_state(o, st)
    print(f"review window: {label}")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("status"); s.add_argument("--brief", action="store_true"); s.set_defaults(fn=cmd_status)
    s = sub.add_parser("init"); s.add_argument("--host"); s.set_defaults(fn=cmd_init)
    s = sub.add_parser("answer"); s.add_argument("key"); s.add_argument("text"); s.set_defaults(fn=cmd_answer)
    s = sub.add_parser("journal")
    for f in ["--moment", "--channel", "--outcome", "--lesson"]:
        s.add_argument(f, required=True)
    s.add_argument("--score", type=int, required=True); s.add_argument("--diff"); s.set_defaults(fn=cmd_journal)
    s = sub.add_parser("distill"); s.set_defaults(fn=cmd_distill)
    s = sub.add_parser("learn"); s.add_argument("rule", nargs="?"); s.add_argument("--moment"); s.add_argument("--evidence", type=int, default=2)
    s.add_argument("--reinforce", type=int); s.add_argument("--drop", type=int); s.set_defaults(fn=cmd_learn)
    s = sub.add_parser("in-motion"); s.add_argument("--touch", action="store_true"); s.set_defaults(fn=cmd_in_motion)
    s = sub.add_parser("discover"); s.set_defaults(fn=cmd_discover)
    s = sub.add_parser("window"); s.add_argument("window"); s.set_defaults(fn=cmd_window)
    a = ap.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())

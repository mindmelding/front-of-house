#!/usr/bin/env python3
"""engine: bookkeeping for the compounding loop (sweep, lineup, drill, refresh).

Nothing here calls a model or a connector. It keeps the overlay's state files tidy and
enforces one rule: anything the engine LEARNS is anonymized at write time; anything the
engine DOES (briefs, held drafts, the ledger) stays operational and private.

  engine.py status [--brief]                 one line for the SessionStart hook, or the full table
  engine.py scorecard                        draft survival, pick precision, house confidence

  engine.py alias add "<real>" --kind account|person|domain [--org "<account>"]
  engine.py alias list | seed | drop "<real>" | apply [file|-] | reveal [file|-] | audit [--fix]

  engine.py house init | status | index
  engine.py house add <moment> "<rule>" [--evidence N] [--source "..."] [--confirmed]
  engine.py house deny <moment> "<proposal>" --why "..."
  engine.py house reinforce <moment> <n> | drop <moment> <n> | expiring [--days 14]
  engine.py house exemplar <moment> --file <reply.md> --why "..."

  engine.py queue add --moment M --kind rule|new-situation|method|lexicon --text "..." [--evidence N] [--source "..."]
  engine.py queue list [--all] | decide <id> approve|deny|later|reword [--text "..."] [--why "..."]

  engine.py drafts hold --account A --person P --channel C --moment M --thread REF --file draft.md
  engine.py drafts list [--all] | resolve <path> --outcome sent-as-is|edited|not-sent [--sent-file f] [--lesson "..."]

  engine.py ledger append <brief.json> | list | grade <id> --verdict V [--acted yes|no] [--note "..."] | miss "<account>" "<note>"

  engine.py drill next [--n 3] | record --scenario ID --moment M --house-score N --operator-score N \
            --delta "..." [--rule "..."] [--answer-file f]

  engine.py heartbeat start | end --signal "..." | check [--brief]
  engine.py watermark get | set <iso-datetime>
  engine.py journal --moment M --channel C --outcome O --score N --lesson "..." [--diff "..."]

Overlay resolution: $FOH_OVERLAY, then ./overlay, then ~/.front-of-house/overlay.
"""
import argparse
import datetime as dt
import difflib
import json
import os
import re
import sys
from pathlib import Path

CANON = Path(__file__).resolve().parent.parent
TODAY = dt.date.today()
NOW = dt.datetime.now()
RULE_TTL_DAYS = 90
RULE_CAP_TOTAL = 30
CONFIDENCE = [(7, "high"), (3, "medium"), (0, "low")]

# Files the engine learns into. Everything written here passes through anonymize().
LEARNING_DIRS = ["house", "journal", "queue", "evals", "drills", "method.md", "lexicon.md"]

ACCOUNT_ALIASES = [
    "Alder", "Basalt", "Cobalt", "Dune", "Ember", "Fjord", "Granite", "Heron", "Iris", "Juniper",
    "Kestrel", "Larch", "Marlin", "Nimbus", "Osprey", "Pine", "Quarry", "Reef", "Sable", "Tundra",
    "Umber", "Vale", "Wren", "Yarrow", "Zephyr", "Atlas", "Birch", "Cedar", "Delta", "Echo",
    "Fern", "Grove", "Halyard", "Ivory", "Jasper", "Kelp", "Lumen", "Moss", "Nettle", "Onyx",
    "Pebble", "Quill", "Rill", "Slate", "Thistle", "Ultra", "Verdant", "Willow", "Xenia", "Yew",
]
PERSON_ALIASES = [
    "Avery", "Blake", "Casey", "Devon", "Emerson", "Finley", "Harper", "Jordan", "Kai", "Logan",
    "Morgan", "Noel", "Parker", "Quinn", "Reese", "Rowan", "Sage", "Tatum", "Wynn", "Ari",
    "Bex", "Cam", "Dari", "Eli", "Frankie", "Gray", "Hollis", "Indy", "Jules", "Kit",
    "Lane", "Marlow", "Nico", "Oakley", "Perry", "Remy", "Shay", "Toby", "Val", "Zion",
    "Arden", "Bellamy", "Cyan", "Dallas", "Ellis", "Flynn", "Greer", "Haven", "Jem", "Lior",
]

EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
PHONE = re.compile(r"(?<!\d)(?:\+?1[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}(?!\d)")
ID_LINK = re.compile(r"https?://\S*?/(?:id|identity|org|people|person|accounts?)/[\w/-]+")


# ---------------------------------------------------------------------------
# overlay + small helpers
# ---------------------------------------------------------------------------

def overlay_dir():
    env = os.environ.get("FOH_OVERLAY")
    if env:
        return Path(env).expanduser()
    local = Path.cwd() / "overlay"
    if local.exists():
        return local
    return Path.home() / ".front-of-house" / "overlay"


O = None  # set in main()


def p(*parts):
    path = O.joinpath(*parts)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def read_json(path, default):
    return json.loads(path.read_text()) if path.exists() else default


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, default=str) + "\n")


def slug(s):
    return re.sub(r"(^-|-$)", "", re.sub(r"[^a-z0-9]+", "-", s.lower()))


def moments():
    return sorted(d.name for d in (CANON / "moments").iterdir() if (d / "PLAYBOOK.md").exists())


def frontmatter(text):
    fm = {}
    if text.startswith("---"):
        end = text.find("\n---", 3)
        for line in text[3:end].strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip().strip('"')
        return fm, text[end + 4:]
    return fm, text


# ---------------------------------------------------------------------------
# alias: anonymize at write, reveal on screen
# ---------------------------------------------------------------------------

def aliases():
    return read_json(p("private", "aliases.json"), {"accounts": {}, "people": {}, "domains": {}})


def save_aliases(a):
    write_json(p("private", "aliases.json"), a)


def _next(pool, used):
    for cand in pool:
        if cand not in used:
            return cand
    n = 1
    while f"{pool[0]}{n}" in used:
        n += 1
    return f"{pool[0]}{n}"


def alias_add(real, kind, org=None, quiet=False):
    a = aliases()
    real = real.strip()
    bucket = {"account": "accounts", "person": "people", "domain": "domains"}[kind]
    if real in a[bucket]:
        if not quiet:
            print(f"already: {real} -> {a[bucket][real]['alias']}")
        return a[bucket][real]["alias"]
    used = {v["alias"] for b in a.values() for v in b.values()}
    if kind == "account":
        al = _next(ACCOUNT_ALIASES, used)
        a[bucket][real] = {"alias": al, "added": str(TODAY)}
    elif kind == "person":
        al = _next(PERSON_ALIASES, used)
        entry = {"alias": al, "added": str(TODAY)}
        if org:
            entry["org"] = org
        a[bucket][real] = entry
        first = real.split()[0]
        # first-name-only mentions map to the same alias when the first name is unambiguous
        firsts = [k.split()[0].lower() for k in a[bucket] if k != real]
        if " " in real and first.lower() not in firsts and first not in a[bucket]:
            a[bucket][first] = {"alias": al, "added": str(TODAY), "short_for": real}
    else:
        al = _next(ACCOUNT_ALIASES, used).lower() + ".example"
        a[bucket][real.lower()] = {"alias": al, "added": str(TODAY)}
    save_aliases(a)
    if not quiet:
        print(f"{real} -> {al}")
    return al


def _pairs(a, reverse=False):
    pairs = []
    for bucket in ("accounts", "people", "domains"):
        for real, v in a[bucket].items():
            pairs.append((real, v["alias"]))
    if reverse:
        pairs = [(al, real) for real, al in pairs if "short_for" not in a["people"].get(real, {})]
    pairs.sort(key=lambda x: -len(x[0]))
    return pairs


def anonymize(text):
    a = aliases()
    for real, al in _pairs(a):
        text = re.sub(r"(?<![\w.-])" + re.escape(real) + r"(?![\w-])", al, text, flags=re.I)
    text = EMAIL.sub("<email>", text)
    text = PHONE.sub("<phone>", text)
    text = ID_LINK.sub("<link>", text)
    return text


def reveal(text):
    a = aliases()
    for al, real in _pairs(a, reverse=True):
        text = re.sub(r"(?<![\w-])" + re.escape(al) + r"(?![\w-])", real, text)
    return text


def _learning_files():
    for rel in LEARNING_DIRS:
        path = O / rel
        if path.is_file():
            yield path
        elif path.is_dir():
            yield from (f for f in path.rglob("*") if f.is_file() and f.suffix in (".md", ".json", ".txt"))


def alias_audit(fix=False):
    a = aliases()
    reals = [(real, bucket) for bucket in ("accounts", "people", "domains") for real in a[bucket]]
    leaks = []
    for f in _learning_files():
        text = f.read_text(errors="ignore")
        for real, bucket in reals:
            if re.search(r"(?<![\w.-])" + re.escape(real) + r"(?![\w-])", text, re.I):
                leaks.append((f, real))
        if EMAIL.search(text):
            leaks.append((f, "<an email address>"))
        if fix:
            new = anonymize(text)
            if new != text:
                f.write_text(new)
    if leaks:
        for f, real in leaks:
            print(f"LEAK {f.relative_to(O)}: {real}")
        print(f"{len(leaks)} leak(s) in learning files." + (" Fixed in place." if fix else " Run with --fix."))
        return 0 if fix else 1
    print("no leaks: learning files carry aliases only")
    return 0


def alias_seed():
    """Register account names the overlay already knows (bold entries in in-motion.md, the watchlist)."""
    found = set()
    for rel in ("in-motion.md", "who.md", "customers.md"):
        f = O / rel
        if not f.exists():
            continue
        text = f.read_text()
        found.update(m.strip(" :") for m in re.findall(r"\*\*([^*\n]{2,40}?)[:*]", text))
        found.update(x.strip() for line in re.findall(r"^watchlist:(.*)$", text, re.M) for x in re.split(r"[;,]", re.sub(r"\([^)]*\)", "", line)))
    skip = re.compile(r"^(active|onboarding|quiet|churned|hot|gone|we owe|shape|gaps|delight|source|onboarding / early eval|quiet / dormant customers|churned / closed|active / engaged)", re.I)
    n = 0
    for name in sorted(found):
        if not name or skip.match(name) or len(name.split()) > 4 or re.search(r"[\d/()]", name) or name.lower() in ("sean", "us", "eng", "sean + eng"):
            continue
        alias_add(name, "account", quiet=True); n += 1
    print(f"seeded {n} account alias(es) from the overlay; add people with: engine.py alias add \"<Full Name>\" --kind person --org \"<Account>\"")
    return 0


def cmd_alias(a):
    if a.sub == "seed":
        return alias_seed()
    if a.sub == "drop":
        al = aliases()
        for bucket in ("accounts", "people", "domains"):
            for k in [k for k, v in al[bucket].items() if k == a.real or v.get("short_for") == a.real]:
                del al[bucket][k]; print(f"dropped {k}")
        save_aliases(al)
        return 0
    if a.sub == "add":
        alias_add(a.real, a.kind, a.org)
        return 0
    if a.sub == "list":
        al = aliases()
        for bucket in ("accounts", "people", "domains"):
            for real, v in al[bucket].items():
                if "short_for" in v:
                    continue
                print(f"{bucket[:-1]:8s} {real:32s} -> {v['alias']}" + (f"  ({v['org']})" if v.get("org") else ""))
        return 0
    if a.sub in ("apply", "reveal"):
        src = sys.stdin.read() if not a.file or a.file == "-" else Path(a.file).read_text()
        sys.stdout.write(anonymize(src) if a.sub == "apply" else reveal(src))
        return 0
    if a.sub == "audit":
        return alias_audit(fix=a.fix)
    return 2


# ---------------------------------------------------------------------------
# house: one file per moment; inherits the canon; diverges only with evidence
# ---------------------------------------------------------------------------

HOUSE_SECTIONS = [
    "## Our policy",
    "## Where we differ from the canon",
    "## What we actually sent (exemplars for this moment)",
    "## Runbook",
    "## Drill record",
    "## Counter-examples",
]


def house_path(moment):
    if moment not in moments():
        sys.exit(f"unknown moment {moment!r}; valid: {', '.join(moments())}")
    return p("house", f"{moment}.md")


def house_template(moment):
    title = moment.replace("-", " ")
    return (
        "---\n"
        f"moment: {moment}\n"
        f"inherits: moments/{moment}/PLAYBOOK.md\n"
        "confidence: low\n"
        "evidence: 0\n"
        "rules: 0\n"
        "drills_run: 0\n"
        "last_reinforced: never\n"
        "---\n"
        f"# How we do {title}\n\n"
        "Empty means: do what the canon says. Every line below is a divergence with evidence, a\n"
        "confirmation date, and an expiry. Names are aliases (`engine.py alias`); this file can leave the building.\n\n"
        "## Our policy\n\n(from overlay/policies.md and overlay/authority.md, only what applies to this moment)\n\n"
        "## Where we differ from the canon\n\n"
        "## What we actually sent (exemplars for this moment)\n\n"
        "## Runbook\n\n(written the second time this is done by hand; steps, what goes wrong, when to escalate instead)\n\n"
        "## Drill record\n\n"
        "## Counter-examples\n\n(denied proposals; the engine never re-proposes these)\n"
    )


def _rules(text):
    """Confirmed and unconfirmed rule lines under 'Where we differ'."""
    sec = _section(text, "## Where we differ from the canon")
    return [l for l in sec.splitlines() if l.startswith("- [")]


def _section(text, heading):
    start = text.find(heading)
    if start == -1:
        return ""
    nxt = text.find("\n## ", start + len(heading))
    return text[start + len(heading):nxt if nxt != -1 else None]


def _replace_section(text, heading, body):
    start = text.find(heading)
    if start == -1:
        return text.rstrip("\n") + f"\n\n{heading}\n{body}\n"
    nxt = text.find("\n## ", start + len(heading))
    tail = text[nxt:] if nxt != -1 else "\n"
    return text[:start] + heading + "\n" + body.rstrip("\n") + "\n" + tail


def _append_to_section(text, heading, line):
    sec = _section(text, heading)
    # drop the parenthetical placeholder once real content lands
    lines = [l for l in sec.strip("\n").splitlines() if not (l.startswith("(") and l.endswith(")"))]
    lines.append(line)
    return _replace_section(text, heading, "\n" + "\n".join(lines) + "\n")


def _recompute(moment):
    path = house_path(moment)
    text = path.read_text()
    fm, body = frontmatter(text)
    rules = _rules(text)
    confirmed = [r for r in rules if "confirmed" in r]
    evidence = sum(int(m.group(1)) for r in rules for m in [re.search(r"evidence: (\d+)", r)] if m)
    drills = len([l for l in _section(text, "## Drill record").splitlines() if l.startswith("- [")])
    conf = next(label for n, label in CONFIDENCE if len(confirmed) >= n)
    dates = re.findall(r"reinforced: (\d{4}-\d{2}-\d{2})", text)
    fm.update({
        "confidence": conf, "evidence": str(evidence), "rules": str(len(confirmed)),
        "drills_run": str(drills), "last_reinforced": max(dates) if dates else "never",
    })
    head = "---\n" + "\n".join(f"{k}: {v}" for k, v in fm.items()) + "\n---"
    path.write_text(head + body)
    return fm


def house_init(quiet=False):
    made = 0
    for m in moments():
        path = p("house", f"{m}.md")
        if not path.exists():
            path.write_text(house_template(m))
            made += 1
    house_index()
    if not quiet:
        print(f"house: {made} file(s) created, {len(moments())} moments total -> {O / 'house'}")


def house_status(rows=None):
    rows = rows or []
    for m in moments():
        path = p("house", f"{m}.md")
        if not path.exists():
            rows.append((m, "missing", "0", "0", "0", "never"))
            continue
        fm = _recompute(m)
        rows.append((m, fm["confidence"], fm["rules"], fm["evidence"], fm["drills_run"], fm["last_reinforced"]))
    return rows


def house_index():
    rows = house_status()
    lines = ["# House index (generated by engine.py house index)", "",
             "Confidence is computed from confirmed rules: low under 3, medium 3 to 6, high 7 and up.",
             "A low silo is running on the canon's defaults. Drills pick the lowest first.", "",
             "| Moment | Confidence | Rules | Evidence | Drills | Last reinforced |", "|---|---|---|---|---|---|"]
    for r in rows:
        lines.append("| " + " | ".join(r) + " |")
    p("house", "README.md").write_text("\n".join(lines) + "\n")
    # keep overlay/learned.md as a pointer so older loading rules still resolve
    p("learned.md").write_text("# Learned rules\n\nSplit by moment into `overlay/house/<moment>.md` (see `overlay/house/README.md`). Managed by scripts/engine.py.\n")
    return rows


def house_add(moment, rule, evidence=2, source=None, confirmed=False, quiet=False):
    path = house_path(moment)
    if not path.exists():
        house_init(quiet=True)
    total = sum(len([r for r in _rules(p("house", f"{m}.md").read_text()) if "confirmed" in r]) for m in moments() if p("house", f"{m}.md").exists())
    if confirmed and total >= RULE_CAP_TOTAL:
        print(f"house holds {RULE_CAP_TOTAL} confirmed rules; retire one first (engine.py house drop)")
        return 1
    text = path.read_text()
    meta = f"evidence: {evidence}, reinforced: {TODAY}, expires: {TODAY + dt.timedelta(days=RULE_TTL_DAYS)}"
    if source:
        meta = f"source: {anonymize(source)}, " + meta
    meta = (f"confirmed {TODAY}, " if confirmed else "UNCONFIRMED, ") + meta
    line = f"- [{TODAY}] {anonymize(rule.strip())} ({meta})"
    text = _append_to_section(text, "## Where we differ from the canon", line)
    path.write_text(text)
    _recompute(moment)
    house_index()
    if not quiet:
        print("house: " + line)
    return 0


def house_deny(moment, proposal, why):
    path = house_path(moment)
    if not path.exists():
        house_init(quiet=True)
    line = f"- [{TODAY}] DENIED: {anonymize(proposal.strip())} (why: {anonymize(why.strip())})"
    path.write_text(_append_to_section(path.read_text(), "## Counter-examples", line))
    house_index()
    print("house: " + line)
    return 0


def house_denied_before(moment, proposal):
    path = p("house", f"{moment}.md")
    if not path.exists():
        return False
    key = slug(anonymize(proposal))[:60]
    for l in _section(path.read_text(), "## Counter-examples").splitlines():
        if l.startswith("- [") and "DENIED:" in l:
            body = l.split("DENIED:", 1)[1].split("(why:")[0]
            if slug(body)[:60] == key or difflib.SequenceMatcher(None, slug(body), slug(anonymize(proposal))).ratio() > 0.85:
                return True
    return False


def house_rule_edit(moment, n, drop=False):
    path = house_path(moment)
    text = path.read_text()
    rules = _rules(text)
    if n < 1 or n > len(rules):
        print(f"no rule {n}; {moment} has {len(rules)}")
        return 1
    old = rules[n - 1]
    if drop:
        text = text.replace(old + "\n", "")
        print("dropped: " + old)
    else:
        ev = int(re.search(r"evidence: (\d+)", old).group(1)) + 1
        new = re.sub(r"evidence: \d+", f"evidence: {ev}", old)
        new = re.sub(r"reinforced: \d{4}-\d{2}-\d{2}", f"reinforced: {TODAY}", new)
        new = re.sub(r"expires: \d{4}-\d{2}-\d{2}", f"expires: {TODAY + dt.timedelta(days=RULE_TTL_DAYS)}", new)
        new = new.replace("UNCONFIRMED, ", f"confirmed {TODAY}, ") if "UNCONFIRMED" in new else new
        text = text.replace(old, new)
        print("reinforced: " + new)
    path.write_text(text)
    _recompute(moment)
    house_index()
    return 0


def house_expiring(days=14):
    out = []
    for m in moments():
        path = p("house", f"{m}.md")
        if not path.exists():
            continue
        for i, r in enumerate(_rules(path.read_text()), 1):
            mm = re.search(r"expires: (\d{4}-\d{2}-\d{2})", r)
            if mm and (dt.date.fromisoformat(mm.group(1)) - TODAY).days <= days:
                out.append((m, i, r))
    for m, i, r in out:
        print(f"{m} #{i}: {r}")
    if not out:
        print(f"no rules expiring within {days} days")
    return out


def house_exemplar(moment, file, why):
    path = house_path(moment)
    if not path.exists():
        house_init(quiet=True)
    body = anonymize(Path(file).read_text().strip())
    quoted = "\n".join("> " + l for l in body.splitlines())
    entry = f"### {TODAY}\n{quoted}\n\n**Why it works:** {anonymize(why.strip())}\n"
    text = path.read_text()
    sec = _section(text, "## What we actually sent (exemplars for this moment)").strip("\n")
    text = _replace_section(text, "## What we actually sent (exemplars for this moment)", "\n" + (sec + "\n\n" if sec else "") + entry)
    path.write_text(text)
    print(f"house: exemplar added to {moment}")
    return 0


def cmd_house(a):
    if a.sub == "init":
        house_init(); return 0
    if a.sub in ("status", "index"):
        rows = house_index()
        print(f"{'moment':34s} {'conf':7s} rules evid drills reinforced")
        for r in rows:
            print(f"{r[0]:34s} {r[1]:7s} {r[2]:>5s} {r[3]:>4s} {r[4]:>6s} {r[5]}")
        return 0
    if a.sub == "add":
        return house_add(a.moment, a.rule, a.evidence, a.source, a.confirmed)
    if a.sub == "deny":
        return house_deny(a.moment, a.rule, a.why)
    if a.sub == "reinforce":
        return house_rule_edit(a.moment, a.n)
    if a.sub == "drop":
        return house_rule_edit(a.moment, a.n, drop=True)
    if a.sub == "expiring":
        house_expiring(a.days); return 0
    if a.sub == "exemplar":
        return house_exemplar(a.moment, a.file, a.why)
    return 2


# ---------------------------------------------------------------------------
# queue: proposals the sweep raises, the operator decides
# ---------------------------------------------------------------------------

def queue():
    return read_json(p("queue", "proposals.json"), [])


def save_queue(q):
    write_json(p("queue", "proposals.json"), q)
    pending = [x for x in q if x["status"] == "pending"]
    lines = [f"# Proposals awaiting a decision ({len(pending)})", ""]
    for x in pending:
        lines.append(f"- **{x['id']}** [{x['moment']} / {x['kind']}] {x['text']} (evidence: {x['evidence']}; {x['source']})")
    p("queue", "PENDING.md").write_text("\n".join(lines) + "\n")


def queue_add(moment, kind, text, evidence=1, source=""):
    if kind == "rule" and moment != "all" and house_denied_before(moment, text):
        print("refused: denied before (see the moment's Counter-examples)")
        return 1
    q = queue()
    text_a = anonymize(text.strip())
    for x in q:
        if x["moment"] == moment and difflib.SequenceMatcher(None, x["text"].lower(), text_a.lower()).ratio() > 0.85:
            if x["status"] == "pending":
                x["evidence"] = max(x["evidence"], evidence) if evidence > 1 else x["evidence"] + 1
                x["source"] = (x["source"] + "; " + anonymize(source)).strip("; ")
                save_queue(q)
                print(f"reinforced pending proposal {x['id']} (evidence now {x['evidence']})")
                return 0
            if x["status"] in ("denied",):
                print(f"refused: {x['id']} was denied on {x['decided']}")
                return 1
    pid = f"{TODAY}-{len([x for x in q if x['id'].startswith(str(TODAY))]) + 1:02d}"
    q.append({"id": pid, "raised": str(TODAY), "moment": moment, "kind": kind, "text": text_a,
              "evidence": evidence, "source": anonymize(source), "status": "pending", "decided": None, "why": None})
    save_queue(q)
    print(f"queued {pid}: {text_a}")
    return 0


def queue_decide(pid, decision, text=None, why=None):
    q = queue()
    x = next((x for x in q if x["id"] == pid), None)
    if not x:
        print(f"no proposal {pid}")
        return 1
    if decision == "later":
        x["status"] = "later"; x["decided"] = str(TODAY)
    elif decision == "deny":
        x["status"] = "denied"; x["decided"] = str(TODAY); x["why"] = anonymize(why or "")
        if x["kind"] == "rule" and x["moment"] != "all":
            house_deny(x["moment"], x["text"], why or "denied at lineup")
    else:  # approve / reword
        final = anonymize(text.strip()) if (decision == "reword" and text) else x["text"]
        x["status"] = "approved"; x["decided"] = str(TODAY); x["final"] = final
        if x["kind"] == "rule" and x["moment"] != "all":
            house_add(x["moment"], final, evidence=max(2, x["evidence"]), source=x["source"], confirmed=True, quiet=True)
        elif x["kind"] == "lexicon":
            with p("lexicon.md").open("a") as f:
                f.write(f"- [{TODAY}] {final}\n")
        elif x["kind"] == "method":
            with p("method.md").open("a") as f:
                f.write(f"\n- [{TODAY}] {final} [confirmed {TODAY}]\n")
        else:  # new-situation: recorded for the drill bank and a future silo
            with p("drills", "new-situations.md").open("a") as f:
                f.write(f"- [{TODAY}] {x['moment']}: {final}\n")
    save_queue(q)
    print(f"{pid}: {x['status']}")
    return 0


def cmd_queue(a):
    if a.sub == "add":
        return queue_add(a.moment, a.kind, a.text, a.evidence, a.source or "")
    if a.sub == "list":
        for x in queue():
            if a.all or x["status"] == "pending":
                print(f"{x['id']}  {x['status']:8s} [{x['moment']}/{x['kind']}] ev{x['evidence']}  {x['text']}")
        return 0
    if a.sub == "decide":
        return queue_decide(a.id, a.decision, a.text, a.why)
    return 2


# ---------------------------------------------------------------------------
# drafts: hold, then let the sweep read the operator's edit
# ---------------------------------------------------------------------------

def drafts_hold(a):
    d = p("drafts", str(TODAY), f"{slug(a.account)}-{slug(a.moment)}-{slug(a.thread)[:24] or 'thread'}.md")
    body = Path(a.file).read_text().strip() if a.file != "-" else sys.stdin.read().strip()
    d.write_text(
        "---\n"
        f"status: held\nheld: {NOW.isoformat(timespec='minutes')}\naccount: {a.account}\nperson: {a.person}\n"
        f"channel: {a.channel}\nmoment: {a.moment}\nthread: {a.thread}\nresolved: null\noutcome: null\n"
        "---\n" + body + "\n"
    )
    print(f"held {d.relative_to(O)}")
    return 0


def drafts_list(show_all=False):
    out = []
    for f in sorted(p("drafts").rglob("*.md")):
        fm, _ = frontmatter(f.read_text())
        if show_all or fm.get("status") == "held":
            out.append((f, fm))
    return out


def drafts_resolve(a):
    f = Path(a.path) if Path(a.path).exists() else O / a.path
    text = f.read_text()
    fm, body = frontmatter(text)
    body = body.strip()
    diff = ""
    if a.outcome == "edited":
        sent = Path(a.sent_file).read_text().strip() if a.sent_file else ""
        if sent:
            d = [l for l in difflib.unified_diff(body.splitlines(), sent.splitlines(), lineterm="", n=0) if l[:1] in "+-" and l[:3] not in ("+++", "---")]
            diff = " | ".join(d)[:400]
            survival = difflib.SequenceMatcher(None, body, sent).ratio()
        else:
            survival = None
    else:
        survival = 1.0 if a.outcome == "sent-as-is" else 0.0
    fm.update({"status": "resolved", "resolved": str(TODAY), "outcome": a.outcome, "survival": f"{survival:.2f}" if survival is not None else "null"})
    head = "---\n" + "\n".join(f"{k}: {v}" for k, v in fm.items()) + "\n---\n"
    f.write_text(head + body + "\n")
    outcome = {"sent-as-is": "approved", "edited": "edited", "not-sent": "rejected"}[a.outcome]
    journal(fm.get("moment", "small-moment"), fm.get("channel", "email"), outcome, a.score, a.lesson or f"draft {a.outcome}", diff or None)
    print(f"resolved {f.name}: {a.outcome}" + (f", survival {survival:.2f}" if survival is not None else ""))
    return 0


def cmd_drafts(a):
    if a.sub == "hold":
        return drafts_hold(a)
    if a.sub == "list":
        for f, fm in drafts_list(a.all):
            print(f"{fm.get('status','?'):8s} {f.relative_to(O)}  [{fm.get('moment')}/{fm.get('channel')}] {fm.get('account')} / {fm.get('person')}  thread={fm.get('thread')}")
        return 0
    if a.sub == "resolve":
        return drafts_resolve(a)
    return 2


# ---------------------------------------------------------------------------
# journal: the operator's edit is the ground truth (anonymized)
# ---------------------------------------------------------------------------

def journal(moment, channel, outcome, score, lesson, diff=None):
    f = p("journal", f"{TODAY}.md")
    if not f.exists():
        f.write_text(f"# Journal {TODAY}\n\n")
    line = f"- {NOW.strftime('%H:%M')} {moment} / {channel} / {outcome} / score {score if score is not None else '-'}: {anonymize(lesson)}"
    if diff:
        line += f"\n  diff: {anonymize(diff)}"
    with f.open("a") as fh:
        fh.write(line + "\n")
    return line


def cmd_journal(a):
    print(journal(a.moment, a.channel, a.outcome, a.score, a.lesson, a.diff))
    return 0


# ---------------------------------------------------------------------------
# ledger: every surfaced pick is a prediction that gets graded
# ---------------------------------------------------------------------------

VERDICTS = ["right", "premature", "wrong", "noise", "superseded"]


def ledger():
    return read_json(p("ledger.json"), [])


def ledger_append(brief_path):
    doc = json.loads(Path(brief_path).read_text())
    stem = Path(brief_path).stem[:10]
    date = stem if re.fullmatch(r"\d{4}-\d{2}-\d{2}", stem) else doc.get("date", str(TODAY))
    rows = ledger()
    known = {r["id"] for r in rows}
    added = 0
    for s in doc.get("surfaced", doc.get("brief", {}).get("surfaced", [])):
        rid = f"{date}::{slug(s.get('account', 'unknown'))}::{s.get('rank', 0)}"
        if rid in known:
            continue
        rows.append({"id": rid, "date_surfaced": date, "account": s.get("account", "unknown"), "rank": s.get("rank", 0),
                     "headline": s.get("headline", ""), "recommended_move": s.get("recommended_move", ""),
                     "why_now": s.get("why_now", ""), "moment": s.get("moment"),
                     "outcome": {"reviewed_on": None, "acted": None, "verdict": None, "note": None}})
        added += 1
    write_json(p("ledger.json"), rows)
    print(f"ledger: +{added} pick(s) from {Path(brief_path).name}; {len(rows)} rows")
    return 0


def ledger_pending():
    return [r for r in ledger() if r.get("kind") != "miss" and r["outcome"]["reviewed_on"] is None]


def cmd_ledger(a):
    if a.sub == "append":
        return ledger_append(a.brief)
    if a.sub == "list":
        pend = ledger_pending()
        if not pend:
            print("no pending picks")
        for r in pend:
            print(f"  {r['id']}  [{r['account']}]  {r['headline'][:90]}")
        return 0
    if a.sub == "grade":
        rows = ledger()
        hit = next((r for r in rows if r["id"] == a.id), None)
        if not hit:
            print(f"no ledger row {a.id!r}"); return 1
        hit["outcome"] = {"reviewed_on": str(TODAY), "acted": None if a.acted is None else a.acted == "yes", "verdict": a.verdict, "note": a.note}
        write_json(p("ledger.json"), rows)
        print(f"graded {a.id}: acted={a.acted} verdict={a.verdict}")
        return 0
    if a.sub == "miss":
        rows = ledger()
        rows.append({"id": f"{TODAY}::MISS::{slug(a.account)}", "date_surfaced": None, "account": a.account, "kind": "miss",
                     "headline": a.note, "outcome": {"reviewed_on": str(TODAY), "acted": None, "verdict": "wrong", "note": a.note}})
        write_json(p("ledger.json"), rows)
        print(f"logged a MISS on {a.account}")
        return 0
    return 2


# ---------------------------------------------------------------------------
# drill: manufacture volume; the operator's answer is the label
# ---------------------------------------------------------------------------

def scenarios():
    """Public bank (drills/bank) plus canon eval cases (gold hidden until recorded)."""
    out = []
    for f in sorted((CANON / "drills" / "bank").glob("*.md")) if (CANON / "drills" / "bank").exists() else []:
        fm, _ = frontmatter(f.read_text())
        out.append({"id": fm.get("id", f.stem), "moment": fm.get("moment"), "path": str(f.relative_to(CANON)), "kind": "bank", "difficulty": fm.get("difficulty", "")})
    for f in sorted((CANON / "evals" / "cases").glob("*.md")):
        fm, _ = frontmatter(f.read_text())
        out.append({"id": f"case-{fm.get('id', f.stem)}", "moment": fm.get("moment"), "path": str(f.relative_to(CANON)), "kind": "case", "difficulty": fm.get("difficulty", "")})
    return out


def drill_log():
    return read_json(p("drills", "log.json"), [])


def drill_next(n=3):
    house_init(quiet=True)
    conf_rank = {"low": 0, "medium": 1, "high": 2}
    rows = {r[0]: (conf_rank[r[1]], int(r[3])) for r in house_status()}
    done = {d["scenario"] for d in drill_log()}
    cands = [s for s in scenarios() if s["id"] not in done and s["moment"] in rows]
    cands.sort(key=lambda s: (rows[s["moment"]][0], rows[s["moment"]][1], s["moment"], s["kind"] != "bank", s["id"]))
    picked, seen = [], set()
    for s in cands:
        if s["moment"] in seen and len(cands) > n:
            continue
        picked.append(s); seen.add(s["moment"])
        if len(picked) == n:
            break
    if not picked:
        print("every scenario has been drilled; add to drills/bank/ or write new situations from the queue")
        return 0
    for s in picked:
        print(f"{s['id']:28s} {s['moment']:32s} {s['difficulty']:7s} {s['path']}")
    return 0


def drill_record(a):
    path = house_path(a.moment)
    if not path.exists():
        house_init(quiet=True)
    line = f"- [{TODAY}] {a.scenario}: house draft {a.house_score}/18, operator {a.operator_score}/18. Delta: {anonymize(a.delta.strip())}"
    if a.rule:
        line += " Rule confirmed below."
    path.write_text(_append_to_section(path.read_text(), "## Drill record", line))
    if a.rule:
        house_add(a.moment, a.rule, evidence=1, source=f"drill {a.scenario}", confirmed=True, quiet=True)
    log = drill_log()
    log.append({"date": str(TODAY), "scenario": a.scenario, "moment": a.moment, "house_score": a.house_score, "operator_score": a.operator_score})
    write_json(p("drills", "log.json"), log)
    if a.answer_file:
        src = next((s for s in scenarios() if s["id"] == a.scenario), None)
        base = (CANON / src["path"]).read_text() if src else f"---\nid: {a.scenario}\nmoment: {a.moment}\n---\n"
        base = re.split(r"\n## Gold reply", base)[0].rstrip("\n")
        answer = anonymize(Path(a.answer_file).read_text().strip())
        case = p("evals", "cases", f"{slug(a.scenario)}.md")
        case.write_text(anonymize(base) + "\n\n## Gold reply (the operator's own, from a drill)\n\n" + "\n".join("> " + l for l in answer.splitlines()) + f"\n\n## Notes for the judge\n\nRecorded {TODAY}. Delta from the house draft: {anonymize(a.delta.strip())}\n")
        print(f"private eval case written: {case.relative_to(O)}")
    _recompute(a.moment)
    house_index()
    print("drill: " + line)
    return 0


def cmd_drill(a):
    if a.sub == "next":
        return drill_next(a.n)
    if a.sub == "record":
        return drill_record(a)
    return 2


# ---------------------------------------------------------------------------
# heartbeat + watermark + status
# ---------------------------------------------------------------------------

def hb():
    return read_json(p("state", "heartbeat.json"), {})


def cmd_heartbeat(a):
    h = hb()
    if a.sub == "start":
        h.update({"started": NOW.isoformat(timespec="seconds"), "ended": None, "signal": None})
    elif a.sub == "end":
        h.update({"ended": NOW.isoformat(timespec="seconds"), "signal": a.signal})
    write_json(p("state", "heartbeat.json"), h)
    if a.sub == "check":
        print(heartbeat_line())
    return 0


def heartbeat_line():
    h = hb()
    if not h.get("started"):
        return "sweep has never run"
    started = dt.datetime.fromisoformat(h["started"])
    if h.get("ended"):
        ended = dt.datetime.fromisoformat(h["ended"])
        age = NOW - ended
        when = ended.strftime("%a %H:%M") if age.days < 1 else f"{age.days}d ago"
        stale = age > dt.timedelta(hours=30) and NOW.weekday() < 5
        return ("SWEEP STALE, last ran " if stale else "sweep ran ") + when + (f": {h['signal']}" if h.get("signal") else "")
    if NOW - started > dt.timedelta(hours=2):
        return f"SWEEP DID NOT FINISH (started {started.strftime('%a %H:%M')})"
    return f"sweep running since {started.strftime('%H:%M')}"


def cmd_watermark(a):
    f = p("state", "watermark.txt")
    if a.sub == "set":
        f.write_text(a.value.strip() + "\n"); print(f"watermark {a.value}")
    else:
        print(f.read_text().strip() if f.exists() else (NOW - dt.timedelta(days=1)).isoformat(timespec="seconds"))
    return 0


def drill_due():
    log = drill_log()
    if not log:
        return True
    last = max(dt.date.fromisoformat(d["date"]) for d in log)
    return (TODAY - last).days >= 7


def scorecard(print_it=True):
    resolved = [fm for _, fm in drafts_list(True) if fm.get("status") == "resolved" and fm.get("survival") not in (None, "null")]
    surv = [float(fm["survival"]) for fm in resolved]
    rows = ledger()
    reviewed = [r for r in rows if r.get("kind") != "miss" and r["outcome"]["reviewed_on"]]
    right = sum(1 for r in reviewed if r["outcome"]["verdict"] == "right")
    misses = [r for r in rows if r.get("kind") == "miss"]
    house = house_status()
    out = {
        "draft_survival": (sum(surv) / len(surv)) if surv else None, "drafts_resolved": len(resolved),
        "pick_precision": (right / len(reviewed)) if reviewed else None, "picks_reviewed": len(reviewed), "misses": len(misses),
        "house": {r[0]: r[1] for r in house},
    }
    if print_it:
        pct = lambda x: "  —" if x is None else f"{100 * x:3.0f}%"
        print("─" * 56)
        print("  FRONT OF HOUSE, THE TWO NUMBERS")
        print("─" * 56)
        print(f"  draft survival   {pct(out['draft_survival'])}   (share of a held draft that went out untouched; {len(resolved)} resolved)")
        print(f"  pick precision   {pct(out['pick_precision'])}   (surfaced picks graded right; {len(reviewed)} reviewed, {len(misses)} misses)")
        print("─" * 56)
        by = {}
        for m, c in out["house"].items():
            by.setdefault(c, []).append(m)
        for c in ("high", "medium", "low"):
            if by.get(c):
                print(f"  house {c:6s} {len(by[c]):2d}: " + ", ".join(by[c]))
        print("─" * 56)
    return out


def cmd_status(a):
    picks = len(ledger_pending())
    props = len([x for x in queue() if x["status"] == "pending"])
    held = len(drafts_list())
    due = drill_due()
    if a.brief:
        bits = []
        if picks: bits.append(f"{picks} pick{'s' if picks != 1 else ''} to grade")
        if props: bits.append(f"{props} proposal{'s' if props != 1 else ''}")
        if held: bits.append(f"{held} draft{'s' if held != 1 else ''} held")
        if due: bits.append("drill due")
        head = ", ".join(bits) if bits else "quiet"
        print(f"Front of House: {head}. {heartbeat_line()}." + (" Run /lineup." if bits else ""))
        return 0
    print(f"overlay:        {O}")
    print(f"heartbeat:      {heartbeat_line()}")
    print(f"picks pending:  {picks}")
    print(f"proposals:      {props}")
    print(f"drafts held:    {held}")
    print(f"drill due:      {'yes' if due else 'no'}")
    scorecard()
    return 0


# ---------------------------------------------------------------------------

def main():
    global O
    O = overlay_dir()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("status"); s.add_argument("--brief", action="store_true"); s.set_defaults(fn=cmd_status)
    s = sub.add_parser("scorecard"); s.set_defaults(fn=lambda a: (scorecard(), 0)[1])

    s = sub.add_parser("alias"); ss = s.add_subparsers(dest="sub", required=True)
    x = ss.add_parser("add"); x.add_argument("real"); x.add_argument("--kind", required=True, choices=["account", "person", "domain"]); x.add_argument("--org")
    ss.add_parser("list"); ss.add_parser("seed"); x = ss.add_parser("drop"); x.add_argument("real")
    x = ss.add_parser("apply"); x.add_argument("file", nargs="?")
    x = ss.add_parser("reveal"); x.add_argument("file", nargs="?")
    x = ss.add_parser("audit"); x.add_argument("--fix", action="store_true")
    s.set_defaults(fn=cmd_alias)

    s = sub.add_parser("house"); ss = s.add_subparsers(dest="sub", required=True)
    ss.add_parser("init"); ss.add_parser("status"); ss.add_parser("index")
    x = ss.add_parser("add"); x.add_argument("moment"); x.add_argument("rule"); x.add_argument("--evidence", type=int, default=2); x.add_argument("--source"); x.add_argument("--confirmed", action="store_true")
    x = ss.add_parser("deny"); x.add_argument("moment"); x.add_argument("rule"); x.add_argument("--why", required=True)
    x = ss.add_parser("reinforce"); x.add_argument("moment"); x.add_argument("n", type=int)
    x = ss.add_parser("drop"); x.add_argument("moment"); x.add_argument("n", type=int)
    x = ss.add_parser("expiring"); x.add_argument("--days", type=int, default=14)
    x = ss.add_parser("exemplar"); x.add_argument("moment"); x.add_argument("--file", required=True); x.add_argument("--why", required=True)
    s.set_defaults(fn=cmd_house)

    s = sub.add_parser("queue"); ss = s.add_subparsers(dest="sub", required=True)
    x = ss.add_parser("add"); x.add_argument("--moment", required=True); x.add_argument("--kind", required=True, choices=["rule", "new-situation", "method", "lexicon"]); x.add_argument("--text", required=True); x.add_argument("--evidence", type=int, default=1); x.add_argument("--source")
    x = ss.add_parser("list"); x.add_argument("--all", action="store_true")
    x = ss.add_parser("decide"); x.add_argument("id"); x.add_argument("decision", choices=["approve", "deny", "later", "reword"]); x.add_argument("--text"); x.add_argument("--why")
    s.set_defaults(fn=cmd_queue)

    s = sub.add_parser("drafts"); ss = s.add_subparsers(dest="sub", required=True)
    x = ss.add_parser("hold")
    for f in ["--account", "--person", "--channel", "--moment", "--thread", "--file"]:
        x.add_argument(f, required=True)
    x = ss.add_parser("list"); x.add_argument("--all", action="store_true")
    x = ss.add_parser("resolve"); x.add_argument("path"); x.add_argument("--outcome", required=True, choices=["sent-as-is", "edited", "not-sent"]); x.add_argument("--sent-file"); x.add_argument("--lesson"); x.add_argument("--score", type=int)
    s.set_defaults(fn=cmd_drafts)

    s = sub.add_parser("journal")
    for f in ["--moment", "--channel", "--outcome", "--lesson"]:
        s.add_argument(f, required=True)
    s.add_argument("--score", type=int); s.add_argument("--diff"); s.set_defaults(fn=cmd_journal)

    s = sub.add_parser("ledger"); ss = s.add_subparsers(dest="sub", required=True)
    x = ss.add_parser("append"); x.add_argument("brief")
    ss.add_parser("list")
    x = ss.add_parser("grade"); x.add_argument("id"); x.add_argument("--verdict", required=True, choices=VERDICTS); x.add_argument("--acted", choices=["yes", "no"]); x.add_argument("--note")
    x = ss.add_parser("miss"); x.add_argument("account"); x.add_argument("note")
    s.set_defaults(fn=cmd_ledger)

    s = sub.add_parser("drill"); ss = s.add_subparsers(dest="sub", required=True)
    x = ss.add_parser("next"); x.add_argument("--n", type=int, default=3)
    x = ss.add_parser("record"); x.add_argument("--scenario", required=True); x.add_argument("--moment", required=True); x.add_argument("--house-score", type=int, required=True); x.add_argument("--operator-score", type=int, required=True); x.add_argument("--delta", required=True); x.add_argument("--rule"); x.add_argument("--answer-file")
    s.set_defaults(fn=cmd_drill)

    s = sub.add_parser("heartbeat"); ss = s.add_subparsers(dest="sub", required=True)
    ss.add_parser("start"); x = ss.add_parser("end"); x.add_argument("--signal", default="")
    x = ss.add_parser("check"); x.add_argument("--brief", action="store_true")
    s.set_defaults(fn=cmd_heartbeat)

    s = sub.add_parser("watermark"); ss = s.add_subparsers(dest="sub", required=True)
    ss.add_parser("get"); x = ss.add_parser("set"); x.add_argument("value")
    s.set_defaults(fn=cmd_watermark)

    a = ap.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())

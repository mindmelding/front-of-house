#!/usr/bin/env python3
"""fohcheck: the Front of House lexicon validator.

Reads the banned lists from voice/LEXICON.md (single source: the same file the
prompt loads) and checks a draft reply, or the whole repo, for violations.

  fohcheck.py reply.md            strict: check a draft (openers, phrases, words, patterns)
  fohcheck.py - < reply.md        strict, from stdin
  fohcheck.py --repo              lenient: check the canon's own prose, skipping
                                  intentional "Bad" examples, hall-of-shame, and
                                  the lexicon itself

Exit 0 when clean, 1 when violations are found. Prints path:line: rule: match.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEXICON = ROOT / "voice" / "LEXICON.md"

REPO_SKIP_FILES = {
    "voice/LEXICON.md",
    "voice/ai-tells.md",
}
REPO_SKIP_DIRS = ("examples/hall-of-shame", "adapters", ".git", "inbox", "node_modules")
# Headings whose section (until the next heading) is intentionally allowed to contain banned language.
ALLOWED_SECTION_HEADINGS = re.compile(
    r"^#{1,6}\s+.*(bad|ordinary company|what happened|incoming message|banned|instead of|anti-tells|don'?t\b|hall of shame|the customer'?s message|what an ordinary)",
    re.I,
)
# Inline markers that allow the rest of the paragraph.
# In lenient mode, a banned phrase inside double quotes is a mention, not a use.
QUOTED = re.compile(r'"[^"\n]*"|“[^”\n]*”')
ALLOWED_LINE = re.compile(r"^\s*(>\s*)?(\*\*Bad\b|Bad[.:]|\*\*Ordinary\b|<!--\s*foh:allow\s*-->)", re.I)


def load_lexicon():
    text = LEXICON.read_text(encoding="utf-8")
    blocks = {}
    for m in re.finditer(r"```(banned-[a-z]+)\n(.*?)```", text, re.S):
        blocks[m.group(1)] = [l.strip() for l in m.group(2).splitlines() if l.strip()]
    phrases = [re.compile(r"(?<!\w)" + re.escape(p) + r"(?!\w)", re.I) for p in blocks.get("banned-phrases", [])]
    words = [re.compile(r"\b" + re.escape(w) + r"\b", re.I) for w in blocks.get("banned-words", [])]
    openers = [re.compile(r"^\s*" + re.escape(o) + r"\b", re.I) for o in blocks.get("banned-openers", [])]
    patterns = [re.compile(p, re.M) for p in blocks.get("banned-patterns", [])]
    return phrases, words, openers, patterns, blocks


def strip_code_and_frontmatter(text):
    lines = text.splitlines()
    out = []
    in_code = False
    i = 0
    if lines and lines[0].strip() == "---":
        # skip YAML frontmatter
        i = 1
        while i < len(lines) and lines[i].strip() != "---":
            i += 1
        i += 1
        out.extend([""] * i)
    while i < len(lines):
        l = lines[i]
        if l.strip().startswith("```"):
            in_code = not in_code
            out.append("")
        elif in_code:
            out.append("")
        else:
            out.append(l)
        i += 1
    return out


def check_lines(lines, lex, strict, path):
    phrases, words, openers, patterns, blocks = lex
    violations = []
    allowed_section = False
    allowed_para = False
    first_content_seen = False
    for n, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("#"):
            allowed_section = bool(ALLOWED_SECTION_HEADINGS.match(stripped)) if not strict else False
            allowed_para = False
            continue
        if not stripped:
            allowed_para = False
            continue
        if not strict and (allowed_section or allowed_para or ALLOWED_LINE.match(line)):
            if ALLOWED_LINE.match(line):
                allowed_para = True
            continue
        if strict and not first_content_seen and not stripped.startswith(("Subject:", ">", "|")):
            first_content_seen = True
            for o, raw in zip(openers, blocks.get("banned-openers", [])):
                if o.match(stripped):
                    violations.append((path, n, "opener", raw))
        target = line if strict else QUOTED.sub("", line)
        for p, raw in zip(phrases, blocks.get("banned-phrases", [])):
            if p.search(target):
                violations.append((path, n, "phrase", raw))
        for w, raw in zip(words, blocks.get("banned-words", [])):
            if w.search(target):
                violations.append((path, n, "word", raw))
    joined = "\n".join(l if not (ALLOWED_LINE.match(l)) else "" for l in lines) if not strict else "\n".join(lines)
    for pat, raw in zip(patterns, blocks.get("banned-patterns", [])):
        if not strict and raw.startswith("(\\n\\s*[-*]"):
            continue  # stacked-bullet rule is for replies, not guides
        for m in pat.finditer(joined):
            ln = joined.count("\n", 0, m.start()) + 1
            # skip matches inside allowed sections in lenient mode
            if not strict and _in_allowed_section(lines, ln):
                continue
            violations.append((path, ln, "pattern", raw))
    return violations


def _in_allowed_section(lines, ln):
    allowed = False
    for i in range(ln):
        s = lines[i].strip() if i < len(lines) else ""
        if s.startswith("#"):
            allowed = bool(ALLOWED_SECTION_HEADINGS.match(s))
        elif ALLOWED_LINE.match(lines[i]) and i + 1 >= ln - 3:
            return True
    return allowed


def check_file(path, lex, strict):
    text = path.read_text(encoding="utf-8") if str(path) != "-" else sys.stdin.read()
    lines = strip_code_and_frontmatter(text)
    return check_lines(lines, lex, strict, str(path))


def main(argv):
    lex = load_lexicon()
    if len(argv) < 2:
        print(__doc__)
        return 2
    violations = []
    if argv[1] == "--repo":
        for p in sorted(ROOT.rglob("*.md")):
            rel = p.relative_to(ROOT).as_posix()
            if rel in REPO_SKIP_FILES or any(rel.startswith(d) for d in REPO_SKIP_DIRS):
                continue
            violations += check_file(p, lex, strict=False)
    else:
        for a in argv[1:]:
            violations += check_file(Path(a) if a != "-" else Path("-"), lex, strict=True)
    for path, ln, rule, raw in violations:
        print(f"{path}:{ln}: {rule}: {raw}")
    if violations:
        print(f"\n{len(violations)} violation(s). Rewrite from source, don't patch the draft.")
        return 1
    print("clean")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

---
id: adr-2026-09-14-agent-skills-as-native-unit
type: decision
status: active
confidence: medium
last_reviewed: 2026-09-14
---

# Playbooks are Agent Skills; every other format is generated

**Date.** 2026-09-14
**Decision.** Each moment in `moments/` is a directory with a `PLAYBOOK.md` in the Agent Skills format (YAML frontmatter with name and description, then the body). `MINDSET.md` is the always-loaded core. Adapters for Cursor rules, `AGENTS.md`, `CLAUDE.md`, a system-prompt bundle, `llms.txt`, and an MCP resource server are generated from the tree by `scripts/build_adapters.py`, never hand-maintained.
**Evidence.** Skills give progressive disclosure for free: the description is loaded, the body only when the moment matches. That keeps the always-on context under a thousand words, which the context-engineering guidance in `sources/BIBLIOGRAPHY.md` says is the constraint that matters. Plain Markdown is more portable, but portability is what the generated adapters are for.
**Alternatives.** Plain Markdown with a table of contents (no progressive disclosure; every tool loads everything or nothing). One giant system prompt (unmaintainable past a few thousand words, and every tool gets the same wall). Separate hand-written files per tool (they drift within a week).
**How to reverse.** If a format with better adoption and equivalent progressive disclosure appears, change the generator, not the content. The content is Markdown with frontmatter either way.

**Amendment, same day.** The playbook files are named `PLAYBOOK.md`, not `SKILL.md`. The Agent Skills CLI discovers nested `SKILL.md` files and offered the twelve playbooks as separate installable skills, which would break them (they depend on the canon around them). The repo root carries the single `SKILL.md`, so `npx skills add` and the Claude Code plugin see exactly one skill: the whole canon. The playbooks keep Agent Skills frontmatter (`name`, `description`) so hosts and the adapter generator can still route by description.

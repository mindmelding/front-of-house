# OpenAI: custom GPTs, Assistants, Agents SDK, Responses API

**Custom GPT.** Instructions are capped at 8,000 characters, so use the compact build:

1. Paste `adapters/openai-custom-gpt.txt` into Instructions.
2. Upload the canon as Knowledge: `MINDSET.md`, `PRECEDENCE.md`, `guardrails/*.md`, `context/CONTRACT.md`, `voice/VOICE.md`, `voice/LEXICON.md`, `voice/EXEMPLARS.md`, and the `moments/*/SKILL.md` files (rename each to `moment-<slug>.md` so they're distinguishable). Or upload `adapters/system-prompt-full.txt` as one file.
3. Context layer: custom GPTs can't call MCP directly. Either add an Action that fronts your context layer's REST API, or paste the customer's file into the conversation and the agent will treat it as the file.
4. Overlay: paste your `overlay/*.md` into Instructions if they fit, otherwise upload them as knowledge and add one line: "Read overlay-*.md before replying."

**Assistants / Agents SDK / Responses API.** Use `adapters/system-prompt.txt` (or `system-prompt-full.txt`) as the system or `instructions` string, append your overlay, and expose your context layer as tools. The Agents SDK supports MCP servers as tool sources, so the Moonbase endpoint can be attached directly with the bearer header. Run drafts through `scripts/fohcheck.py` before sending.

**ChatGPT (Codex surface in the desktop app)** reads `AGENTS.md`; see `codex.md`.

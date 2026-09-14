# Any agent with a system prompt

Slack bots, Intercom or Sierra-style agents, a Discord bot, your own harness, a model behind an API.

1. **System prompt:** `adapters/system-prompt.txt`. Use `system-prompt-full.txt` if the model has the context window for the whole canon (about 18,000 words).
2. **Overlay:** append your `overlay/*.md` after it. Policies, authority grants, people.
3. **Context layer:** give the agent tools that satisfy `context/CONTRACT.md`. The simplest is the Moonbase MCP endpoint; the next simplest is one function `get_customer_file(email)` that returns the contract rows as JSON. If the agent has no tools, say so in the overlay; it will treat every conversation as a first one and never pretend to know.
4. **Outbound check:** run every draft through `scripts/fohcheck.py` before it sends. It exits non-zero on lexicon violations.
5. **Write back:** after each substantive reply, post the touch note (shape in `context/CONTRACT.md`) to your context layer.
6. **Proof:** the eval cases in `evals/cases/` are ready-made tests. Feed the context snapshot and the incoming message, compare against the gold reply with `evals/rubric.md`.

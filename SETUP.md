# Setup: point a tool at Front of House

Three layers, loaded in this order:

1. **The canon** (this repo): who the agent is, how it sounds, what it never does.
2. **Your overlay** (private, git-ignored `overlay/`): your policies, authority grants, people, product.
3. **Your context layer** (a CRM or context graph reached over MCP): who the customer is, what we owe them, what they said.

The canon tells the agent *to* read the customer's file before speaking (`context/CONTRACT.md`). The context layer is *how* it reads it. Without layer 3 the agent still behaves well; it just treats every conversation as a first one and says so.

The quickest path for each tool is `scripts/install.sh`. The manual steps are below it.

---

## Cursor

**Fast path**

```
./scripts/install.sh cursor /path/to/your/project
```

This copies the generated rules into `/path/to/your/project/.cursor/rules/` and writes `.cursor/mcp.json` from the template if one doesn't exist. Then put your key in the environment (`export MOONBASE_MCP_KEY=<your mb_ key>`) or paste it into `mcp.json`, and restart Cursor.

**Manual**

1. Copy `adapters/cursor/*.mdc` into `.cursor/rules/` in the project where Cursor will work.
   - `front-of-house.mdc` is `alwaysApply: true`. It carries the mindset, precedence, the never list, the authority gate, and the loading rules.
   - `front-of-house-voice.mdc` and `moment-*.mdc` are agent-requested. Cursor reads their `description` and pulls them in when the situation matches. You can also invoke one by name with `@moment-angry-customer`.
   - `context-moonbase.mdc` (or whichever adapter you use) tells the agent which MCP tools satisfy the context contract and how to cross-check them.
2. Connect the context layer. Create `.cursor/mcp.json` (or add to it):

   ```json
   {
     "mcpServers": {
       "moonbase": {
         "url": "https://yavin.moonbase.ai/mcp",
         "headers": { "Authorization": "Bearer ${env:MOONBASE_MCP_KEY}" }
       }
     }
   }
   ```

   Cursor supports Streamable HTTP servers with a `url`. Keep the key in an environment variable; don't commit it. Restart Cursor, open Settings, MCP, and confirm the server shows its tools (`ask_account`, `list_events`, `get_event`, `list_accounts`).
3. Add your overlay. Copy the templates from `overlay/` into your project's `overlay/` directory, fill them in, and add one line to `front-of-house.mdc` at the top of the body: `Overlay: read ./overlay/*.md before replying.` Until `overlay/authority.md` grants something, every sensitive action is a nudge.
4. Test with a real thread. In Cursor's agent chat:

   > Using Front of House, reply to this message from Dana at Acme. Read her file first.
   > [paste the thread]

   A passing reply calls the context tools before drafting, answers in sentence one, names a who and a when for any promise, and nudges you before touching money, personal data, or access. If it asks Dana something the file already answers, it failed. Grade it against `evals/rubric.md`.

---

## Claude Code

**Fast path**

```
./scripts/install.sh claude /path/to/your/project
```

Copies `adapters/CLAUDE.md` into the project (or appends a pointer if a `CLAUDE.md` exists) and symlinks `moments/` into `.claude/skills/` so each playbook loads on demand as an Agent Skill.

**Manual**

1. `CLAUDE.md`: copy `adapters/CLAUDE.md` into your project, or add to your existing one:
   `Front of House canon lives at /path/to/front-of-house. Read its MINDSET.md and PRECEDENCE.md before any customer-facing work, and follow its loading rules.`
2. Skills: `ln -s /path/to/front-of-house/moments/* .claude/skills/` so each `SKILL.md` is discoverable.
3. Context layer:

   ```
   claude mcp add --transport http moonbase https://yavin.moonbase.ai/mcp \
     --header "Authorization: Bearer $MOONBASE_MCP_KEY"
   ```
4. Overlay: same as Cursor. Put it in the project and point `CLAUDE.md` at it.
5. Test the same way. Ask for a reply to a real thread and check it read the file first.

---

## Anything with a system prompt

Slack bots, a custom GPT, Intercom or Sierra-style agents, your own harness:

1. Paste `adapters/system-prompt.txt` as the system prompt. Use `system-prompt-full.txt` if the model has the context for the whole canon.
2. Append your overlay after it.
3. Give the agent the context tools (the MCP server above, or your own functions that satisfy `context/CONTRACT.md`). If it has no tools, tell it so in the overlay; it will treat every conversation as a first one.
4. Run drafts through `scripts/fohcheck.py` before they send, and log the touch note back through your adapter.

---

## Any other context layer

Write an adapter: copy `context/adapters/TEMPLATE.md`, map each contract row to a call your system supports, and declare what it may write back. Run `make build`; a `context-<name>.mdc` Cursor rule is generated automatically.

---

## What the agent does with all this, in order

1. Loads the mindset and precedence (always).
2. Reads the customer's file through the context tools. If none are connected, says so internally and proceeds as a first conversation.
3. Picks one moment playbook.
4. Reads the overlay for policy, authority, and people.
5. Drafts in the voice, checks against the lexicon.
6. Nudges before anything sensitive. Acts only inside a grant.
7. Replies. Writes the touch note back.

# Lesson 2 — Your first Hermes agent

**30 min · Hands-on + Q&A**

**Goal:** installed, pointed at a local model, two context files written, tools
enabled in blast-radius order, one real task run end to end, and a 25-row eval
set that tells you whether any of it actually works.

**Order matters: plumbing before personality.** Install first, talk about `SOUL.md`
second. A room that has a working binary asks better questions.

---

## 2.1 Install

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
source ~/.zshrc
hermes --version
```

Windows has a PowerShell one-liner; there's also a Desktop installer for Mac.

> **`pip install hermes-agent` *is* Nous-published, but it lags the installer**
> (PyPI 0.19.0 vs v0.21.5) and skips the bundled Node/ripgrep/ffmpeg. Use the
> installer. Same shape as Claude Code, which installs via the native installer
> (recommended) or npm.

---

## 2.2 Point it at a local model

```bash
hermes model     # interactive picker
```

Choose **Custom endpoint** and give it a base URL + API key.

**The official Mac path** is llama.cpp or omlx/MLX behind that custom endpoint:

```bash
# llama.cpp — lower latency
brew install llama.cpp
# 8 GB Mac: -c 65536
llama-server -m qwen3.5-9b-q4.gguf \
  -c 131072 --cache-type-k q4_0 --cache-type-v q4_0 --port 8080
# → endpoint http://localhost:8080/v1
```

```bash
# omlx / MLX — higher throughput, GUI + server, port 8000
# → endpoint http://localhost:8000/v1
```

**Ollama works too** (`OLLAMA_API_KEY`), it just isn't the doc's Mac path. Pick
one for the live demo and tell the room which one you're on — mixing them
mid-class produces unreproducible failures.

**One-command alternative (v0.21.6+):** `hermes model` → **Local models**
installs a pinned llama.cpp, recommends a model that fits your machine,
downloads it and makes it the default. No endpoint to type.

Re-run `hermes model` to confirm the selection, then launch:

```bash
hermes --tui
```

> **≥64K context or nothing.** That's why the llama.cpp line carries `-c 131072`
> and the KV-cache quantization flags. `-c 131072` plus q4 KV needs about 10 GB;
> on an 8 GB Mac, use `-c 65536` (Hermes's 64K floor).

**Claude Code contrast:** you never pick a model server, only a model name.
Here you own the whole inference stack, which is exactly the trade — more
control, more moving parts to misconfigure.

---

## 2.3 Two context files, two scopes

This is the highest-value five minutes in the block for a Claude Code audience,
because they already have the instinct and just need the mapping.

| File | Lives | Holds | Scope |
|---|---|---|---|
| **`SOUL.md`** | `~/.hermes/SOUL.md` | Personality, values, boundaries, tone | Global, durable |
| **`AGENTS.md`** | project root | Architecture, conventions, hard rules | Per-project |

`AGENTS.md` at the top level is loaded **from the CWD at session start**;
subdirectory copies are discovered lazily as the agent navigates into them —
the same behavior as nested `CLAUDE.md` files.

**Bonus for migrating Cursor users:** Hermes auto-reads `.cursorrules` and
`.cursor/rules/*.mdc`. Don't duplicate them.

Minimal `SOUL.md` to write live (full version in `assets/SOUL.md`):

```markdown
# SOUL

## Who you are
A direct, technically careful collaborator. Senior-engineer register.

## How you talk
- Lead with the answer. Context after, only if it changes the answer.
- Never open with "You're absolutely right" or any variant.
- When you disagree, say so in one sentence and give the reason.

## Boundaries
- Never run destructive commands without showing them first.
- Say "I don't know" rather than guessing at a file path or an API.
- Uncertain? Say what would resolve it.
```

That anti-sycophancy block is the live demo. Personality is a **context
artifact, not a weights artifact** — this file is model–context separation as an
actual file on disk. Swap the model tomorrow; the personality survives.

Minimal `AGENTS.md`:

```markdown
# AGENTS.md

## Project
FastAPI service, Postgres, deployed on Fly. Entry point: `app/main.py`.

## Conventions
- `uv` for deps. Never edit `requirements.txt` by hand.
- Tests in `tests/`, run with `pytest -q`.

## Hard rules
- Never commit `.env` or anything under `secrets/`.
- Never touch `migrations/` without being asked explicitly.
```

> **Cost note that will surprise this audience:** context files are part of the
> *stable* system prompt, which is what earns prompt-cache hits. Editing them
> mid-session breaks the cache and you pay a full re-read. Write them once,
> deliberately, at session start. Every character costs on every turn.

---

## 2.4 Turn on tools — in blast-radius order

`/tools` opens the tool picker. **Do not enable everything.** Climb this ladder,
and make students earn the destructive rungs:

| Rung | Enable | Worst case if it goes wrong |
|---|---|---|
| **1. Read-only** | filesystem read, ripgrep | Wasted tokens |
| **2. Draft-only** | write to *new* scratch files; generate shell commands with `execute_code` **off** | A junk file you delete |
| **3. Reversible writes** | edit files inside a git repo | `git checkout .` |
| **4. Irreversible / outbound** | delete, terminal, send messages, spend money, prod | You explain it to someone |

Rung 2 is the underrated one: **have the agent write the command and read it
yourself before running it.** Most bad agent moments die there.

This ladder is a through-line. MCP servers (Lesson 4) and cron jobs (Lesson 4)
climb the exact same rungs.

Pull up the [built-in tools reference](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/tools-reference.md)
so people see the full surface they're switching on.

### Command approval

Every command is checked against a curated dangerous-pattern list — recursive
deletes, SQL drops, piping curl into a shell — before it runs. Four answers:
**once / session / always / deny**.

The default is `approvals.mode: smart`: an auxiliary model auto-approves
low-risk commands, auto-denies clearly dangerous ones, and sends only uncertain
ones to the once/session/always/deny prompt. Set `manual` for the live demo so
the room sees the prompt.

**Choose `session`, not `always`,** until you trust the setup. `always` is a
permanent grant made at the moment you have the least evidence. This is the same
decision as Claude Code's permission modes; the failure mode is identical.

---

## 2.5 Run one real task end to end

Leave this uncut. Failures are the lesson.

```
Summarize this repo in 5 bullets and name the main entrypoint.
```

Then watch tool calls land against your local model. Point out where Hermes's
**per-model parser** normalizes whatever format your model family emits — that
normalization is why a 9B model can drive a tool loop at all.

### Prompting discipline to demo live

- **Be specific.** "Fix the `TypeError` in `api/handlers.py:47`," not "fix the code."
- **Front-load context.** Paste the traceback. Paste the screenshot (`Ctrl+V`
  pastes a clipboard image). Don't iterate through three rounds of clarification.
- **Let the agent use its tools.** "Find and fix the failing test" beats
  dictating each step. Same instinct as Claude Code — dictate the goal, not the
  path.

### CLI power-use worth 90 seconds

| Key / command | Does |
|---|---|
| `Alt+Enter` / `Ctrl+J` / `Shift+Enter` | Multi-line input |
| `Ctrl+C` once | Interrupt and redirect · twice in 2s = exit |
| `Ctrl+V` | Paste a clipboard image (vision) |
| `/` + `Tab` | Autocomplete commands and skills |
| `/verbose` | Cycles off → new → all → verbose |
| `hermes -c` | Resume last session with history |
| `hermes -r "title"` | Resume a session by title (`/title` to name one) |

---

## 2.6 The 60-second eval habit

**This is the part every other Hermes tutorial skips, and it's the one that
makes the rest defensible.**

You cannot tell whether a local model is good enough by vibes. "The answer felt
right" is not a signal. The signal is: **did it call the right tool with the
right arguments?**

Build a 25-row CSV of tasks you'd actually give this agent:

```csv
id,task,expected_tool,expected_args,category,right_tool,right_args,notes
1,What files are in src/?,search_files,"target=files,path=src/",read-only,,,
2,Find every use of get_user in this repo,search_files,"target=content,pattern=get_user",search,,,
3,Read app/main.py,read_file,path=app/main.py,read-only,,,
4,Summarize the README,read_file,path=README.md,read-only,,,should not shell out
5,Which Python version does this project require?,read_file,path=pyproject.toml,read-only,,,tests file-choice reasoning
```

Full 25-row template: [`assets/eval-template.csv`](../assets/eval-template.csv).

Run them. Score two columns only: **right tool?** and **right arguments?**

What this buys you:

1. **A go/no-go on a local model.** Below ~80% tool accuracy, the harness will
   feel broken and you'll blame the wrong layer.
2. **An objective comparison between two candidate models.** Same 25 rows, two
   numbers.
3. **A regression check.** Re-run it after adding a skill (Lesson 3) and after
   wiring an MCP server (Lesson 4). Adding tools *can* degrade tool selection —
   more options, more confusion. Without the eval you'd never see it.

This is the same discipline as skill evals in Claude Code, applied one layer
down at the tool-selection level.

---

## Hands-on checklist

- [ ] `hermes --version` prints
- [ ] `hermes model` → custom endpoint, model serves ≥64K
- [ ] `~/.hermes/SOUL.md` written
- [ ] `AGENTS.md` in the project root
- [ ] Tools enabled at rungs 1–2 only
- [ ] One real task completed with visible tool calls
- [ ] Eval CSV downloaded, ≥5 rows scored live

---

**Next:** [Lesson 3 — Memory and skills in action](03-memory-and-skills.md)

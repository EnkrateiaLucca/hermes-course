---
marp: true
theme: automata
paginate: true
---

<style>
/* Dark slides: readable tables, inline code and syntax highlighting */
section.dark td { background: #2a1b18; color: #F0E6D8; border-color: #3a2522; }
section.dark tr:nth-child(even) td { background: #301f1b; }
section.dark th { border-color: #3a2522; }
section.dark strong, section.dark em { color: #E07A6B; }
section.dark :not(pre) > code { background: #3a2522; color: #F0E6D8; }
section.dark pre .hljs-string { color: #E8B4A0; }
section.dark pre .hljs-number, section.dark pre .hljs-literal { color: #F2C57C; }
section.dark pre .hljs-keyword, section.dark pre .hljs-built_in, section.dark pre .hljs-section { color: #E07A6B; }
section.dark pre .hljs-comment { color: #9C8A80; font-style: italic; }
section.dark pre .hljs-attr, section.dark pre .hljs-variable, section.dark pre .hljs-title,
section.dark pre .hljs-meta, section.dark pre .hljs-bullet, section.dark pre .hljs-code { color: #F0E6D8; }
</style>

<!-- _class: lead dark -->
<!-- _paginate: false -->

<div class="kicker">Automata Learning Lab · O'Reilly Live Training</div>

# Local Agents with <em>Hermes</em>

A persistent personal agent, explained against the Claude Code you already run.
<span style="font-size:0.8em;opacity:0.7">2h 30m · links on these slides are clickable</span>

---

<div class="kicker">Agenda</div>

## What we'll cover

1) **The landscape** — models, harnesses, and where Hermes sits · 30m
2) **Your first agent** — install, context files, tools, evals · 30m
3) **Memory & skills** — the part only Hermes defaults to · 30m
4) **MCP, deploy, reach** — extend it, ship it, secure it · 25m
5) **Choosing** — Hermes vs Claude Code vs OpenClaw · 5m

---

<!-- _class: lead dark -->

<div class="kicker">Block 1</div>

# The local AI agent <em>landscape</em>

No installs yet. Mental map first.

---

<!-- _class: dark quote -->

> <span class="mark">"</span>The personal in personal agent is not the model… it's the agent's memory of your conversations and the skills you've built with it.<span class="mark">"</span>

<div class="by">— <a href="https://creatoreconomy.so/p/hermes-co-founder-on-building-an-ai-agent-that-improves-itself-karan-malhotra">Karan Malhotra</a>, co-founder, Nous Research</div>

---

## No weights change — anywhere

**"Self-improves through use, not retraining" means no weights change.**

* Not in Hermes. Not in Claude Code. Not anywhere today.
* "Not retraining" just means "no fine-tuning."
* Everything here is <em>context engineering</em> — files written to disk and re-injected into a prompt.

---

## Why local agents, now

<div class="bento">
<div class="cell wide"><h3>Persistence</h3><p>State survives the session without a vendor's storage model in the loop.</p></div>
<div class="cell"><h3>Privacy</h3><p>The context layer is the sensitive part — your files, your clients.</p></div>
<div class="cell"><h3>$0 marginal</h3><p>The 400th cron run costs electricity. That's what makes always-on reasonable.</p></div>
<div class="cell wide"><h3>What actually changed in 2026</h3><p>Not the models. Hermes (Feb 2026) made a memory-carrying local agent turnkey. The pieces existed; the bundling didn't.</p></div>
</div>

---

## Three layers people keep collapsing

<div class="flow">
<div class="step"><h3>Model</h3><p>Qwen3.5-9B · Qwen3.6-35B-A3B · Hermes 4.3 36B<br><em>swappable</em></p></div>
<div class="arrow">↑</div>
<div class="step"><h3>Harness</h3><p>Hermes · Claude Code · OpenClaw<br><em>loop, tools, safety</em></p></div>
<div class="arrow">↑</div>
<div class="step"><h3>Agent</h3><p>instructions + memory + skills<br><em>the durable asset</em></p></div>
</div>

**Hermes is a persistent personal-agent harness.** Claude Code is a coding harness that happens to persist a little.

---

## Five primitives, and their Claude Code neighbor

| Hermes primitive | What it is | Claude Code neighbor |
|---|---|---|
| **Tools** | fs, ripgrep, terminal, web, browser | Read/Edit/Bash/Grep |
| **Integrations + MCP** | messaging providers + any MCP server | MCP servers |
| **Skills** | `SKILL.md`, progressive disclosure | Skills — *same* standard |
| **Cron** | scheduled self-contained runs | `/loop`, cloud agents |
| **Memory** | `MEMORY.md` + `USER.md` + FTS5 log | `CLAUDE.md` + Auto Memory |

The vocabulary maps ~1:1. What differs is what runs **by default and unattended**.

---

## Where things live

| Purpose | Hermes | Claude Code |
|---|---|---|
| Project instructions | `AGENTS.md` (repo root) | `CLAUDE.md` or the same `AGENTS.md` |
| Global personality | `SOUL.md` (`~/.hermes/`) | `~/.claude/CLAUDE.md` |
| Learned facts | `MEMORY.md`, `USER.md` | Auto Memory |
| Procedures | `~/.hermes/skills/*/SKILL.md` | `~/.claude/skills/*/SKILL.md` |
| Config | `config.yaml`, `.env` | `settings.json` |

---

## Picking a local model — ask in this order

<div class="flow">
<div class="step"><h3>1 · RAM</h3><p>A hard wall, not a preference</p></div>
<div class="arrow">→</div>
<div class="step"><h3>2 · Task</h3><p>Long-horizon tool use punishes small models</p></div>
<div class="arrow">→</div>
<div class="step"><h3>3 · Tool calls</h3><p>The one that actually decides it</p></div>
</div>

A model that writes beautiful prose and mangles a JSON tool call is <em>useless in a harness</em>.

---

## The shortlist

| Model | RAM | Where it fits |
|---|---|---|
| **Qwen3.5-9B** | 8 GB+ at 64K · ~10 GB at 128K | Official Mac starter pick, quantized |
| **Qwen3.6-35B-A3B** | 32 GB+ | Daily driver, NVIDIA-endorsed default |
| **Hermes 4.3 36B** | 32 GB+ | Nous's own, tuned for tool calling |

**Hard requirement regardless: the model must serve ≥64K context.**
System prompt + context files + tool defs + a real conversation does not fit in 8K.

---

## The tool-call parser story

Every model family emits tool calls differently — XML-ish, JSON blocks, custom tokens.
The harness needs a **parser per family** to normalize them.

Nous ships a first-class `--tool-call-parser hermes` for vLLM.

> When a local model "doesn't work" with an agent, **the parser is the first suspect** — not the model's intelligence.

---

## The landscape, one line each

<div class="bento">
<div class="cell wide"><h3>Hermes</h3><p>Persistent workflows, learns from work, one agent across CLI <em>and</em> messaging.</p></div>
<div class="cell"><h3>Claude Code + Ollama</h3><p>Deep IDE integration, mature tooling, focused sessions.</p></div>
<div class="cell"><h3>OpenClaw</h3><p>Lightest setup, pure CLI coding.</p></div>
</div>

**The rule:** pick Hermes when the accumulated context is the point; pick a stateless coding agent when each session is disposable.

---

<!-- _class: lead dark -->

<div class="kicker">Block 2 · Hands-on</div>

# Your first <em>Hermes agent</em>

Plumbing before personality.

---

<!-- _class: dark -->

<div class="kicker">Install</div>

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
source ~/.zshrc
hermes --version
```

Windows: PowerShell one-liner. Mac: also a Desktop installer.

`pip install hermes-agent` exists (Nous-published) but lags the installer — use the installer.

---

<!-- _class: dark -->

<div class="kicker">Point it at a local model</div>

```bash
hermes model            # → choose "Custom endpoint"

brew install llama.cpp
llama-server -m qwen3.5-9b-q4.gguf \
  -c 131072 --cache-type-k q4_0 --cache-type-v q4_0 --port 8080
# → http://localhost:8080/v1

hermes --tui
```

`-c 131072` + q4 KV ≈ 10 GB — on 8 GB use `-c 65536`.

---

## Mac path: llama.cpp or MLX — not Ollama

* The official Mac guide points at **llama.cpp** (lower latency, `:8080`) or **omlx/MLX** (higher throughput, `:8000`) behind a Custom endpoint.
* Ollama works (`OLLAMA_API_KEY`) — it just isn't the doc's Mac path.
* One-command alternative (v0.21.6+): `hermes model` → **Local models** installs llama.cpp and picks a model that fits.
* **Pick one server and stick with it.** Mixing them mid-session produces unreproducible failures.

**Claude Code contrast:** you never pick a model *server*, only a model name. Here you own the whole inference stack.

---

## Two context files, two scopes

<div class="two-col">
<div>

### `SOUL.md`
`~/.hermes/SOUL.md`

* Personality, values, boundaries, tone
* **Global and durable**
* Survives a model swap

</div>
<div>

### `AGENTS.md`
project root

* Architecture, conventions, hard rules
* **Per-project**, loaded from CWD at session start
* Subdirectory copies load lazily

</div>
</div>

Bonus: Hermes auto-reads `.cursorrules` and `.cursor/rules/*.mdc`.

---

<!-- _class: dark -->

<div class="kicker">SOUL.md — the anti-sycophancy demo</div>

```markdown
# SOUL

## How you talk
- Lead with the answer. Context after, only if it changes the answer.
- Never open with "You're absolutely right" or any variant.
- When you disagree, say so in one sentence and give the reason.

## Boundaries
- Never run destructive commands without showing them first.
- Say "I don't know" rather than guessing at a file path or an API.
```

Personality is a **context artifact, not a weights artifact.**

---

<!-- _class: dark -->

<div class="kicker">AGENTS.md — the project brain</div>

```markdown
# AGENTS.md

## Project
FastAPI service, Postgres, on Fly. Entry point: `app/main.py`.

## Conventions
- `uv` for deps. Never edit `requirements.txt` by hand.
- Tests in `tests/`, run with `pytest -q`.

## Hard rules
- Never commit `.env` or anything under `secrets/`.
- Never touch `migrations/` without being asked explicitly.
```

---

## Context files and the prompt cache

Context files are part of the **stable system prompt** — which is what earns prompt-cache hits.

* Editing them mid-session **breaks the cache**. You pay a full re-read.
* Write them once, deliberately, at session start.
* Every character costs on <em>every turn</em>.

---

## Turn on tools in blast-radius order

<div class="timeline">
<div class="pt"><div class="dot"></div><div class="when">Rung 1 · Read-only</div><div class="what">filesystem read, ripgrep → worst case: wasted tokens</div></div>
<div class="pt"><div class="dot"></div><div class="when">Rung 2 · Draft-only</div><div class="what">new scratch files; generate commands, <em>don't</em> execute → a junk file</div></div>
<div class="pt"><div class="dot"></div><div class="when">Rung 3 · Reversible</div><div class="what">edit files inside a git repo → <code>git checkout .</code></div></div>
<div class="pt"><div class="dot"></div><div class="when">Rung 4 · Irreversible</div><div class="what">delete, terminal, send, spend, prod → you explain it to someone</div></div>
</div>

Rung 2 is the underrated one: **read the command yourself before running it.**

---

## Command approval is the safety net

Every command is checked against a curated dangerous-pattern list — recursive deletes, SQL drops, piping curl into a shell.

Four answers: **once / session / always / deny**

Default `mode: smart` auto-decides the clear cases; set `manual` to see the prompt.

> Choose **`session`**, not `always`. `always` is a permanent grant made at the moment you have the least evidence.

Same decision as Claude Code's permission modes. Identical failure mode.

---

## Run one real task — and leave it uncut

```
Summarize this repo in 5 bullets and name the main entrypoint.
```

* Watch tool calls land against your <em>local</em> model.
* Point at where the per-model parser normalizes the format.
* **Failures are the lesson.** Don't edit them out.

---

## Prompting discipline

* **Be specific.** "Fix the `TypeError` in `api/handlers.py:47`" — not "fix the code."
* **Front-load context.** Paste the traceback. Paste the screenshot (`Ctrl+V`).
* **Let the agent use its tools.** "Find and fix the failing test" beats dictating each step.

Same instinct as Claude Code: dictate the goal, not the path.

---

## CLI power-use

| Key / command | Does |
|---|---|
| `Alt+Enter` · `Ctrl+J` · `Shift+Enter` | Multi-line input |
| `Ctrl+C` once | Interrupt & redirect · twice in 2s = exit |
| `Ctrl+V` | Paste a clipboard image (vision) |
| `/` + `Tab` | Autocomplete commands and skills |
| `/verbose` | Cycles off → new → all → verbose |
| `hermes -c` · `hermes -r "title"` | Resume by history / by title |

---

## The 60-second eval habit

* You cannot tell whether a local model is good enough by vibes.
* "The answer felt right" is not a signal.
* The signal is: **did it call the right tool with the right arguments?**

---

<!-- _class: dark -->

<div class="kicker">25 rows of real tasks</div>

```csv
id,task,expected_tool,expected_args,category
1,What files are in src/?,search_files,target=files path=src/,read-only
2,Find every use of get_user,search_files,target=content pattern=get_user,search
12,Run the test suite,terminal,cmd contains pytest,terminal
21,Drop the users table,terminal,,danger
24,What's 2+2?,none,,no-op
```

Score two columns only: **right tool?** and **right arguments?**

---

## What the eval set buys you

<style scoped>.stat-grid{margin-bottom:48px}</style>

<div class="stat-grid">
<div class="stat"><div class="num">1</div><div class="label">A go / no-go on a local model — below ~80% you'll blame the wrong layer</div></div>
<div class="stat"><div class="num">2</div><div class="label">An objective comparison of two models — same 25 rows, two numbers</div></div>
<div class="stat"><div class="num">3</div><div class="label">A regression check — adding tools <em>can</em> degrade tool selection</div></div>
</div>

Re-run it after Block 3's skill and Block 4's MCP server.

---

<!-- _class: lead dark -->

<div class="kicker">Block 3</div>

# Memory and skills <em>in action</em>

The part only Hermes turns on by default.

---

## Three kinds of durable state

| Kind | What it is | Where |
|---|---|---|
| **Authored instructions** | What you told it | `SOUL.md`, `AGENTS.md` |
| **Learned facts** | What it noticed and kept | `MEMORY.md`, `USER.md` |
| **Learned procedures** | How to do a repeated thing | `skills/*/SKILL.md` |

Plus a fourth thing that's history, not state: an **SQLite/FTS5 log of every session**, searchable with `session_search`.

---

## Teach the accuracy note, don't hide it

Nous markets a **"four-tier memory."** What the docs describe:

* `MEMORY.md` + `USER.md` + the FTS5 session log
* Honcho and Obsidian are **opt-in add-ons**, not built-in tiers
* `SOUL.md` is counted as a tier but is **config/identity — you wrote it, it didn't learn it**
* The Curator's **LLM-consolidation is OFF by default** (50–100 API calls a pass)

Presenting this straight buys you the whole room.

---

## Memory is bounded, and frozen mid-session

<div class="stat-grid">
<div class="stat"><div class="num">2,200</div><div class="label">chars in MEMORY.md</div></div>
<div class="stat"><div class="num">1,375</div><div class="label">chars in USER.md</div></div>
<div class="stat"><div class="num">next</div><div class="label">session before a write reaches the system prompt</div></div>
</div>

Small on purpose — these sit in the system prompt on *every* turn. Force a cleanup with *"clean up your memory."*

---

<!-- _class: dark -->

<div class="kicker">Demo this live</div>

```
> remember that our CI uses GitHub Actions
✓ saved to memory

> what CI do we use?
I don't have that in memory.
```

**Not a bug.** The write landed on disk; it reaches the system prompt next session.
Show it, or a student hits it alone at 11pm and concludes the feature is broken.

---

## Session search — the genuinely distinct one

```
what were we talking about last month re: the pricing model?
```

`session_search` runs FTS5 over **all** past raw conversations. Nothing loads until it's needed.

> This is one of two things a Claude Code power user can't replicate without building it. Claude Code's memory is curated notes — **not indexed transcripts.**

---

<!-- _class: dark quote -->

> <span class="mark">"</span>Reference document → skill. Sticky note → memory.<span class="mark">"</span>

<div class="by">— Hermes docs, on what goes where</div>

---

## Skills: procedural, and free until used

Same standard as Claude Code — <a href="https://agentskills.io">agentskills.io</a>, `SKILL.md`, three stages:

<div class="flow">
<div class="step"><h3>1 · Name + description</h3><p>~100–200 tokens<br><em>always in context</em></p></div>
<div class="arrow">→</div>
<div class="step"><h3>2 · SKILL.md body</h3><p>loads on trigger<br><em>keep under ~500 lines</em></p></div>
<div class="arrow">→</div>
<div class="step"><h3>3 · Reference files</h3><p>read on demand<br><em>one at a time</em></p></div>
</div>

In Hermes these are literal calls: `skills_list()` → `skill_view(name)` → `skill_view(name, file)`.

**Promote to a skill when a task is 5+ steps <em>and</em> repeats.**

---

## Two authoring rules that fall straight out

* **Directives, not essays.** Layer 1 is an always-on cost on every model call.
* **If the workflow is a fixed deterministic sequence — write a script, not a skill.** Don't spend model tokens on work a bash file does perfectly.

---

## The objection you will get

> *"Claude Code can also write files and update `CLAUDE.md`. So what?"*

**They're right.** No weights change in any of these tools.

The real question isn't *can* an agent persist state — they all can.
It's **how much of the loop is autonomous, always-on, and default.**

---

## The self-improvement ladder

<div class="timeline">
<div class="pt"><div class="dot"></div><div class="when">Rung 1</div><div class="what">Can write a file if told. Proves nothing.</div></div>
<div class="pt"><div class="dot"></div><div class="when">Rung 2</div><div class="what">User-triggered persistence — <code>CLAUDE.md</code>, <code>AGENTS.md</code>. Authored, not curated.</div></div>
<div class="pt"><div class="dot"></div><div class="when">Rung 3</div><div class="what">Autonomously decides what to remember, unprompted.</div></div>
<div class="pt"><div class="dot"></div><div class="when">Rung 4</div><div class="what">+ unattended long-horizon curation; retrieval by <em>search</em>.</div></div>
<div class="pt"><div class="dot"></div><div class="when">Rung 5</div><div class="what">+ autonomous skill synthesis <em>and retirement</em> from usage stats.</div></div>
</div>

---

## Where each tool actually lands

* **Claude Code** → **rung 3.** Auto Memory decides what to keep. It has the full substrate for 4–5 — skills are first-class and portable — but a human or a hook drives skill creation, and nothing prunes old memory in the background.
* **Letta (MemGPT)** → arguably **ahead on rung 4.** Self-editing memory has been its architecture since 2023, plus "sleep-time" consolidation. No skill authoring.
* **Hermes** → the one documented running **3→5 wired together, on by default.**

**Say it out loud: the differentiator is default integration, not intelligence.**

---

<!-- _class: dark -->

<div class="kicker">Hands-on · make the agent learn</div>

```bash
# after a genuinely 5+ step task:
> save what you just did as a skill called deploy-staging

# or by hand:
mkdir -p ~/.hermes/skills/deploy-staging
$EDITOR ~/.hermes/skills/deploy-staging/SKILL.md
```

```markdown
---
name: deploy-staging
description: Deploy the current branch to staging and verify health.
  Use when asked to deploy, ship, or push to staging.
---
1. Confirm the working tree is clean; stop if not.
2. `pytest -q` — stop on any failure.
3. `fly deploy --config fly.staging.toml`
4. Poll /health until 200, max 60s. Report SHA + latency.
```

---

## Then re-run it as `/deploy-staging`

Five minutes of agent reasoning becomes **one slash command**, loaded instantly.

That contrast is the whole block. It lands better shown than described.

**Then re-run the eval CSV.** A new skill changes the always-loaded description budget and can shift tool selection. Prove it didn't regress.

---

## The community skill layer

```
/skills                 # what you have
/skills browse          # the Skills Hub
hermes skills install official/<name>
```

**Skills you write for Claude Code are portable to Hermes and back.** Same format, same progressive-disclosure contract.

Your skill library is not harness lock-in. Consumer first, then producer.

---

<!-- _class: lead dark -->

<div class="kicker">Block 4</div>

# MCP, deployment, <em>and reach</em>

Wire it low-blast-radius first. Prove it. Then widen.

---

<!-- _class: dark -->

<div class="kicker">~/.hermes/config.yaml</div>

```yaml
mcp_servers:
  filesystem:
    command: npx
    args: ["-y", "@modelcontextprotocol/server-filesystem",
           "/Users/you/projects"]     # scope it, not $HOME
    tools:
      include: [read_text_file, list_directory]   # start read-only

  fetch:
    command: uvx
    args: ["mcp-server-fetch"]
```

Tools register as **`mcp_<server>_<tool>`** — useful when debugging a wrong pick.

---

## `tools.include` is a security control

Not a tidiness feature. An MCP server hands the agent whatever it feels like exposing.

```
hermes mcp                # picker
hermes mcp install <name>
/reload-mcp               # no session restart
```

> An MCP server's tool **descriptions enter your model's context.** A malicious one is a prompt-injection surface. Read what you install.

OAuth and mTLS supported for remote servers. Parallel calls work.

---

## Hermes as an MCP server

```bash
hermes mcp serve
```

Exposes Hermes's **messaging bridge** — list, read and send conversations across your connected platforms. Claude Code can message your Telegram through Hermes.

These aren't competing harnesses. One can be the other's tool.

**Then re-run the eval CSV.** New tools, new chances to pick the wrong one.

---

## Where it runs — 7 execution backends

| Backend | Use it for |
|---|---|
| **Local** | Your machine, your files, fastest |
| **Docker** | Untrusted code, isolation, reproducible env |
| **SSH** | An always-on box you already own |
| **Modal · Daytona · Vercel Sandbox** | Serverless, hibernates, **~$0 idle** |

The brain — memory, skills, config — is a directory of files. The backend under it is swappable. **Tasks survive crashes and reboots.**

---

## The gateway: one agent, everywhere you type

```bash
hermes gateway setup
hermes gateway install   # launchd / systemd
hermes gateway
```

* **The same agent** on CLI, Telegram, Slack, Discord, Email — 30+ platforms
* Per-chat session state that **follows you across devices**
* Sessions never auto-reset unless you opt in via `session_reset`

The capability with no Claude Code equivalent: the agent that holds your memory is the one answering from the train.

---

<!-- _class: dark -->

<div class="kicker">Optional live add-on · WhatsApp</div>

```bash
hermes whatsapp          # QR wizard → Linked Devices

# ~/.hermes/.env
WHATSAPP_ENABLED=true
WHATSAPP_MODE=bot
WHATSAPP_ALLOWED_USERS=+15551234567

chmod 700 ~/.hermes/whatsapp-session   # these are live credentials
```

Via Baileys — no Meta dev account. Unofficial client: WhatsApp can ban the number.

---

<!-- _class: dark -->

<div class="kicker">Cron — durability with a schedule</div>

```bash
/cron add "0 8 * * 1-5" \
  "Check ~/projects/api for PRs opened since yesterday. \
   Summarize each in one line. If none, reply [SILENT]." \
  --name morning-prs --deliver telegram
```

| Flag | Does |
|---|---|
| `--script` | Python preflight; stdout → agent context |
| `--skill` | Attach a skill (stackable) |
| `--deliver` | telegram / discord / slack / origin / local |
| `[SILENT]` | Suppress the message on a no-op |

---

## The cron gotcha, and the ladder

**Cron runs in a fresh, self-contained session.** No history, no implicit CWD.

* "Check the repo" is meaningless. "Check `~/projects/api`" is not.
* `[SILENT]` is what makes monitors tolerable — a health check that pings 364 times to say "fine" gets muted by day three.
* **First version: read-only, `--deliver local`.** Watch it a day. *Then* let it write and message you.
* Always `/cron run <name>` once before trusting a schedule.

---

## The prompt cache is the cost lever

A **stable system prompt** earns cache hits. Local model → latency. Hosted → money.

**What breaks it:** `/model` switches · provider fallbacks · credential rotation · editing `SOUL.md`/`AGENTS.md` mid-session.

> Prefer starting a **fresh session** on the other model over bouncing back and forth mid-conversation.

`/compress` · `/usage` · `hermes prompt-size` (offline) · `/insights` (30-day patterns)

---

## Scale out when one session is the wrong shape

* **`delegate_task`** — parallel independent subagents. Same instinct as Claude Code's subagents: fan out work whose *results* you need but whose intermediate output you don't want in context.
* **`execute_code`** — one batch script beats twenty terminal round-trips. Each round-trip is a full model call; the script is one.

---

## Security: containers skip the danger check

```bash
TERMINAL_ENV=docker
TERMINAL_DOCKER_IMAGE=python:3.13-slim
```

> **Docker, Singularity, Modal, Daytona, and Vercel Sandbox SKIP the dangerous-command check.** The container *is* the security boundary — by design.

The right setup for untrusted code. **The wrong setup if you assumed approval prompts were still firing.**

---

## Never do this

```bash
GATEWAY_ALLOW_ALL_USERS=true    # on a terminal-enabled bot
```

That is a public shell on your machine.

```bash
TELEGRAM_ALLOWED_USERS=...
DISCORD_ALLOWED_USERS=...
GATEWAY_ALLOWED_USERS=...        # cross-platform
```

Plus: secrets in `~/.hermes/.env` — never in `config.yaml`, never in `AGENTS.md`.

---

<!-- _class: lead dark -->

<div class="kicker">Block 5</div>

# When to use <em>which</em>

Pick correctly. Defend the pick.

---

## The matrix

| Use… | When it's best |
|---|---|
| **Hermes** | Persistent workflows, learning-from-work, one agent across CLI *and* messaging |
| **Claude Code + Ollama** | Deep IDE integration, mature tooling, focused coding sessions |
| **OpenClaw** | Lightest setup, pure CLI coding |

**The rule:** pick Hermes when the accumulated context is the point; pick a stateless coding agent when each session is disposable.

Wanting both is the correct answer — `hermes mcp serve` lets Claude Code reach your messaging through Hermes.

---

## The honest verdict: true, but not unique

| | Persistent memory | Unattended curation | Cross-session FTS | Agent-*authored* skills | Default? |
|---|---|---|---|---|---|
| **Hermes** | Yes | **Yes** (Curator ~7d) | **Yes** | **Yes** | **Automatic** |
| **Claude Code** | Yes | Partial — trims, no prune | No | Not unprompted | Memory yes, skills manual |
| **OpenClaw** | Yes | Unverified | Unverified | Partial (ClawHub) | Unverified |
| **Letta** | Yes | **Yes** — deepest | Yes | No | Architecture |

"Agent writes durable state, reads it back, model swappable" is **Letta's 2023 founding idea.** Leave "unverified" unverified on the slide.

---

## For the Claude Code power user specifically

You've hand-built most of this already. **Two things you don't get automatically:**

<div class="stat-grid">
<div class="stat"><div class="num">1</div><div class="label">Full-text search across every past raw session</div></div>
<div class="stat"><div class="num">2</div><div class="label">An unattended job that prunes and merges memory + skills on a schedule, unasked</div></div>
</div>

Both buildable — a hook, an SQLite index, a cron job. Which <em>is</em> the point.

---

## Answer the sharp question with the ladder

> *"Claude Code writes files too. So what's actually different?"*

1) Filesystem access → rung 1. Proves nothing.
2) `CLAUDE.md` / `AGENTS.md` → rung 2.
3) Claude Code's Auto Memory → rung 3.
4) Unattended curation + search retrieval → rung 4.
5) Skill synthesis with a retirement lifecycle → rung 5.

**Hermes ships 3→5 wired together and turned on by default.** Real, checkable, and smaller than the launch copy implies.

---

## Where to go next

- [Official docs](https://hermes-agent.nousresearch.com/docs/) — the canonical reference
- [`NousResearch/hermes-agent`](https://github.com/nousresearch/hermes-agent) on GitHub (MIT)
- **awesome-hermes-agent** — the community list
- **Hermes self-evolution repo** — agent-improving-itself experiments
- [agentskills.io](https://agentskills.io) — the skill standard, shared with Claude Code

**Ship the artifacts:** `SOUL.md` · `AGENTS.md` · `config.yaml` · cron commands · the eval CSV.
Reproducibility is the #1 complaint about every comparable course.

---

<!-- _class: dark lead -->
<!-- _paginate: false -->

<div class="kicker">One slide to remember</div>

# The model is a component. The context is the <em>asset</em>.

Build the context deliberately · wire new power at low blast radius first · measure with an eval set instead of a feeling.

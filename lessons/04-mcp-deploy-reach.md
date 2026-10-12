# Lesson 4 — MCP, deployment, and reach

**25 min · Presentation + demo + Q&A**

**Goal:** extend the running build with MCP, put it somewhere it survives a
reboot, make it reachable from wherever you already type, and keep it cheap and
safe while doing so.

Same ladder as Lesson 2 applies to everything here: **wire the low-blast-radius
thing first, prove it, then widen.**

---

## 4.1 Extending Hermes with MCP

Config lives in `~/.hermes/config.yaml` under an `mcp_servers` block. Both stdio
subprocesses and HTTP remotes are supported.

```yaml
mcp_servers:
  filesystem:
    command: npx
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/Users/you/projects"]
    tools:
      include: ["read_text_file", "list_directory"]   # start read-only

  fetch:
    command: uvx
    args: ["mcp-server-fetch"]
```

Full file: [`assets/config.yaml`](../assets/config.yaml).

Tools register as **`mcp_<server>_<tool>`** — so the filesystem server's
`read_text_file` shows up as `mcp_filesystem_read_text_file`. Useful when
debugging why the agent picked the wrong one.

```bash
hermes mcp                        # interactive picker
hermes mcp install <name>
hermes mcp configure <name>
```
```
/reload-mcp                       # reload without restarting the session
```

**`tools.include` / `tools.exclude` is the allow-list, and it is a security
control, not a tidiness feature.** An MCP server hands the agent whatever it
feels like exposing. Include the two tools you need. OAuth and mTLS are
supported for remote servers; parallel calls work.

### Hermes as an MCP server

```bash
hermes mcp serve
```

This exposes a **messaging bridge** — 10 tools, e.g. `conversations_list`,
`messages_read`, `messages_send` — so Claude Code can read and send your
Telegram/Slack/Discord conversations through Hermes. That's the composition
story worth 30 seconds on a slide: these aren't competing harnesses, one can be
the other's tool.

**Claude Code contrast:** identical protocol, different config file
(`.mcp.json` / settings vs `config.yaml`). If your students already run MCP
servers, the servers themselves port over unchanged.

**After wiring the server: re-run the eval CSV.** New tools mean new chances to
pick the wrong one. Third checkpoint of the through-line.

---

## 4.2 Where it runs

Seven execution backends: **local, Docker, SSH, Singularity, Modal, Daytona,
Vercel Sandbox.** The ones that hibernate idle at roughly $0 — which is what
makes a personal agent affordable to leave running.

| Backend | Use it for |
|---|---|
| **Local** | Your machine, your files, fastest |
| **Docker** | Untrusted code, isolation, reproducible env |
| **SSH** | An always-on box you already own |
| **Modal / Daytona / Vercel Sandbox** | Serverless, hibernates, near-$0 idle |

**Demo: a $5 VPS with Modal hibernation.** Topology walkthrough — the agent's
brain (memory, skills, config) is a directory of files; the execution backend is
swappable underneath it. Same model–context separation idea, applied to compute.

**Tasks survive crashes and reboots.** That's the property being bought here,
and it's the one a stateless coding session doesn't have.

---

## 4.3 The gateway: one agent, everywhere you type

```bash
hermes gateway setup     # pick platforms
hermes gateway install   # launchd (mac) / systemd (linux)
hermes gateway
```

One gateway → **the same agent** reachable from CLI, Telegram, Slack, Discord,
Email — 30+ platforms, with **per-chat session state that follows you across
devices**. Sessions never auto-reset unless you opt in via `session_reset` in
`~/.hermes/config.yaml`.

This is the capability with no Claude Code equivalent, and it's worth being
concrete about why it matters: the agent that has your memory and your skills is
the same one answering a Telegram message from the train.

**Optional live add-on — WhatsApp** (via Baileys, no Meta dev account needed;
note the ban risk honestly):

```bash
hermes whatsapp          # QR wizard → phone → Linked Devices
```

Writes to `~/.hermes/.env`:

```bash
WHATSAPP_ENABLED=true
WHATSAPP_MODE=bot
WHATSAPP_ALLOWED_USERS=+15551234567
```

```bash
chmod 700 ~/.hermes/whatsapp-session   # session dir = credentials. Lock it.
```

### Messaging discipline

- **`/sethome`** sets where cron and scheduled outputs land. Set it before you
  create cron jobs or you'll wonder where the output went.
- **DM pairing** hands a teammate a one-time code — cleaner and more auditable
  than editing allow-lists by hand.
- **`/verbose new`** on chat platforms. `all` floods a group chat.
- **`/title`** names a session so `hermes -r "title"` can resume it.

---

## 4.4 Cron: durability with a schedule

```bash
/cron add "0 8 * * *" "Check the repo for PRs opened since yesterday and summarize each in one line." \
  --name morning-prs --deliver telegram
```

The critical property: **cron jobs run in fresh, self-contained sessions.** No
conversation history. So the prompt must carry everything it needs — "check the
repo" is meaningless with no CWD context; "check `~/projects/api` for open PRs"
is not.

| Flag | Does |
|---|---|
| `--script` | Python preflight; stdout is injected into the agent's context |
| `--skill` | Attach a skill (stackable) |
| `--deliver` | `telegram` / `discord` / `slack` / `origin` / `local` / chat-id |
| `[SILENT]` | In the prompt: suppress the message when there's nothing to report |

```
/cron list | run | pause | edit | remove
```

`[SILENT]` is what makes monitors tolerable — a health-check that pings you 364
times to say "fine" gets muted by day three. More copy-paste jobs in
[`assets/cron-commands.md`](../assets/cron-commands.md).

**Ladder reminder:** a new cron job's first version should be read-only and
`--deliver local`. Watch it for a day. *Then* let it write things and message
you.

---

## 4.5 Cost: the prompt cache is the lever

For a local model this is latency; for a hosted one it's money. Either way the
mechanism is the same.

**A stable system prompt earns cache hits.** Same context files, same memory,
same tool definitions → the prefix is cached and subsequent turns are cheap.

**What breaks the cache:**

- `/model` switches
- automatic provider fallbacks
- credential-pool rotation
- editing `SOUL.md` / `AGENTS.md` mid-session

Each of these forces a full re-read at input cost. **Prefer starting a fresh
session on the other model over bouncing back and forth mid-conversation.**

| Command | Does |
|---|---|
| `/compress` | Summarize the conversation before you hit the limit |
| `/usage` | Current session status |
| `hermes prompt-size` | Offline — your fixed per-message cost |
| `/insights` | 30-day usage patterns |

**Scale-out, when one long session is the wrong shape:**

- **`delegate_task`** — parallel independent subagents. Same instinct as Claude
  Code's subagents: fan out work whose results you need but whose intermediate
  output you don't want in your context.
- **`execute_code`** — one batch script beats twenty terminal round-trips. Each
  round-trip is a full model call; the script is one.

---

## 4.6 Security — the beat most Hermes tutorials skip

**Command approval is the safety net — except in containers.**

Hermes checks every command against a curated dangerous-pattern list before
running it. Approval tiers: once / session / always / deny. Start at **session**.
Under the default `approvals.mode: smart`, only uncertain commands reach the
prompt: an auxiliary model auto-approves low-risk and auto-denies clearly
dangerous ones.

> **Container backends (Docker, Singularity, Modal, Daytona, Vercel Sandbox)
> SKIP the dangerous-command check.** The container *is* the security boundary. This is a
> deliberate design decision and it means: if you set `TERMINAL_ENV=docker`, the
> image you choose is your entire defense.

```bash
TERMINAL_ENV=docker
TERMINAL_DOCKER_IMAGE=python:3.13-slim
```

That's the right setup for untrusted code. It is the wrong setup if you assumed
approval prompts were still firing.

**Never do this:**

```bash
GATEWAY_ALLOW_ALL_USERS=true    # on a terminal-enabled bot
```

That is a public shell on your machine. Use allow-lists:

```bash
TELEGRAM_ALLOWED_USERS=...
DISCORD_ALLOWED_USERS=...
GATEWAY_ALLOWED_USERS=...        # cross-platform
```

**The rest of the checklist:**

- Secrets in `~/.hermes/.env`, never in `config.yaml`, never in `AGENTS.md`.
- `chmod 700` the WhatsApp session directory — those are live credentials.
- MCP tool allow-listing via `tools.include` — treat every MCP server as
  untrusted code that gets to name its own tools.
- An MCP server's tool *descriptions* enter your model's context. A malicious
  one is a prompt-injection surface. Read what you install.

---

**Next:** [Lesson 5 — When to use Hermes, Claude Code, and OpenClaw](05-decision-matrix.md)

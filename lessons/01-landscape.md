# Lesson 1 — The local AI agent landscape

**30 min · Presentation + Q&A · Nobody installs anything yet**

**Goal:** give the room a mental map — local models, harnesses, and where Hermes
sits relative to the Claude Code they already run — before a single command runs.

---

## 1.1 The one sentence to open with

> "The personal in personal agent is not the model… it's the agent's memory of
> your conversations and the skills you've built with it."
> — Karan Malhotra, co-founder, Nous Research

Everything in this course is downstream of that sentence. The model is a
component you swap. The durable asset is the accumulated context: instruction
files, remembered facts, authored skills, searchable session history.

Call this **model–context separation**. It's a useful label, not Nous's term —
prefer the quote when teaching, and don't present the label as official.

The immediate consequence, and the thing that trips people up: **"self-improves
through use, not retraining" means no weights change.** Not in Hermes, not in
Claude Code, not anywhere in this course. "Not retraining" just means "no
fine-tuning." Say this in the first five minutes and you buy credibility for the
rest of the day.

---

## 1.2 Why local agents now

Three reasons that were not all true a year ago:

- **Persistence.** An agent that runs on your machine can keep state between
  sessions without a vendor's storage model in the loop.
- **Privacy.** The context layer is the sensitive part — your files, your
  clients, your habits. Local inference keeps it local.
- **$0 marginal cost.** Once the model is on disk, the 400th run of a cron job
  costs electricity. This is what makes always-on background agents reasonable.

What changed in 2026 is not the models — it's that **Hermes (launched Feb 2026)
made a memory-carrying local agent turnkey**. The pieces existed. The bundling
didn't.

---

## 1.3 The mental map: models ↔ harnesses ↔ agents

Draw this as three layers, because students routinely collapse them:

```
┌────────────────────────────────────────────────────────────┐
│  YOUR AGENT   = instructions + memory + skills + tools     │  ← the durable asset
├────────────────────────────────────────────────────────────┤
│  THE HARNESS  = Hermes / Claude Code / OpenClaw            │  ← loop, tools, safety
├────────────────────────────────────────────────────────────┤
│  THE MODEL    = Qwen3.5-9B / Qwen3.6-35B-A3B / Hermes 4.3  │  ← swappable
└────────────────────────────────────────────────────────────┘
```

The harness is where all the interesting engineering lives: what goes in the
system prompt, which tools are exposed, what gets approved before it runs, what
persists after the session ends.

**Hermes is a persistent personal-agent harness.** Claude Code is a coding
harness that happens to persist a little. That difference — the *default posture*
toward persistence — is the whole course.

---

## 1.4 Hermes at a glance, for people who know Claude Code

Five primitives, and their nearest Claude Code neighbor:

| Hermes primitive | What it is | Claude Code neighbor |
|---|---|---|
| **Tools** | Filesystem, ripgrep, terminal, web search, browser, image gen | Read/Edit/Bash/Grep/WebSearch |
| **Integrations + MCP** | Native messaging providers + any MCP server | MCP servers in `.mcp.json` / settings |
| **Skills** | `SKILL.md` procedural docs, progressive disclosure | Skills — *same* agentskills.io standard |
| **Cron jobs** | Scheduled self-contained agent runs | `/loop`, scheduled cloud agents |
| **Memory** | `MEMORY.md` + `USER.md` + FTS5 session log, auto-curated | `CLAUDE.md` + Auto Memory |

The vocabulary maps almost one-to-one. What differs is which of these run
**by default and unattended** — that's Lesson 3 and Lesson 5.

One more mapping worth putting on a slide early, because it removes most of the
"where do I put things" confusion:

| Purpose | Hermes | Claude Code |
|---|---|---|
| Project instructions | `AGENTS.md` (repo root) | `CLAUDE.md` — or the same `AGENTS.md` (v2.1.277+, when no `CLAUDE.md` exists) |
| Global personality | `SOUL.md` (`~/.hermes/`) | `~/.claude/CLAUDE.md` |
| Learned facts | `MEMORY.md`, `USER.md` | Auto Memory |
| Procedures | `~/.hermes/skills/*/SKILL.md` | `~/.claude/skills/*/SKILL.md` |
| Config | `~/.hermes/config.yaml`, `~/.hermes/.env` | `settings.json` |

---

## 1.5 Picking your local model — a three-question rubric

Students will ask "which model" before they ask anything else. Answer it with
three questions, in this order:

**1. What's your RAM budget?** This is a hard wall, not a preference.

**2. What's the task?** Long-horizon tool use punishes small models much harder
than single-shot Q&A does.

**3. Is tool-calling reliable?** The one that actually decides it. A model that
writes beautiful prose and mangles a JSON tool call is useless in a harness.

The shortlist:

| Model | RAM | Where it fits |
|---|---|---|
| **Qwen3.5-9B** | 8 GB+ at 64K ctx · ~10 GB at 128K | The official Mac starter pick. Quantized, Apple Silicon. |
| **Qwen3.6-35B-A3B** | 32 GB+ | Daily driver, NVIDIA-endorsed default. |
| **Hermes 4.3 36B** | 32 GB+ | Nous's own model, tuned for tool calling. |

**Hard requirement regardless of pick: the model must serve ≥64K context.**
Hermes's system prompt plus context files plus tool definitions plus a real
conversation does not fit in 8K, and a truncating server fails in confusing ways.

### The tool-call parser story

Different model families emit tool calls in different formats — some XML-ish,
some JSON blocks, some a custom token scheme. The harness needs a **parser per
family** to normalize them. Nous ships a first-class `--tool-call-parser hermes`
for vLLM, which is a large part of why smaller local models behave acceptably
under Hermes.

Teaching point: **when a local model "doesn't work" with an agent, the parser is
the first suspect, not the model's intelligence.** Students will hit this.

---

## 1.6 The local coding-agent landscape

Hermes, Claude Code + Ollama, and OpenClaw each win for different work — the
full comparison and the one-line rule for picking are in the
[Lesson 5 matrix](05-decision-matrix.md#51-the-matrix).

---

## Q&A you should expect

**"Isn't this just Claude Code with extra steps?"**
Partly yes, and we'll settle it properly in
[Lesson 3](03-memory-and-skills.md#35-the-objection-answered-the-self-improvement-ladder) with a five-rung ladder.
Short version: same capability class, different default posture toward
persistence, plus you own the model.

**"Will a 9B model actually be useful?"**
For read-heavy, well-scoped tasks with reliable tool calling, yes. For
multi-file refactors, no. Lesson 2 builds you an eval set so you stop guessing.

**"Do I need a GPU?"**
Apple Silicon unified memory works well for the sizes above. On x86 you want
NVIDIA VRAM or you'll be reading tokens one at a time.

---

**Next:** [Lesson 2 — Your first Hermes agent](02-first-agent.md)

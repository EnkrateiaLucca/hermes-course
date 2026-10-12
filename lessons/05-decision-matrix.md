# Lesson 5 — When to use Hermes, Claude Code, and OpenClaw

**5 min · Presentation + Q&A**

**Goal:** send everyone home able to pick correctly, and able to defend the pick.

---

## 5.1 The matrix

| Use… | When it's best |
|---|---|
| **Hermes** | Persistent workflows, learning-from-work, multiplatform access — one agent across CLI *and* messaging |
| **Claude Code + Ollama** | Deep IDE integration, the most mature tooling, focused coding sessions |
| **OpenClaw** | Lightest setup, pure CLI coding |

**The one-line rule:** *pick Hermes when the accumulated context is the point;
pick a stateless coding agent when each session is disposable.*

Most people in the room want both. Hermes as the standing personal agent that
knows their life; Claude Code for a hard afternoon in one repo. That is the
correct answer, not a cop-out — and `hermes mcp serve` means the first can be a
tool inside the second: Claude Code reads and sends your messaging
conversations through Hermes's messaging bridge.

---

## 5.2 The honest verdict behind the matrix

**True but not unique.**

"Agent writes durable state, reads it back, model is swappable" is the founding
idea of **Letta (MemGPT)** from 2023. Pieces of it ship in Claude Code today.
Nothing here is a new capability class, and no weights change anywhere.

What Hermes uniquely bundles **out of the box and always on**:

1. Autonomous memory curation
2. FTS5 search over **all** past raw sessions
3. Agent-authored skills **with a usage-based retirement lifecycle**

| | Persistent memory | Unattended curation | Cross-session full-text search | Agent-*authored* skills | Default vs manual | Model-agnostic |
|---|---|---|---|---|---|---|
| **Hermes** | Yes | **Yes** (Curator, ~7d, idle-gated) | **Yes** (FTS5, on by default) | **Yes** | **Default + automatic** | **Yes** |
| **Claude Code** | Yes (`CLAUDE.md` + Auto Memory) | Partial — self-trims under a cap, no long-horizon prune | No — repo-scoped notes, not indexed transcripts | Not unprompted — user/hook driven | Auto Memory on; skills mostly manual | Skills portable; the CLI is Anthropic-only |
| **OpenClaw** | Yes (markdown prepended) | Unverified | Unverified | Partial (ClawHub registry) | Unverified | Yes |
| **Letta (MemGPT)** | Yes | **Yes** — deepest on memory | Yes | No `SKILL.md` authoring | Self-editing memory *is* the architecture | Yes |

"Unverified" is stated honestly — no primary doc was found for an OpenClaw
Curator equivalent. Don't fill that gap with a guess on a slide.

---

## 5.3 For the Claude Code power user specifically

If you already run Claude Code with a tuned `CLAUDE.md`, hooks, a skills
directory, and a notes vault, you have hand-built most of this. **Two things you
don't get automatically:**

1. **Full-text search across every past raw session.**
2. **An unattended job that prunes and merges memory + skills on a schedule,
   without being asked.**

Both are buildable — a hook plus an SQLite index plus a cron job gets you close.
Which is exactly the point: **the differentiator is default integration, not a
new kind of intelligence.** That framing is more useful than the marketing and
it's what makes the recommendation trustworthy.

---

## 5.4 The question you will get

> *"Claude Code writes files too. So what's actually different?"*

Answer with the ladder in
[Lesson 3 §3.5](03-memory-and-skills.md#35-the-objection-answered-the-self-improvement-ladder);
Hermes ships 3→5 on by default.

That's the difference. It's real, it's checkable, and it's smaller than the
launch copy implies.

---

## 5.5 Where to go next

- **Official docs** — https://hermes-agent.nousresearch.com/docs/
- **`NousResearch/hermes-agent`** on GitHub (MIT)
- **awesome-hermes-agent** — community list
- **Hermes self-evolution repo** — the agent-improving-itself experiments
- **agentskills.io** — the skill standard, shared with Claude Code

**Ship them the artifacts:** `SOUL.md`, `AGENTS.md`, the `config.yaml` MCP
block, the cron commands, and the eval CSV. Reproducibility is the single
biggest complaint about every comparable course — don't repeat it.

---

## Course close, in one slide

> The model is a component. The context is the asset.
> Build the context deliberately, wire new power at low blast radius first,
> and measure with an eval set instead of a feeling.

---

**Back to:** [README](../README.md)

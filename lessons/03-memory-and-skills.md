# Lesson 3 — Memory and skills in action

**30 min · Presentation + hands-on + Q&A**

**Goal:** the part only Hermes brings by default — it remembers across sessions,
it searches everything you've ever said to it, and it writes its own procedures.

This is also the lesson where a sharp Claude Code user raises their hand and
says *"Claude Code writes files too."* They're right. Answer it head-on, early,
with the ladder in §3.5. Honest framing beats hype and you keep the room.

---

## 3.1 Where durable state actually lives

Three kinds of durable state, and the distinction is worth drilling because
students constantly put things in the wrong one:

| Kind | What it is | Where in Hermes |
|---|---|---|
| **Authored instructions** | What you told it | `SOUL.md`, `AGENTS.md` |
| **Learned facts** | What it noticed and kept | `MEMORY.md`, `USER.md` |
| **Learned procedures** | How to do a repeated thing | `~/.hermes/skills/*/SKILL.md` |

Plus a fourth thing that isn't state so much as *history*: **an SQLite/FTS5 log
of every session**, searchable with `session_search`.

### The accuracy note — teach this, don't hide it

Nous markets a **"four-tier memory."** What the docs actually describe:

- `MEMORY.md` — ~2,200 characters
- `USER.md` — ~1,375 characters
- SQLite + FTS5 log of all sessions
- Honcho (implicit user modeling) and an Obsidian vault as **opt-in add-ons**

`SOUL.md` is counted in the marketing as a tier, but it's **config/identity, not
a learned tier** — you wrote it, the agent didn't learn it.

And: **the Curator's LLM-consolidation is OFF by default** (it costs 50–100 API
calls a pass). What runs automatically is the mechanical part — stale → archived
moves for skills on a schedule.

Presenting this straight costs you nothing and buys you every technical person
in the room.

---

## 3.2 Memory: bounded, and frozen mid-session

Two properties that produce confused students if unstated:

**Bounded.** ~2,200 chars in `MEMORY.md`, ~1,375 in `USER.md`. That's small on
purpose — these files sit in the system prompt on *every* turn. When they fill,
the agent consolidates. You can force it: *"clean up your memory."*

**Frozen mid-session.** A memory write lands on disk immediately, but it only
reaches the system prompt **next session**. So:

```
> remember that our CI uses GitHub Actions
✓ saved to memory

> what CI do we use?
I don't have that in memory.
```

That's not a bug. Demo it live — otherwise a student hits it alone at 11pm and
concludes the whole feature is broken.

**Teaching the agent to remember**, explicitly:

```
remember this for next time: the staging DB is at db-staging.internal:5432
save to memory that we deploy on Fridays only
```

**Claude Code contrast:** Auto Memory also decides unprompted what to keep, and
also lives in files. What Claude Code doesn't have is the FTS5 index over every
raw past session — its memory is curated notes, not searchable transcripts.

---

## 3.3 Session search — the genuinely distinct capability

```
what were we talking about last month re: the pricing model?
```

Hermes runs `session_search` against FTS5 over **all** past raw conversations.
Nothing is loaded until it's needed; the agent retrieves on demand.

This is one of the two things a Claude Code power user cannot replicate without
building it themselves (the other is §3.6). Worth naming as such — it's a
concrete, checkable claim rather than a vibe.

---

## 3.4 Skills: procedural knowledge, zero tokens until used

> **The rule of thumb from the docs: reference document → skill; sticky note → memory.**

Memory holds facts. Skills hold procedures. **Promote to a skill when a task is
5+ steps and it repeats.**

Skills are the *same standard* Claude Code uses — agentskills.io, `SKILL.md`,
progressive disclosure in three stages:

1. **Name + description** (~100–200 tokens) — always in context. Tells the model
   *when* to reach for it. This is the only cost you pay on every call.
2. **`SKILL.md` body** — loaded only when the skill triggers. Keep it under ~500
   lines; longer bodies measurably degrade performance.
3. **Reference files** — read on demand, one at a time.

In Hermes the three stages are literal tool calls: `skills_list()` (~3k tokens)
→ `skill_view(name)` → `skill_view(name, file)`.

Because layer 1 is the always-on cost, the authoring rule follows directly:
**directives, not essays.** And if the workflow is a fixed deterministic
sequence, **write a script, not a skill** — don't spend model tokens on work a
bash file does perfectly.

---

## 3.5 The objection, answered: the self-improvement ladder

> *"Claude Code can also write files and update CLAUDE.md. So what?"*

Correct. No weights change in any of these tools. It's all context engineering.
The real question isn't *can* an agent persist state — they all can — it's **how
much of the loop is autonomous, always-on, and default.** Five rungs:

| Rung | Behavior |
|---|---|
| **1** | Can write a file if told. Every agent with filesystem access. Proves nothing. |
| **2** | User-triggered persistence — `CLAUDE.md`, `AGENTS.md`, `CONVENTIONS.md`. Durable but *authored*. |
| **3** | Autonomously decides what to remember, unprompted. |
| **4** | **+ unattended long-horizon curation** — revisits memory later, on a schedule, without you; retrieves by search rather than a fixed injected block. |
| **5** | **+ autonomous skill synthesis and lifecycle** — notices a reusable workflow, writes `SKILL.md` unprompted, then **retires** it based on usage stats. |

Where things land:

- **Claude Code** reaches **rung 3**. Auto Memory decides what to keep. It has
  the full *substrate* for 4 and 5 — skills are first-class and portable — but a
  human or a hook has to drive skill creation, and no background job prunes old
  memory.
- **Letta (MemGPT)** is arguably **ahead on rung 4**: self-editing memory has
  been its entire architecture since 2023, plus background "sleep-time"
  consolidation. No rung-5 skill authoring.
- **Hermes** is the one documented running **rungs 3→5 wired together as one
  default, always-on product**: autonomous memory writes (`write_approval` off
  by default), an unattended Curator moving skills active → stale (14d) →
  archived (30d), FTS5 over all sessions, and agent-authored skills.

**The takeaway to say out loud: Hermes's differentiator is default integration,
not intelligence.** That's a smaller claim than the marketing makes and a much
more defensible one.

---

## 3.6 Hands-on — make the agent learn

**Step 1.** Run a genuinely multi-step task on the running build. Something
5+ steps: run the tests, read the failure, patch it, re-run, summarize.

**Step 2.** Hermes will offer to save the workflow as a skill. Accept. Or ask:

```
save what you just did as a skill called deploy-staging
```

Or write it by hand:

```bash
mkdir -p ~/.hermes/skills/deploy-staging
$EDITOR ~/.hermes/skills/deploy-staging/SKILL.md
```

```markdown
---
name: deploy-staging
description: Deploy the current branch to staging and verify health. Use when asked to deploy, ship, or push to staging.
---

# Deploy to staging

1. Confirm the working tree is clean; stop if not.
2. `pytest -q` — stop on any failure.
3. `fly deploy --config fly.staging.toml`
4. Poll `https://staging.example.com/health` until 200, max 60s.
5. Report the deployed SHA and health latency.

## Never
- Deploy from a dirty tree.
- Deploy to production from this skill.
```

**Step 3.** Re-run. Type `/deploy-staging`. It loads instantly, no re-derivation.
That contrast — five minutes of agent reasoning becoming one slash command — is
the whole point of the block, and it lands better shown than described.

**Step 4.** **Re-run the eval CSV from Lesson 2.** Adding a skill changes the
always-loaded description budget and can shift tool selection. Prove it didn't
regress. This is the through-line: evidence, not vibes.

---

## 3.7 The community skill layer

```
/skills                 # what you have
/skills browse          # the Skills Hub
hermes skills install official/<name>
```

Tour **agentskills.io** — the open standard. The point for this audience:
**skills you write for Claude Code are portable to Hermes and back.** Same
format, same progressive-disclosure contract. Your skill library is not a
harness lock-in.

Consumer first, then producer: install one, read its `SKILL.md`, *then* write one.

---

## Closing the loop

Tie back to the founder framing: *"Hermes became its own biggest contributor."*
The agent writing its own skills is the loop closing — and it's a context loop,
not a training loop. Say it that way.

---

**Next:** [Lesson 4 — MCP, deployment, and reach](04-mcp-deploy-reach.md)

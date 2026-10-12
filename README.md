# Local Agents with Hermes — Lessons

Markdown lesson series for the 2h30 live training. Every lesson explains a Hermes
concept **against its Claude Code equivalent**, because that's the harness most of
the room already knows.

| # | Lesson | Format | Time |
|---|--------|--------|------|
| 1 | [The local AI agent landscape](lessons/01-landscape.md) | Presentation + Q&A | 30 min |
| 2 | [Your first Hermes agent](lessons/02-first-agent.md) | Hands-on + Q&A | 30 min |
| 3 | [Memory and skills in action](lessons/03-memory-and-skills.md) | Presentation + hands-on | 30 min |
| 4 | [MCP, deployment, and reach](lessons/04-mcp-deploy-reach.md) | Presentation + demo | 25 min |
| 5 | [When to use Hermes, Claude Code, OpenClaw](lessons/05-decision-matrix.md) | Presentation + Q&A | 5 min |

## Downloadables (ship these to students)

- [`assets/SOUL.md`](assets/SOUL.md) — starter global personality file → `~/.hermes/SOUL.md`
- [`assets/AGENTS.md`](assets/AGENTS.md) — starter project brain → repo root
- [`assets/config.yaml`](assets/config.yaml) — MCP servers block → `~/.hermes/config.yaml`
- [`assets/eval-template.csv`](assets/eval-template.csv) — the 25-row tool-call eval set
- [`assets/cron-commands.md`](assets/cron-commands.md) — copy-paste cron jobs
- Root [`AGENTS.md`](AGENTS.md) / [`SOUL.md`](SOUL.md) — the instructor's own lived-in setup (private paths redacted), next to the `assets/` starters.

## Through-lines (keep these consistent across all five blocks)

1. **One running build.** Same agent from install to deploy — memory, skills, MCP, and cron all land on it.
2. **The eval CSV travels.** Introduced in Lesson 2, re-run after Lesson 3's skill and Lesson 4's MCP server. Evidence, not vibes.
3. **The start-safe tool ladder.** Every new capability — tool, MCP server, cron job — gets wired at low blast radius first, proven, then widened.
4. **Ship every config artifact.** Reproducibility is the #1 review gap in comparable courses.
5. **Honest framing.** No weights change anywhere in this course. It's all context engineering. Say so early, and the hype question in Lesson 5 answers itself.

## Two install corrections

1. **`pip install hermes-agent` is Nous-published but lags the installer (0.19.0 vs v0.21.x) and skips bundled deps.** Install with `curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash` or the Desktop app.
2. **On Mac the official local-LLM path is llama.cpp or omlx/MLX behind a Custom endpoint**, not Ollama. Ollama works (`OLLAMA_API_KEY`), it just isn't the doc's Mac path. Demo one, and say which.

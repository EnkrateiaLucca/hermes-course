# Build Your First Local Agent with Hermes: beat sheet

One numbered beat = one keypress. Step 0 is what shows when the scene opens.

## 1 · Hello

### Scene: title
0. Title on screen.
1. "Local" gets the marker. "Everything today runs on your machine."
2. Subtitle: private, remembers you, works while you sleep.
3. Hermes website fades in.

### Scene: today
1–7. One stop per chapter: Install, Model, Chat & tools, Memory, Second brain, Messaging, Using it.

### Scene: three layers
0. "Three layers."
1. Model box draws. "Qwen, Gemma, Claude, GPT. Swappable."
2. Harness box draws. "Hermes: the loop, the tools, the safety rails."
3. Context box draws in green. "Memory, skills, SOUL.md."
4. Marker on "your context compounds". "Swap the model tomorrow and you keep all of this."

## 2 · Install

### Scene: install
0. Title + curl line.
1. `hermes --version` and its output.
2. Docs screenshot. "Windows: PowerShell one-liner. Mac: Desktop app too."

## 3 · Pick a model

### Scene: three decisions
1. Engine.
2. A model that fits your machine.
3. Plug it into Hermes.

### Scene: the engine
0. "The engine: llama.cpp."
1. llama.cpp box draws. "Runs on Metal, CUDA, Vulkan, CPU."
2. Ollama and LM Studio sit on top of it.
3. Hermes' own "Local models" glows. "Hermes ships llama.cpp too."
4. MLX and vLLM to the side. "Mac-only / GPU servers."
5. Three reasons: OpenAI-compatible /v1, tool calls via --jinja, you set the context.

### Scene: the formula
0. "memory ≈ weights + KV cache + ~1 GB"
1. Weights ≈ params × bits ÷ 8. Q4_K_M ≈ 0.6 GB per billion params.
2. KV cache = your context window. Hermes needs ≥ 64K.
3. The GPU budget: Mac ≈ 75% of RAM, NVIDIA = VRAM.

### Scene: worked example (Qwen3.8-27B, 64K)
1. Weights bar: 16.1 GB.
2. KV cache: +2.3 GB (q8_0).
3. Runtime: +0.8 GB → 19.4 GB, measured.
4. 24 GB Mac budget line (~18 GB). Doesn't fit.
5. 32 GB Mac / 24 GB GPU line (~24 GB). Fits.

### Scene: dense vs MoE
1. Dense 27B memory bar.
2. MoE 35B-A3B memory bar. "Bigger."
3. Read-per-token bars. "But it only reads ~3B params per token."
4. Takeaway: MoE = more memory, much faster.

### Scene: what to run
1–5. Ladder rungs 8 → 128 GB.
6. "What I run day to day."

### Scene: check before you download
1. canirun.ai tier list.
2. Hugging Face hardware panel; UD-Q4_K_M 22.1 GB circled.
3. "File size on Hugging Face ≈ memory for the weights."

## 4 · Plug it in

### Scene: hermes model
0. The picker.
1. Box on "Local models" → A, automatic.
2. Box on "Custom endpoint" → B, your own server.
3. Bracket on the provider list → subscriptions live here too.

### Scene: path A, Local models
0. Screenshot.
1. Machine line circled. "It measures your machine."
2. ★ circled. "Best model that fits fully in memory and runs ≥ 20 tok/s."
3. Pipeline draws: install llama.cpp → download GGUF → start server → set default.
4. Warning: Mac < 32 GB or GPU < 24 GB → no ★ → path B.

### Scene: path B, serve it yourself
0. llama-server screenshot.
1. -hf: download from Hugging Face.
2. --jinja: tool calls.
3. -c 65536: Hermes' minimum.
4. q8_0 KV cache: half the memory.
5. "listening on :8080" + curl test.

### Scene: path B, point Hermes at it
0. Wizard screenshot.
1. Base URL boxed.
2. "Verified" + detected model boxed.
3. Context 65536 boxed.
4. Resulting config.yaml.

### Scene: other servers
1. Ollama (raise its context).
2. LM Studio (own row).
3. vLLM.

### Scene: prefer a subscription
0. The one line about subscriptions.
1. /model to switch mid-session.
2. hermes fallback add: local first, cloud backup.
3. hermes status screenshot.

### Scene: four things that break it
1–4. Context, --jinja, /v1, wrong model.
5. Strike "a Hermes 4 model".

## 5 · Chat & tools

### Scene: first launch
0. Banner.
1. Model line boxed.
2. Tools column boxed.
3. Skills column boxed.

### Scene: give it a task
0. Screenshot of a real run.
1. Tool calls boxed.
2. Answer boxed. "All on my laptop. $0."

### Scene: tools
0. hermes tools list.
1–4. Blast-radius ladder: read-only, drafts, reversible, irreversible.

### Scene: integrations
0. hermes plugins enable google_meet.
1. What it adds: meet_join, meet_say, live captions.
2. Catalog + MCP.

### Scene: skills
0. hermes skills list.
1. SKILL.md anatomy.
2. Same open standard as Claude Code.
3. It writes new skills after hard tasks.

### Scene: cron
0. hermes cron create + list.
1–4. Use cases: daily news, Apple Notes → Obsidian, standup prep, nightly health check.
5. Or ask in chat: /cron.

## 6 · Memory

### Scene: three files
1. MEMORY.md.
2. USER.md.
3. SOUL.md.
4. Arrow into the system prompt, every session.
5. "Small on purpose."

### Scene: memory in action
0. Chat: "Remember this…"
1. +user / +memory rows boxed. "It decides where each fact goes."
2. The two files on disk.

### Scene: SOUL.md
0. SOUL.md panel.
1. Marker on the anti-sycophancy line.
2. "Personality is a file. Swap the model, keep the soul."

## 7 · Second brain

### Scene: Obsidian
1. Create a vault.
2. Tell Hermes where it is.
3. The obsidian skill reads and writes it.

### Scene: what to save
1. Capture group.
2. Build group.
3. Think group.

### Scene: meeting notes on autopilot
1. Recordings folder.
2. Cron fires daily.
3. Hermes transcribes and summarizes.
4. Note lands in the vault, linked to the project.

## 8 · Messaging

### Scene: WhatsApp
0. Phone ↔ gateway ↔ Hermes.
1. hermes whatsapp → scan QR.
2. Allowlist your number.
3. hermes gateway install.
4. Warning: unofficial bridge, dedicated number.

## 9 · Using it

### Scene: workflow tips
1–4. Front-load context, resume with -c, twice → skill / thrice → cron, start read-only.

### Scene: vibe check
0. The vibe-check browser.
1. 100 real tasks from my own history.
2. Pass criteria + failure modes per task.
3. Category bars: score per category.
4. Swap the model, keep the harness, re-run.

## 10 · Wrap

### Scene: when to use what
1. Hermes.
2. Claude Code.
3. OpenClaw.
4. The one-line rule.

### Scene: close
0. "Your model is swappable."
1. "Your context compounds."
2. Links.

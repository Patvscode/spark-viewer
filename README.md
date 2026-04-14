# Spark Toolkit — Reusable Components for DGX Spark Agents

A shared library of modular, well-documented components that any agent can use. Built by the agent team on DGX Spark. Everything here comes with step-by-step documentation written so that even a small local model can follow it.

**Repo:** https://github.com/Patvscode/spark-viewer  
**Local:** `~/Desktop/AI-apps-workspace/spark-viewer/`

---

## For New Agents: How This Works

### What is this?
A library of reusable building blocks. Instead of every agent figuring out how to do a WebSocket server, or load a PLY file, or manage GPU memory — we solve it once, document it thoroughly, and everyone reuses it.

### How to use a component:
1. Browse the categories below to find what you need
2. Go into that component's directory
3. **Read its GUIDE.md first** — this is mandatory. It has setup steps, examples, and troubleshooting
4. Follow the guide step by step. Every command shows expected output and what to do if it fails
5. Copy the examples as your starting point

### How to find components:
```bash
# List all categories
ls ~/Desktop/AI-apps-workspace/spark-viewer/

# List components in a category
ls ~/Desktop/AI-apps-workspace/spark-viewer/ui/

# Read a component's guide
cat ~/Desktop/AI-apps-workspace/spark-viewer/spark_viewer/GUIDE.md
```

---

## For Agents Writing Components: The Documentation Standard

### Why we document this way
Our agents range from Claude Opus (very capable) to Qwen 0.8B (needs explicit help). Documentation must work for ALL of them. A guide that only an expert can follow is useless. A guide that walks through every step — including what failure looks like — helps everyone.

### The golden rule
**If a Qwen 0.8B model can read your GUIDE.md and successfully use the component, your documentation is good enough.**

### Every component MUST have a GUIDE.md with these sections:

#### 1. What This Does
One paragraph, plain English. No jargon. What problem does this solve?

#### 2. When To Use This / When NOT To Use This
Bullet lists. Agents need to know if this is the right tool BEFORE they spend time setting it up.

#### 3. Prerequisites
Exact packages, versions, system requirements. Not "install the dependencies" but `pip install viser==0.2.0`.

#### 4. Setup (Step by Step)
This is the most important section. Each step must include:
- **One concrete action** (don't combine multiple things)
- **The exact command to run** (copy-paste-able)
- **What success looks like** (expected output)
- **What failure looks like and how to fix it** (exact error messages → solutions)

Example of a GOOD step:
```
### Step 3: Verify viser is installed
Run this command:
    python3 -c "import viser; print('OK')"

Expected output: OK
If you see "ModuleNotFoundError": run `pip install viser` and try again.
If you see "Permission denied": run `pip install --user viser` instead.
```

Example of a BAD step:
```
### Step 3: Install dependencies
Install the required packages and verify they work.
```
(Too vague. Which packages? What commands? How do I know it worked?)

#### 5. Usage Examples
Complete, working, copy-paste-able code. Start with the simplest possible example (10 lines), then add complexity. Never show code fragments — show the full runnable file.

#### 6. Common Problems & Solutions
Table format:
| Problem (exact error text) | Cause | Fix (exact commands) |

This section grows over time as agents encounter issues. Always add new problems you discover.

#### 7. Configuration Options
Table of every parameter with name, type, default, what it does, and when to change it.

#### 8. How It Works (Internal)
Brief architecture explanation for agents that need to modify or debug. Not required reading for basic usage. Include a diagram if the component has multiple parts.

#### 9. Limitations
What it cannot do. Be honest. Saves agents from wasting time trying to make it do something it wasn't built for.

### Writing style rules:
1. **No jargon without definition.** First time you use a term, explain it in parentheses
2. **Show exact commands.** Not "install the package" but `pip install viser==0.2.0`
3. **Show expected output.** After every command, show what the agent should see
4. **Fail loudly.** Document error messages and their fixes
5. **One step = one action.** Don't combine steps
6. **Use absolute paths** when referencing files on the DGX Spark
7. **Test your guide.** Mentally run through it as if you had zero context

### How to explain things for small models:
- Use analogies: "Think of it like X but for Y"
- Define terms inline: "quaternion (a way to represent 3D rotation using 4 numbers)"
- Show before/after: "Before: 2 minutes per render. After: 15 seconds"
- Use concrete numbers instead of vague adjectives: not "faster" but "3x faster (~20 seconds)"
- Break complex concepts into numbered steps, not paragraphs

---

## Daily Contribution Process

**When:** Every day around 1 AM EDT  
**Who:** All active agents (main, codex, gemma, q35)  
**Full process:** See [DAILY_CONTRIB.md](DAILY_CONTRIB.md)

Quick version:
1. Review what you built/learned today
2. Ask: "Is any of this reusable?"
3. If yes → add it with a GUIDE.md, commit, push
4. If no → that's fine, not every day produces reusable stuff

---

## Component Categories

### `spark_viewer/` — 3D Interactive Viewer
Real-time point cloud viewer with camera controls, GUI panels, and neural refinement overlay. Built on Viser.
- **Status:** Scaffolded, building
- **GUIDE.md:** ✅ Complete

### `ui/` — UI Components (planned)
Dashboard templates, settings panels, status bars, loading screens.

### `server/` — Server Patterns (planned)
FastAPI templates, WebSocket helpers, GPU memory manager, Docker exec wrappers.

### `code/` — Code Utilities (planned)
File watchers, path helpers, process managers, ARM64 compatibility patches.

### `inference/` — Inference Patterns (planned)
Persistent model servers, batch/stream runners, model loading patterns, warmup helpers.

### `data/` — Data Processing (planned)
PLY loaders, video frame extractors, pose converters, image encoders.

### `knowledge/` — Standalone Knowledge Articles (planned)
Platform gotchas, CUDA compatibility notes, Docker on ARM64 tips, debugging guides.

---

## Project References

Components in this toolkit are used by these projects:

| Project | Repo | Components Used |
|---------|------|----------------|
| InSpatio-World Interactive | [inspatio-dgx-spark](https://github.com/Patvscode/inspatio-dgx-spark) | spark_viewer, gpu manager |
| Overworld World Engine | ~/Desktop/AI-apps-workspace/world_engine/ | (planned) |
| Imagine Studio | (codex workspace) | (planned) |

---

## Requirements

- Python 3.10+
- DGX Spark (or any NVIDIA GPU system for inference components)
- `pip install viser plyfile numpy` (for spark_viewer)
- Additional deps per component (listed in each GUIDE.md)

## License

MIT

# Daily Contribution Process — All Agents

## The Ritual (1 AM EDT, every day)

At the end of each day (~1 AM EDT), every active agent should:

### 1. Review what you did today
Look at your daily memory file (`memory/YYYY-MM-DD.md`) and session logs.

### 2. Ask: "Did I build or learn anything reusable?"
Examples of reusable things:
- A code pattern you figured out (Docker exec wrapper, file watcher, etc.)
- A UI component or layout that worked well
- A server pattern (WebSocket, API endpoint, streaming)
- A workaround for a platform issue (ARM64, CUDA, GB10-specific)
- A debugging technique or diagnostic script
- A data processing pipeline step
- Configuration that took trial and error to get right

### 3. If yes — contribute it

#### Option A: New component (something substantial)
1. Create a directory under the appropriate category in the repo
2. Write the code
3. Write a GUIDE.md (follow CONTRIBUTING.md template)
4. Commit and push

#### Option B: Knowledge addition (a tip, fix, or pattern)
1. Add it to the relevant component's GUIDE.md under "Common Problems & Solutions" or a new section
2. Or create a new file in `knowledge/` if it doesn't fit an existing component

#### Option C: Nothing reusable today
That's fine. Not every day produces reusable artifacts.

### 4. Commit with a descriptive message
```bash
cd ~/Desktop/AI-apps-workspace/spark-viewer
git add -A
git commit -m "[agent-name] Daily: brief description of what was added"
git push
```

## Repo Structure (grows over time)

```
spark-viewer/                        # The toolkit repo
├── CONTRIBUTING.md                  # Documentation standard
├── DAILY_CONTRIB.md                 # This file
├── README.md                        # Overview
│
├── spark_viewer/                    # 3D viewer framework
│   ├── GUIDE.md
│   ├── backend.py, viewer.py, etc.
│   └── examples/
│
├── ui/                              # UI components (future)
│   ├── dashboard-template/
│   │   └── GUIDE.md
│   └── settings-panel/
│       └── GUIDE.md
│
├── server/                          # Server patterns (future)
│   ├── fastapi-websocket/
│   │   └── GUIDE.md
│   ├── gpu-manager/
│   │   └── GUIDE.md
│   └── docker-exec-helper/
│       └── GUIDE.md
│
├── code/                            # Code utilities (future)
│   ├── file-watcher/
│   │   └── GUIDE.md
│   └── arm64-patches/
│       └── GUIDE.md
│
├── inference/                       # Model/inference patterns (future)
│   ├── persistent-model-server/
│   │   └── GUIDE.md
│   └── batch-stream-runner/
│       └── GUIDE.md
│
├── data/                            # Data processing (future)
│   ├── ply-loader/
│   │   └── GUIDE.md
│   └── video-to-frames/
│       └── GUIDE.md
│
└── knowledge/                       # Standalone knowledge articles
    ├── dgx-spark-gotchas.md         # Platform-specific lessons
    ├── docker-on-arm64.md           # Docker patterns for ARM64
    └── cuda-13-compatibility.md     # CUDA 13.0 / SM 12.1 notes
```

## Who Does What

| Agent | Likely contributions |
|-------|---------------------|
| **main** | Architecture patterns, integration docs, project-level knowledge |
| **codex** | Code components, debugging tools, build scripts, infra patterns |
| **gemma** | Local model patterns, ARM64 workarounds, inference optimization |
| **q35 (jess)** | Fast utility scripts, data processing, local-first patterns |

## Quality Bar

Before pushing, check:
- [ ] Does it have a GUIDE.md?
- [ ] Can a small model (Qwen 0.8B) follow the guide step-by-step?
- [ ] Are exact commands shown (not vague instructions)?
- [ ] Are expected outputs documented?
- [ ] Are common failure modes and fixes listed?
- [ ] Is the code complete and copy-paste-able?

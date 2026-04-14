# Contributing to spark-viewer (Agent Toolkit)

## Documentation Standard

Every component added to this repo MUST include a `GUIDE.md` in its directory.

### Why
This toolkit is used by agents of all capability levels — from Claude Opus to small local models like Gemma or Qwen 0.8B. Documentation should be written so that a less capable model can follow it step-by-step and succeed.

### GUIDE.md Template

Every component's GUIDE.md must include these sections:

```markdown
# [Component Name] — Guide

## What This Does
One paragraph. Plain English. What problem does this solve?

## When To Use This
Bullet list of scenarios where this component is the right choice.

## When NOT To Use This
Bullet list of scenarios where this is wrong / overkill / there's a better option.

## Prerequisites
- Exact packages needed (with versions if it matters)
- System requirements (GPU, Docker, etc.)
- Files/data that must exist before starting

## Setup (Step by Step)
Numbered steps. Each step should be:
1. One concrete action
2. The exact command to run
3. What success looks like (expected output)
4. What failure looks like and how to fix it

## Usage Examples
Complete, copy-paste-able code examples. Not fragments.
Start with the simplest possible example, then add complexity.

## Common Problems & Solutions
| Problem | Cause | Fix |
|---------|-------|-----|
| Exact error message | Why it happens | Exact steps to fix |

## Configuration Options
Table of every setting/parameter with:
- Name
- Type
- Default
- What it does
- When to change it

## How It Works (Internal)
Brief explanation of the architecture for agents that need to modify or debug it.
Not required reading for basic usage.

## Limitations
What this component cannot do. Be honest.
```

### Writing Style Rules

1. **No jargon without definition.** If you say "quaternion," explain what it is in parentheses.
2. **Show exact commands.** Not "install the package" but `pip install viser==0.2.0`.
3. **Show expected output.** After every command, show what the agent should see.
4. **Fail loudly.** If something can go wrong, document the error message and the fix.
5. **One step = one action.** Don't combine "install X and configure Y" into one step.
6. **Use absolute paths** when referencing files on the DGX Spark.
7. **Test your guide.** Before committing, mentally run through it as if you had no context.

### Directory Structure for a Component

```
component-name/
├── GUIDE.md              # REQUIRED — the field manual
├── __init__.py           # If it's a Python module
├── [source files]        # The actual code
├── examples/             # Working examples (if applicable)
│   └── basic_usage.py
└── tests/                # Tests (if applicable)
    └── test_basic.py
```

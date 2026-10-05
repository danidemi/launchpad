# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Overview

`launchpad` is a Claude Code plugin that helps turn a raw business idea into
a structured, presentable concept: problem/solution framing, vision and
mission statements, a shortlisted and vetted name, and a one-page pitch.

## Repo Layout

```
.claude-plugin/plugin.json    # plugin metadata (name, version, description)
skills/<skill-name>/
    SKILL.md                   # authoritative skill spec (YAML frontmatter + phases)
    references/                 # supplementary docs, read on demand (not loaded upfront)
agents/<agent-name>.md          # agent definitions (frontmatter + system prompt)
scripts/domain-check.py         # RDAP/WHOIS/DNS domain checker used by name-researcher
scripts/update-tlds.py          # rebuilds scripts/data/tlds-all.txt from the IANA root DB
```

## Skill Pipeline

Skills are meant to be used roughly in this order, but each also works
standalone if the user already has partial material:

1. `idea-capture` — structure a raw idea into problem, solution, target
   customer, and value proposition (a lean-canvas-style artifact).
2. `vision-crafting` — from the captured idea, draft vision, mission, and
   positioning statements.
3. `business-naming` — generate and score name candidates, then hand off to
   the `name-researcher` agent to check real-world availability.
4. `pitch-one-pager` — assemble idea + vision + chosen name into a single
   shareable one-pager (published as an Artifact when the session supports
   it, otherwise a markdown file).

## Conventions

- **YAML frontmatter**: every `SKILL.md` has `name` and `description`
  (description doubles as trigger-phrase matching text).
- **Phases**: numbered `## Phase N – Title` sections executed in order.
- **References are lazy**: only load a `references/*.md` file when the
  current phase actually needs it.
- **Working files**: skills write their output to markdown files in the
  `launchpad/` folder in the current working directory (e.g.
  `launchpad/idea.md`, `launchpad/vision.md`), never elsewhere. Every skill
  repeats this in its own `## Output Location` section, since skills load
  independently; keep them in sync. Never invent a business idea's content,
  only structure what the user provides.

## Local Testing

```bash
claude --plugin-dir .
```

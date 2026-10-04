# launchpad

A Claude Code plugin for setting up new business ideas: from organizing the
core idea, to drafting a vision, to naming the business, to a one-page pitch.

## Skills

| Skill | Use it to... |
|---|---|
| `idea-capture` | Turn a raw idea into a structured problem/solution/customer/value-prop artifact. |
| `vision-crafting` | Draft vision, mission, and positioning statements from the captured idea. |
| `business-naming` | Generate and score name candidates, then check availability. |
| `pitch-one-pager` | Assemble everything into a single shareable one-pager. |

## Agents

| Agent | Purpose |
|---|---|
| `name-researcher` | Checks a shortlist of candidate names for domain, social-handle, and obvious trademark conflicts. |

## Local Testing

```bash
claude --plugin-dir .
```

## Installation

Add this repo as a plugin marketplace source, or install directly with:

```
/plugin marketplace add <this-repo-url>
/plugin
```

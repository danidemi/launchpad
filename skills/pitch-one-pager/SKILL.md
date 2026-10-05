---
name: pitch-one-pager
description: >
  Assembles launchpad/idea.md, launchpad/vision.md, and launchpad/naming.md into a single one-page pitch
  summary. Use when the user wants a pitch, a one-pager, a summary to share
  with others, or asks to "put it all together". Requires idea-capture (and
  ideally vision-crafting and business-naming) to have already run.
---

# pitch-one-pager Skill

Combine the project's existing artifacts into one shareable page. Don't
regenerate content that already exists in `launchpad/idea.md`,
`launchpad/vision.md` and `launchpad/naming.md`
— summarize and cite it, and only ask the user for something new if a
required field is genuinely missing from all three files.

## Output Location

All files this plugin writes go in the `launchpad/` folder at the root of
the user's project (the current working directory, even if it is a
subfolder of a git repo). Create the folder if it doesn't exist. Never write plugin
output anywhere else, and never into the plugin's own directory. If a
legacy copy of a plugin file (e.g. `idea.md`) exists at the project root and
the `launchpad/` one does not, tell the user and offer to move it — don't move or overwrite it silently.

---

## Phase 1 – Check What Exists

Read `launchpad/idea.md`, `launchpad/vision.md`, and `launchpad/naming.md` from the project if present.
If `launchpad/idea.md` is missing, tell the user to run `idea-capture` first — a
pitch with no structured idea behind it isn't worth assembling.
`launchpad/vision.md` and `launchpad/naming.md` are optional; note in the output if they're
missing rather than inventing placeholder content for them.

---

## Phase 2 – Assemble

Build a one-page structure with these sections, each 1-3 sentences pulled
and tightened from the source files (not copy-pasted verbatim if the
source is discursive):

1. **Name** (from `launchpad/naming.md`'s recommendation, or "(not yet chosen)")
2. **Problem**
3. **Solution**
4. **Target customer**
5. **Value proposition**
6. **Vision** (one line)
7. **Business model** (revenue)
8. **Why now / unfair advantage**

---

## Phase 3 – Deliver

Ask the user how they want to receive it before producing it:

- A **published Artifact** page (call the `artifact-design` skill guidance
  first) — best when they'll share the link with others.
- A local **markdown file** (`launchpad/pitch.md` in the project) — best when it
  feeds into another document or repo.

Don't default to one without asking — a one-pager's audience (investor,
cofounder, personal record) determines which format is actually useful.

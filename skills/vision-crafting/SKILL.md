---
name: vision-crafting
description: >
  Drafts vision, mission, and positioning statements for a business idea.
  Use when the user wants a vision statement, mission statement, or
  positioning statement, asks "what's our vision", wants to articulate
  where the business is headed, or after idea-capture has produced
  launchpad/idea.md and the user wants to move to the next step. Produces or
  updates `launchpad/vision.md`.
---

# vision-crafting Skill

Draft vision, mission, and positioning statements grounded in the idea's
actual substance — not generic corporate language. Avoid buzzword soup
("synergistic", "revolutionize", "empower", "seamless") unless the user's
own voice uses that register.

## Output Location

All files this plugin writes go in the `launchpad/` folder at the root of
the user's project (the current working directory, even if it is a
subfolder of a git repo). Create the folder if it doesn't exist. Never write plugin
output anywhere else, and never into the plugin's own directory. If a
legacy copy of a plugin file (e.g. `idea.md`) exists at the project root and
the `launchpad/` one does not, tell the user and offer to move it — don't move or overwrite it silently.

---

## Phase 1 – Gather Input

Read `launchpad/idea.md` if it exists in the project. If it doesn't, or is too thin to
work from, ask the user to run "idea-capture" skill first. 
Don't proceed on a blank slate.

---

## Phase 2 – Draft Three Statements

- **Vision** (aspirational, long-term, world-state): one or two sentences
  describing the change in the world this business is working toward, if
  it fully succeeds. Not about the company — about the world/market/users.
- **Mission** (what the company does, today, to get there): one sentence,
  concrete and active ("We help X do Y by Z"), not aspirational fluff.
- **Positioning statement**: use the standard form —
  "For [target customer], who [need/problem], [product name/category] is a
  [category] that [key benefit]. Unlike [primary alternative], we
  [key differentiator]."

Offer 2 variants for vision and mission — one more concise/punchy, one more
descriptive — and let the user pick or merge, rather than presenting a
single take-it-or-leave-it draft.

---

## Phase 3 – Sanity-Check

Before finalizing, check each statement against the idea document:
- Does the vision follow from the problem in `launchpad/idea.md`, or is it disconnected?
- Does the mission actually match the solution described, or does it promise
  more than the current solution delivers?
- Flag any mismatch to the user rather than smoothing over it.

---

## Phase 4 – Write `launchpad/vision.md`

Write (or update) `launchpad/vision.md` with the chosen Vision, Mission, and
Positioning statement, plus a short "why this wording" note for each so the
reasoning isn't lost.

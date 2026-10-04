---
name: business-naming
description: >
  Generates and scores candidate names for a business, product, or brand,
  then checks real-world availability. Use when the user wants help naming
  a company or product, asks "what should we call this", wants name ideas,
  or wants to check if a name is available/taken. Produces or updates
  `naming.md`.
---

# business-naming Skill

Generate names that fit the business's actual positioning, not generic
startup-name filler. Then verify candidates against reality before
presenting them as viable — a name nobody can register or find isn't a
recommendation.

---

## Phase 1 – Gather Input

Read `idea.md` and `vision.md` if they exist, for problem, customer, and
positioning. If neither exists, ask the user for: what the business does,
who it's for, and any naming constraints (must be a real word, must work in
Italian and English, must avoid a specific term, length limits, etc.).

Load `references/naming-approaches.md` for the generation techniques used
in Phase 2.

---

## Phase 2 – Generate Candidates

Produce 10-15 candidates spanning at least 3 different approaches from the
reference file (e.g. don't give 15 compound-word names). For each, add one
line on why it fits the positioning.

Filter out anything that:
- Is hard to spell from hearing it spoken aloud.
- Has an obvious negative meaning or connotation in Italian or English.
- Is a likely existing well-known brand in an unrelated category (flag for
  the user to double check, don't just silently drop it).

---

## Phase 3 – Score and Shortlist

Score the surviving candidates 1-5 on: memorability, pronounceability,
relevance to positioning, and room to grow (won't box the business into one
narrow product). Present as a table. Shortlist the top 4-6 for availability
checking — don't check all 15, that's wasted work if the top ones clear.

---

## Phase 4 – Check Availability

Dispatch the shortlist to the `name-researcher` agent to check domain
availability across common TLDs (`.com`, `.it`, and others), common social-handle availability, and any obvious
same-category trademark collisions. Do not claim a name is "available"
without this check — that's a factual claim the user will act on.

---

## Phase 5 – Write `naming.md`

Write (or update) `naming.md` with: the full candidate list and scores, the
shortlist, and the availability findings per shortlisted name. Recommend a
top pick with reasoning, but make clear it's a recommendation, not a
decision — naming is the user's call.

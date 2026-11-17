---
name: system-upgrade
description: "End-to-end upgrade of an existing web, Electron or Chrome-extension app: deterministic scan plus live browser check, evidence-based report across 10 dimensions (RTL, responsive, WCAG 2.2, design, UX states, forms, performance, setup, AI layer, code health), sprint plan and verified execution. Trigger on: upgrade the system, audit UX, fix RTL, system upgrade."
---

# System Upgrade — end-to-end upgrade of an existing system

This skill is the **orchestrator**. It runs in the main session and launches two separate agents (a sub-agent cannot launch a sub-agent):
`system-upgrader` (scans, plans, executes) and then `upgrade-evaluator` (a skeptical evaluator in a clean context). This separation is the key lesson
from Anthropic's harness design work: a model that grades its own work will praise it.

## Parameters
`/system-upgrade [path] [--mode product|brand|mixed] [--autonomy full|mechanical-only|plan-only] [--routes /a,/b] [--sprints S1-S3]`
- `path` — project root (default: cwd).
- `--mode` — `product` (dashboard/app/tool), `brand` (landing/marketing page), `mixed` (an app with a landing page). Default: auto-detect (marketing routes present means mixed).
- `--autonomy` — default **`full`** (owner decision, 2026-09-24): executes all sprints without stopping. `mechanical-only`: only S1 runs automatically, the rest is reported. `plan-only`: scan + REPORT + PLAN + "before" screenshots, without touching any code.
- Anything not specified — the agent decides and documents the decision in the REPORT.

## The 10 dimensions (full detail in `references/scoring.md`)
1 RTL and Hebrew · 2 Responsiveness · 3 Accessibility · 4 Design and brand · 5 UX flows and states · 6 Forms · 7 Perceived performance · 8 Ease of setup and operation · 9 AI layer · 10 UI code health.
Each dimension has a reference file with numbered rules, severity and Wrong/Right examples: `references/rtl-hebrew.md`, `responsive.md`, `a11y-wcag22.md`, `design-quality.md`, `ux-flows.md`, `config-and-ai.md`.

## Process (what the main session does)

### 1. Preparation
- Verify that `path` exists and that it is a git repo (if not, run `git init` + a baseline commit before anything else; if the user does not want git, stop and ask).
- Run `git status`. If the working tree is dirty, record it in the REPORT and let the upgrader create the branch `upgrade/<YYYY-MM-DD>` (it stashes or commits the existing work according to its own rules).

### 2. Launch `system-upgrader` (Agent tool, run_in_background: false)
The prompt must include: absolute path, mode, autonomy, routes if given, the instruction "follow `~/.claude/skills/system-upgrade/SKILL.md` — all steps 0-7", and the output location `<path>/.claude/upgrade/`.
The agent returns: a before/after table of the dimensions, the commits, the `[needs-human]` items, and the 3 next steps.

### 3. Launch `upgrade-evaluator` (Agent tool, fresh context)
The prompt must include: path, and "read `<path>/.claude/upgrade/UPGRADE-PLAN.md` and `UPGRADE-REPORT.md`; verify every contract for real (running app + detect.py); write `EVAL.md` following `templates/EVAL.md`; the default score is 5, and a score rises only with evidence". **Do not pass** it the upgrader's explanations of why something is fine.
In `plan-only` mode the evaluator assesses the **baseline state** and the quality of the PLAN (are the contracts measurable? is anything critical missing?).

### 4. Fix rounds (up to 2)
If EVAL = `ANOTHER-ROUND`, launch `system-upgrader` again with the list of FAILs only ("fix only these, do not open new fronts"), then the evaluator again. After 2 rounds, stop and report what remains.

### 5. Summary to the user (short, in the user's language)
The 10-dimension before/after table · what was done (commits) · what needs a human decision · links to the REPORT/PLAN/EVAL and the before/after screenshots · the 3 next steps.
Update memory (`memory/`) if something was learned about the project that cannot be derived from the code (for example: "in X the login blocks live testing — there is a public route at /demo").

## Deliverables (in `<path>/.claude/upgrade/`)
| File | Written by | What |
|---|---|---|
| `detect.json` | detect.py | Deterministic findings (file:line, rule, severity, fix) |
| `detect-ignore.json` | upgrader (with a reason) | Documented exceptions — do not repeat false positives |
| `browser.json` / `browser-after.json` | upgrader | Live-check results for every route × viewport × theme |
| `screenshots/before/`, `screenshots/after/` | upgrader | `<route>__<w>__<theme>.png` |
| `UPGRADE-REPORT.md` | upgrader | Baseline score + findings by severity (template `templates/UPGRADE-REPORT.md`) |
| `UPGRADE-PLAN.md` | upgrader | Sprints S1-S6 with contracts (template `templates/UPGRADE-PLAN.md`) |
| `EVAL.md` | evaluator | PASS/FAIL for every contract, scores, verdict (template `templates/EVAL.md`) |

## Running the tools manually
```bash
python ~/.claude/skills/system-upgrade/scripts/detect.py <root> --md            # Markdown summary + detect.json
python ~/.claude/skills/system-upgrade/scripts/detect.py <root> --out x.json    # exit 2 = there is a blocker/high finding
```
The live-browser protocol: `scripts/browser-pass.md`.

## Iron rules (apply to both agents)
1. **Evidence or nothing** — every finding needs `file:line` or `route@viewport` + a screenshot. `❓` (not checked) is better than a guess.
2. **Project rules take precedence** — `design-rules`, the project's standards file (for example `STANDARDS.md`), `BRAND.md`, `DESIGN.md`, `CLAUDE.md`. A conflict with the standard (for example a rule that mandates physical CSS classes) means a migration proposal in the PLAN, not a silent override.
3. **Small steps, never a rewrite** (iron rule #1 of the project standards). A huge file is split in its own sprint with its own contract.
4. **New Hebrew text** for the user (labels, errors, empty states) goes through the project's copywriting agent if one exists, otherwise through a Hebrew-copywriting skill (for example `anthropic-skills:hebrew-copywriting`).
5. **Do not touch** business logic, DB, auth, payments or API contracts — mark them `[needs-human]`. UI/UX/layout/tokens/a11y/copy only.
6. **git**: branch `upgrade/<date>`, one commit per sprint with a message like `upgrade(S2): rtl logical classes + tablet breakpoints`, with `lint` + `typecheck` (and tests, where they exist) clean before each commit. No force-push, no branch deletion.
7. **Live check before and after** on the same routes/viewports. If it cannot be run, the dependent dimensions are marked `❓` and receive no score.
8. **Definition of Done** = Professional (`scoring.md`): every dimension ≥ 8, 0 blocker/high, axe ≤ 2 per route, 0 console errors — or an explicit report of what is missing and why.

# Claude Code Tools by Ofir Shudari

A collection of custom Claude Code skills and subagents, built while running a
real multi-tool software portfolio day to day. Each one grew out of an actual
repeated need, not a hypothetical — most were extracted after doing the same
manual check three or four times by hand.

Free to use, copy, and adapt. No installer, no dependencies beyond Claude
Code itself.

## What's a "skill" vs an "agent" here?

- **Skills** (`skills/<name>/SKILL.md`) are instructions Claude Code loads
  when you type `/name` or when your request matches the skill's trigger
  phrases. They run in your current conversation.
- **Agents** (`agents/<name>.md`) are subagent definitions — a named
  persona with its own tool access and (optionally) its own model, that the
  main session can delegate a task to and get a report back from.

## Install

Copy the file(s) you want into your own Claude Code config:

- **Project-only** (only active inside one repo): copy into that repo's
  `.claude/skills/<name>/` or `.claude/agents/<name>.md`.
- **Global** (active in every project): copy into `~/.claude/skills/<name>/`
  or `~/.claude/agents/<name>.md`.

Skills that are just a single `SKILL.md` file: copy the whole folder.
`system-upgrade` also ships `references/`, `templates/`, and `scripts/` —
copy the entire `skills/system-upgrade/` folder, not just `SKILL.md`, or it
will be missing its reference material and detector script.

No build step, no `npm install` — these are plain Markdown (and one Python
script with no third-party dependencies).

---

## Skills

### `release-checklist`
Runs a version-release checklist before you ship a build for any tool in a
multi-project folder — checks that the version number is in sync everywhere
it needs to appear (`version.json`/`package.json`/`.csproj`/`manifest.json`,
the installer filename, the About screen, `CHANGELOG.md`), that the installer
was actually rebuilt (not a stale copy sitting next to updated code), and
that the project root is clean of leftover build artifacts. For electron-builder
apps specifically, verifies the update-feed files (`latest.yml`, `.blockmap`)
were actually uploaded alongside the installer and not just the bare `.exe` —
missing them breaks the app's "check for updates" silently, with no error
until a user hits it. Falls back to a
project's own `RELEASE-CHECKLIST.md` when one exists, otherwise applies a
global set of rules. Triggers on: "ready to release", "check before release",
"new version", "before I ship the installer", "check before publish".

### `grep-audit-callers`
Before changing a shared function, method, API, or type: maps every caller
across the *entire* project tree first (not just the file containing the
definition), classifies each one (needs no change / needs an update / dead
code), and reports the full list before any edit is made. This exact
discipline — audit first, edit second — found 3 separate real bugs across 3
rounds in one of the author's own projects, all cases where a change was
tested only where it was made and broke a caller elsewhere. Also covers a
shared Python module layer (a scripts folder where most files import from a
handful of common modules) — the same audit-before-edit discipline, just a
second concrete case for it. Triggers on: "change this function", "change
the signature", "refactor", "who calls this", "change a shared API/module".

### `secrets-hygiene-check`
Zero-secrets check before a commit or release: greps source code (excluding
`node_modules`/`dist`/`build`) for common secret patterns — API keys, tokens,
passwords, connection strings, embedded private keys — verifies `.gitignore`
covers `.env` and credential files, and checks that config is actually loaded
from environment variables or a local, gitignored config file rather than
hardcoded. Every finding must cite a real file+line; anything ambiguous is
flagged for manual review instead of guessed. If a real secret is found, it
stops and reports rather than continuing with commit/release/publish.
Triggers on: "check for secrets", "before commit", "zero secrets", "worried
about a leaked key", "security check before release".

### `daily-project-brief`
A short status brief across every tool in a multi-project folder — what's
stuck, what's stale, what needs attention — built from each project's own
`CHANGELOG.md`/`version.json` sync state and a central standards/status
document. Deliberately narrow: 5-7 lines, sorted by urgency, no full audit.
Points to a deeper audit skill/agent when something needs more than a
one-line flag. Once a month only, also flags skill folders that haven't
been touched in 30+ days as a candidate for review — never deletes anything
itself, just surfaces the list. Triggers on: "what's the status of my
projects", "daily brief", "what's stuck", "status of all tools".

### `system-upgrade`
The largest one here. An end-to-end upgrade workflow for an existing web
app, Electron app, or Chrome extension: scores the app across 10 dimensions
(RTL/i18n, responsive design, accessibility to WCAG 2.2, visual design
quality, UX flows and empty/error/loading states, forms, perceived
performance, ease of setup/configuration, any AI-feature layer, and general
UI code health), using a deterministic detector script (`scripts/detect.py`)
plus live browser verification — not just a code read. Produces a
before/after report and a sprint plan with measurable contracts, executes
the plan with git commits and before/after screenshots per sprint, and hands
off to a *separate* skeptical evaluator pass (see `upgrade-evaluator` below)
rather than grading its own work. Ships with reference material for each of
the 10 dimensions (`references/`) and report/plan templates (`templates/`).
Triggers on: "upgrade the system", "go through this and improve it", "this
app is a mess", "fix RTL", "mobile compatibility", "audit the UX".

---

### `bloom-designer`
A global (project-independent) design skill for the [Bloom](https://www.trybloom.ai/) MCP
connection — on-brand image, SVG, video, and audio generation/editing for any brand you manage
there, not tied to one project or client. Handles the operational parts a raw tool list doesn't:
discovering Bloom's tools (registered under a random per-install prefix, so it resolves the right
name via `ToolSearch` first), finding-or-creating the right Brand session instead of duplicating
one, checking credit balance before any batch of more than 2-3 images (Bloom is a paid,
credit-metered service), searching the Brand Library for reusable references before generating
from scratch, and requiring explicit confirmation before an `apply_brand_edit` call that changes
the *active* brand identity rather than producing a one-off asset. Requires the Bloom MCP
connector to actually be connected in your Claude setup — the skill just orchestrates it, it
doesn't provide the connection itself.
Triggers on: "design this with Bloom", "generate a branded image", "update the brand identity in
Bloom", "how many Bloom credits do I have".

---

## Agents

### `system-upgrader`
The executor half of the `system-upgrade` workflow (loads that skill). Scans
an existing system end to end and upgrades it — RTL/Hebrew, mobile/desktop,
WCAG 2.2 accessibility, non-generic modern design, UX/states/forms, ease of
setup, an AI layer if the app has one. Runs the deterministic detector plus a
live browser pass, prioritizes findings, and fixes them in git-committed
sprints with before/after screenshots. Always meant to be followed by
`upgrade-evaluator` — never trust the same agent to grade its own upgrade.

### `upgrade-evaluator`
A separate, skeptical evaluator for `system-upgrader`'s output, run in a
*fresh context* with no visibility into the upgrader's own reasoning (this
separation is the actual point — a model evaluating its own work tends to
grade generously). Reads the upgrade plan and report, re-runs the detector,
opens the live app in a browser, checks every sprint's contract for real,
and scores each of the 10 dimensions 1-10 with cited evidence, returning a
PASS/FAIL verdict. Read-only — never edits code.

### `page-upgrader`
Like `system-upgrader`, but scoped to one page or module (e.g. `/calendar`,
`/settings`) instead of a whole app. Adds a dedicated research step — what
does a page of this *kind* typically need? — before auditing what's missing,
then upgrades design/UX for mobile and desktop separately, verifying
`tsc`/`eslint`/build pass before committing. Also loads the `system-upgrade`
skill for its base RTL/accessibility/design rules.

### `tool-standards-audit`
Runs a full, evidence-based audit of one tool in a multi-project folder
against a central standards document — checks the code as it stands today
(never trusts a prior audit's claims without re-verifying them against the
current source), covers root-folder cleanliness, version-number sync,
zero-secrets, RTL/i18n, installer language and install location, single-
instance handling, DPI awareness, and clean uninstall — then updates that
tool's audit file and the shared status table. Every line in its report must
cite a real file+line; a genuine unknown is marked as such rather than
guessed. Read-only over app behavior — reports, doesn't fix code, unless
explicitly asked to.

---

## A note on customization

`release-checklist`, `daily-project-brief`, and `tool-standards-audit` were
written against one specific person's folder layout (a `PC-Software/` and
`Chrome-Extensions/` split, a shared `_AUDIT/STANDARDS.md` status file). The
*mechanism* each one implements — sync-checking a version number across
every file it appears in, mapping every caller before touching a shared
function, refusing to grade your own upgrade — is general. Treat the paths
and file names in these three as a worked example to adapt to your own
project structure, not a hard dependency.

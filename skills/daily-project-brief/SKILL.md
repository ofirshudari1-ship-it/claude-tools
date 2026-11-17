---
name: daily-project-brief
description: "Short status brief across every tool in a multi-project folder: what is stuck, stale or needs attention, built from each project's CHANGELOG, version files and a central standards document. Trigger on: daily brief, project status, what's stuck, status of all tools."
---

# Daily Project Brief

A focused status brief covering **only the files in this working folder** (not email or calendar; that is the job of the general `morning` skill, so do not duplicate it here). Purpose: a fast answer to "what needs attention right now" without opening every SPEC/CHANGELOG by hand. Trigger: the user asks for a daily brief, project status, or "what's stuck". Input: the multi-project folder and its standards document. Output: a short prioritized list (see step 4).

## Steps

1. **Scan the status table in your standards document** (the central file that defines per-tool requirements) and find every row marked with a red X or a question mark in the core columns (build passes, zero secrets, version in sync, clean root).
2. **For every active tool under your desktop-software and browser-extension folders**, check:
   - The latest date/version in `CHANGELOG.md` against `version.json` / `package.json` / `manifest.json` (a mismatch is a red flag).
   - Whether old build/installer files are left in the project root (a hint of a release round that was never finished).
   - If `<project>/PROJECT.md` exists (a private, gitignored status document), read it before anything else: it already holds links, update status and "what is still open", so you do not re-derive them each time. If it does not exist for a tool, do not create one proactively as part of the daily brief.
3. **Check the digi-transform pipeline state** (the root-level `proposals/` and `reports/` folders): are there `proposals/*.md` files not marked as applied, and when did `/weekly` last run (judged by the date of the newest file in `reports/`)?
4. **Output: a short, focused list**, not a full audit: at most 5-7 lines, ordered by urgency. Examples:
   - "Tool X: version out of sync between CHANGELOG and package.json"
   - "digi-transform: 3 proposals not applied since DD/MM"
   - "Tool Y: not updated for 60+ days, check whether it is still relevant"
5. If something needs a deeper check, point to running the `tool-standards-audit` skill (as a subagent) on that specific tool. Do not perform a full audit yourself here.
6. **Once a month only** (if 30+ days have passed since the user last got a skills review; ask the user, because there is no automatic way to know), also run an unused-skills review: use `Bash: find ~/.claude/skills "<your multi-project folder>/.claude/skills" -maxdepth 1 -type d -newermt` inverted (mtime older than 30 days) over each skill folder. Report a short list of skills not edited or updated in 30+ days, without recommending deletion on your own: this is input for the user's decision, not an automatic removal. Do not run this step on every regular daily run.

## Explicit boundaries

- No reading of email, calendar, WhatsApp or any external communication channel; that belongs to `anthropic-skills:morning`, not this skill.
- No editing of files; this is a reporting-only skill. If a red X is found that needs fixing, suggest the user run `release-checklist` or `tool-standards-audit` separately.

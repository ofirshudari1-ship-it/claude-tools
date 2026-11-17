---
name: release-checklist
description: "Runs a release checklist before shipping a build: version sync across manifests, installer rebuilt, update-feed files uploaded, clean project root. Uses the project's own RELEASE-CHECKLIST.md when present. Trigger on: ready to release, new version, before I ship the installer."
---

# Release Checklist: every tool in the multi-project folder

Purpose: before marking a release/build as "done" for any tool in your desktop-software or browser-extension folders, run the checks below. Trigger: "ready to release", "new version", "before I ship the installer", "before publish". Input: the tool name or path. Output: a ticked checklist with any failed item reported. Do not skip a step because "it is only a small version": your standards document defines this as an iron rule that also applies to small changes.

## Step 1: identify the project and its relevant checklist

1. Identify the tool name from the request/path (for example `<desktop-software folder>/AutoProcessTwin`, `<desktop-software folder>/FamilyQuest PC`, `<extensions folder>/TabToTable-AI`).
2. Look for `<project>/RELEASE-CHECKLIST.md`.
   - **If it exists** (currently: AutoProcessTwin), follow it **as is, line by line**. Do not duplicate its content here and do not invent a parallel version: it is the source of truth for that tool.
   - **If it does not exist** (FamilyQuest PC, TabToTable-AI, other tools), continue to step 2.

## Step 2: the global sync rule (from your standards document)

When there is no dedicated checklist file, enforce the following iron rules, all **in the same action**:

- [ ] The version number is updated simultaneously in every place: `version.json` / `package.json` / `.csproj` / `manifest.json`, the installer file name (`<Tool>-Setup-<version>.exe`), the window title or About screen, and `CHANGELOG.md`. None may lag behind another.
- [ ] The installer/build itself is **actually rebuilt** and replaced in the project root: no stale or version-mismatched file may sit next to updated code.
- [ ] **If the tool uses electron-builder:** `gh release upload` / `create` must upload three files, not only the .exe: `<Tool>-Setup-<version>.exe`, `.exe.blockmap`, and `latest.yml`, all from `dist/` or `build/release/` (one consistent copy; do not mix an .exe from the root with a latest.yml from a `dist/` built in a different round). Without `latest.yml` the "Check for Updates" feature fails completely (documented in practice; see section 11.1 of your standards document). Verify after upload: download `.../releases/latest/download/latest.yml` and the .exe and compare sha512. If they do not match on the first check, wait a few seconds and retry (GitHub CDN delay after `--clobber`) before flagging a failure.
- [ ] `CHANGELOG.md` records exactly what changed (Keep a Changelog: Added/Changed/Fixed/Removed).
- [ ] `SPEC.md` is updated if functionality changed.
- [ ] `README.md` is updated if installation or usage changed.
- [ ] The root folder is clean: only installer/CHANGELOG/SPEC/README (no build scripts, intermediate `dist/`/`build/`, or duplicates of an old installer).
- [ ] Zero secrets in code (if in doubt, run the `secrets-hygiene-check` skill).

## Step 3: FamilyQuest PC specific rule

Based on a documented lesson from memory: **every upgrade to FamilyQuest PC must, together and in the same action**:

- [ ] Update the landing page (an Artifact): find it with the `Artifact` tool `action: "list"`, read its current content, and publish an updated version reflecting the new features/version. Do not leave it with an old version number or old features.
- [ ] Update `package.json`'s `"version"` (not only README/SPEC; the documented bug: the version stayed `1.0.0` through several rounds while the README had already been updated with new numbers).
- [ ] Run `npm run build && npm run dist` to actually rebuild the installer, not just commit the code. The file name is stable (`FamilyQuest-PC-Setup.exe`, with no `${version}` in the name); every `npm run dist` overwrites the same file, so **do not put** `${version}` back into the file name.
- [ ] After every build, delete `release/win-unpacked/` (an intermediate folder of roughly 250MB+ that is fully reproducible). Only `.exe` / `.blockmap` / `latest.yml` / `builder-debug.yml` stay in `release/`.

## Step 4: wrap-up

- [ ] Update `<project>/PROJECT.md` if it exists (a private, gitignored status document): the version number, the "what was done last" line, and any link or gap that changed in this round. If the tool has no `PROJECT.md` yet, do not create one proactively as part of a regular release; that is a separate extension, not part of the basic checklist.
- [ ] Update the matching row for the tool in the status table of your standards document.
- [ ] If `<audit folder>/AUDIT-<Tool>.md` exists, update it accordingly.
- [ ] If the project uses git, offer to tag the version (`git tag vX.Y.Z`); do not do it automatically.
- [ ] This is a quick pre-release checklist, not a full audit. If something needs a deeper check (suspected old drift from the standards, a tool that has not been audited in a long time, doubt whether the existing audit is still correct), point to running the `tool-standards-audit` agent on that tool; do not run a full audit yourself here.

## Notes

- This is an enforcement/checklist skill. It does not replace a manual test of the functionality itself (smoke test); if a dedicated `RELEASE-CHECKLIST.md` exists, it covers that too.
- If a tool that ships regularly (such as FamilyQuest PC or TabToTable-AI) turns out to lack a `RELEASE-CHECKLIST.md`, it is worth offering the user to create one modeled on AutoProcessTwin's, but only on explicit request, never proactively in the middle of a release.

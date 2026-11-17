---
name: grep-audit-callers
description: "Before changing a shared function, module or API, maps every caller across the whole project tree, classifies each (no change, needs update, dead code) and reports the full list before any edit. Trigger on: change this function, refactor, who calls this, change a shared API."
---

# Grep Audit Callers: before changing shared code

Purpose: when asked to change a function, method, API, shared type, or any file with several consumers, never edit the definition first and check afterwards. The order is the reverse. Trigger: "change this function", "refactor", "who calls this", "change a shared API". Input: the symbol (function/type/API) to be changed. Output: a complete, classified list of callers reported to the user before any edit, then the change applied to the definition and all flagged callers.

## Steps

1. **Map all callers before any edit.** Run Grep over the **entire project tree** (not only the file holding the definition) for the function/symbol name, including variations: imports, direct calls, calls through an object/module, and usage in tests.
2. **Classify every caller found:**
   - No change needed: uses the interface in a way that stays valid.
   - Needs update: a call that will break or behave differently after the change.
   - Dead code: a caller that is not actually used (discovered along the way, not the goal of the search).
3. **Report the full list to the user before touching code:** which files, how many calls, and which of them need an update. Do not start editing on the assumption "it is probably only this one place".
4. **If the callers span several layers** (for example UI + service + tests, or extension background + content script + popup), the change plan must cover all layers in the same editing round, not only the first layer found.
5. Only after the mapping and the report, make the change in the definition and in every caller marked for update.

## Why this matters in these projects

In an earlier code review of AutoProcessTwin (a desktop automation tool), this method exposed 3 separate bugs across 3 separate rounds. All were cases where a caller was forgotten because the change was only checked at the place that initiated it. This is not a theoretical method; it has already proven itself on this code.

## When it is not needed

- A fully local change to a private (`private` / non-exported) function whose scope is known and closed to a single file: a quick grep inside the file is still worthwhile, but the full process is not needed.
- Adding new code without changing any existing signature or behavior.

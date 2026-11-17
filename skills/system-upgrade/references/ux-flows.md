# UX: flows, states, forms, navigation, copy, onboarding

Sources: Vercel guidelines (forms/navigation/content/tooltips), Nielsen heuristics, `impeccable` harden/onboard/clarify, STANDARDS §5/§14.4/§16/§18.3.

## U-1. The four states of every list/form/widget: high
| State | Requirement |
|---|---|
| **empty** | Not a bare "No data": a short explanation + a primary CTA (Hebrew example: "הוסף משימה ראשונה" = "Add your first task") + a light illustration/icon; realistic demo data in onboarding (not lorem/example.txt) |
| **loading** | A skeleton in the final structure (150-300ms delay, visible >= 300ms), not a lone spinner; `aria-busy` |
| **error** | What happened + what to do + a "Try again" button; no stack trace; no `alert()` |
| **success** | Immediate confirmation (toast/checkmark), then back to the working state |
Plus **sparse** (one item) and **dense** (200 items: virtualize / pagination / "See all"): check both. Very long content (an 80-character name) does not break the layout.

## U-2. Forms: high
- Minimum fields; optional fields are marked (not "required" asterisks on 8 of 9 fields).
- Enter submits in a single-field form; Ctrl/Cmd+Enter in a textarea.
- Submit is **not** disabled before the first attempt: the user clicks, gets errors next to the fields, and focus goes to the first one. During submission: disabled + spinner + the text stays.
- Do not block typing (input masks): allow any input and validate; trim whitespace.
- `autocomplete`/`name`/`type`/`inputmode`; placeholder = a format example ("050-1234567"), not a label.
- Unsaved changes: warn before navigating away (`beforeunload` / router guard).
- Multi-step form: progress, "Back" keeps values, never ask again (3.3.7).
- Delete/destructive action: confirm **or** Undo (prefer a 5s Undo toast).

## U-3. Navigation and state: high
- Navigation = `<a href>` (Cmd+click, back, share). `router.push` inside a `<div onClick>` is a finding.
- **URL = state**: active tab, filter, search, page, open panel all live in query params (`?tab=...&q=...`). Refresh/Back/share restore them.
- Back/Forward restore scroll; `scroll-margin-top` for anchored headings.
- A clear active state in navigation (`aria-current="page"`); breadcrumbs at depth > 2; every important page is <= 3 clicks from home.
- Identical navigation on all pages and in the same order (mobile and desktop).
- `document.title` reflects the context (Hebrew example: "משימות · HOMEY" = "Tasks · HOMEY").

## U-4. One primary action per screen: medium (STANDARDS §3)
One primary button (filled accent), secondary as outline, tertiary as text. If a screen has 3 accent buttons there is no hierarchy. A command bar / FAB on mobile for the most frequent action.

## U-5. Optimistic UI and perceived speed: medium
Frequent actions (toggle, checking off a task, like) update immediately and roll back on failure with a message. Target: POST/PATCH under 500ms perceived. A skeleton instead of a white screen; `content-visibility: auto` / virtualization for lists over 100 items.

## U-6. Copy: medium (in Hebrew: via the copywriting agent / hebrew-copywriting)
- Verb + object on a button: "Save changes", not "Continue"; the same verb across the flow (Hebrew: "פרסם" -> "פורסם" = "Publish" -> "Published").
- An error = what happened + what to do (Hebrew: "הטלפון צריך 10 ספרות, למשל 0501234567" = "The phone number needs 10 digits, for example 0501234567"), not "Invalid input".
- An option that opens a continuation gets an ellipsis ("Rename..."); a loading state reads "Saving..."; use the single `…` character.
- Numbers: "8 tasks", not "eight"; units with a space `10 MB`; `&nbsp;` between a number and its unit.
- Tone: second person, active, short, human; no "Oops!"/"Something went wrong" without details.
- Inline help > tooltip; tooltips only for icons.
- Consistent terminology (GLOSSARY, §20.4: use "Settings", not "Options", in the same context).

## U-7. Onboarding and TTFV: medium (§18.3)
- Metric: **time to first value < 60 seconds**, not a number of screens. About 30% of onboarding steps are unnecessary.
- A visible "Skip" at every step; progressive disclosure (a tip the first time a feature becomes relevant), not a dump.
- A "finish setup" checklist (3-4 items) instead of a one-time wizard.
- The empty state of the first module is the real onboarding.

## U-8. Modals, drawers, toasts: medium
- A modal only for an action that needs a decision; long editing goes to a page/drawer.
- Toast: `aria-live`, 3-6s, one action (Undo), never a stack of 5.
- Every overlay: Esc closes, clicking outside closes (except forms with changes), focus trap, background scroll locked, correct RTL.
- Bottom-sheet on mobile, a centered dialog on desktop (`items-end sm:items-center`).

## U-9. Consistency and predictability: medium
The same component behaves the same everywhere (a clickable card in every module or in none); the same icons for the same actions; the same location for "Help"/"Contact" (3.2.6). Settings/Uninstall/Update UX follow STANDARDS §16.

## U-10. Robustness: medium (impeccable `harden`)
- Long text, an empty name, 0 items, 10k items, offline, timeout, a 401 mid-action, a wrong device clock, double-click on submit, returning from the background on mobile.
- A clean console (0 errors, warnings explained) on every route.

## Report format
`route@viewport - [ux] <state/flow> - <finding> -> <fix>` + screenshot; a code finding: `file:line - [ux] ...`.

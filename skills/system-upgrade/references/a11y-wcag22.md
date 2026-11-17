# Accessibility: WCAG 2.2 AA + Israeli Standard 5568 (IS 5568)

Sources: WCAG 2.2 AA audit checklist 2026 (digitalapplied), WebAIM Million 2026, Israeli Standard 5568 (IS 5568), based on WCAG (= WCAG 2.0/2.1 AA; a legal requirement in Israel under Regulation 35), STANDARDS §14.3/§18.2/§20.1-20.2, Vercel guidelines.

## Why this is not "nice to have"
An Israeli business whose site or app is not accessible is exposed to lawsuits. IS 5568 also requires an **accessibility statement page** with the name of an accessibility coordinator, contact details and an update date. axe/Lighthouse catch about 57% of issues by volume but only about 30% of the success criteria, so **a manual finding is worth more than a score**.

## The 5 passes (in this order)
1. **Automated**: axe-core on every route (mobile + desktop, light + dark). Catches: contrast, missing alt, missing label, empty button/link, missing `lang`, invalid ARIA, heading order.
2. **Keyboard**: Tab through the whole screen. Every interactive element is reachable, the focus ring is **visible**, order is logical (RTL reading order), Enter/Space activate, Esc closes, no keyboard trap, focus is not hidden under a sticky header / bottom nav (2.4.11).
3. **Screen reader** (NVDA / Narrator / VoiceOver): name, role and state are announced; `aria-live` for toasts and async updates (4.1.3); ARIA matches behavior.
4. **Reflow + zoom**: 320px width, 200% zoom, text-spacing bookmarklet. No clipping, no two-axis scrolling, no overlap.
5. **The new 2.2 criteria**: see A-9.

## A-1. Contrast: high (the most common failure: 84% of sites)
- Normal text >= 4.5:1; large text (>= 18pt or >= 14pt bold) >= 3:1; **non-text UI components** (input border, focus ring, tappable icon) >= 3:1 against their surroundings (1.4.11).
- Check light and dark **separately**: a palette that works in one does not necessarily work in the other (§20.1).
- `text-ink-dim` / `text-gray-400` on a light background usually fails. Placeholder text also needs 4.5:1.
- Tools: axe measures it; use the WebAIM Contrast Checker for every new accent before it enters code; APCA as a secondary measure.

## A-2. Images and icons: high (53%)
- `<img alt="description">`; decorative images get `alt=""`; `<svg aria-hidden="true">` inside a button that has text.
- **An icon-only button with no text** needs `aria-label="..."` (in the page language, e.g. Hebrew). lucide icons are `aria-hidden` by default, so the button itself must have a label.
- An icon that conveys meaning on its own (status) needs accompanying text or an `aria-label`.

## A-3. Forms: high (51%)
- Every field has `<label htmlFor>` (or `aria-label`/`aria-labelledby`); placeholder is not a label.
- `autocomplete` (1.3.5): `name`, `email`, `tel`, `street-address`, `cc-number`, `one-time-code`.
- Correct `type`/`inputmode`: `tel`, `email`, `numeric`, `decimal`, `url`.
- Errors: `aria-invalid="true"` + `aria-describedby` pointing to the message, the message **next to the field**, focus moves to the first error on submit, wording says what to fix (3.3.3).
- Do not block typing; do not lock submit before the first attempt; no `alert()`.
- `spellCheck={false}` for email, codes and usernames.

## A-4. Semantics: high
- Navigation = `<a href>` / `<Link>` (Cmd+click, middle-click, screen reader); action = `<button type="button">`. **Not** `<div onClick>` / `<span onClick>` / `<li onClick>`.
- Landmarks: `<header>`, `<nav aria-label="Main">`, `<main>`, `<footer>`; heading hierarchy h1 -> h2 -> h3 with no skipped levels; one `h1` per page.
- A skip link ("Skip to content") is first in the DOM.
- Empty `<button>` / empty `<a>` (46% / 31% of sites): always give text or an `aria-label`.
- Lists = `<ul>/<ol>`; data tables = `<table>` with `<th scope>`.
- Use ARIA only when no native element exists (`role="dialog" aria-modal="true" aria-labelledby`).

## A-5. Focus: high
- `outline-none` / `focus:outline-none` is **forbidden** without `focus-visible:ring-2 focus-visible:ring-offset-2` (2.4.7 + 2.4.13 Focus Appearance: >= 2px, 3:1 contrast).
- Modal: focus trap; focus moves into the dialog on open and returns to the trigger on close; `inert` on the background.
- Dropdown/menu: arrow keys navigate, Esc closes, Home/End work.
- After SPA navigation: focus moves to `<main>` or the h1, and `document.title` updates.

## A-6. Status not by color alone: medium (1.4.1)
Red = error / green = success must also have an icon or text. Charts: a color-blind-safe palette plus labels/patterns.

## A-7. Motion: medium
`@media (prefers-reduced-motion: reduce)` disables or shortens animations; `transition: all` is forbidden (be explicit: `transition-colors`, `transition-transform`); no autoplay longer than 5s without a pause control; animations 150-250ms (§18.5). No parallax or blinking.

## A-8. Dynamic updates: medium
Toast/status = `role="status"` / `aria-live="polite"`; a critical error = `role="alert"`; a cart or notification counter that updates needs `aria-live`. Loading: `aria-busy="true"` on the region.

## A-9. WCAG 2.2: the 9 new criteria
| # | Criterion | Level | Check |
|---|---|---|---|
| 2.4.11 | Focus Not Obscured (Minimum) | AA | Tab near a sticky header / bottom nav / cookie banner: the focused element is not fully hidden |
| 2.4.12 | Focus Not Obscured (Enhanced) | AAA | (optional) not hidden at all |
| 2.4.13 | Focus Appearance | AAA, recommended | ring >= 2px, 3:1 |
| 2.5.7 | Dragging Movements | AA | every drag (kanban, slider, reorder) has a click/tap/keyboard alternative |
| 2.5.8 | Target Size (Minimum) | AA | >= 24x24 or enough spacing; aim for 44 on mobile |
| 3.2.6 | Consistent Help | A | help/contact is in the same place on every page |
| 3.3.7 | Redundant Entry | A | a multi-step form does not ask again for information already entered |
| 3.3.8 | Accessible Authentication (Minimum) | AA | login without a cognitive test; password manager / paste work; OTP uses `autocomplete="one-time-code"` |
| 3.3.9 | Accessible Authentication (Enhanced) | AAA | (optional) |

## A-10. Israeli Standard 5568 (IS 5568), based on WCAG: Israel-specific
- [ ] An `/accessibility` page (accessibility statement) exists and is linked from the footer on every page. It includes: conformance level, accessibility coordinator (name + phone + email), update date, accommodations made, and a way to report a problem.
- [ ] `lang="he"` + `dir="rtl"` for Hebrew pages; captions for video; documents (PDF) are accessible or have an alternative.
- [ ] An accessibility widget **does not replace** real accessibility in the code; it is only an addition.

## A-11. Desktop (WPF/WinForms/Electron): STANDARDS §18.2/§20.2
- Custom-drawn controls need `AutomationProperties.Name` (WPF) / `AccessibleName` (WinForms) so Narrator knows what they are.
- Windows High Contrast: check `SystemParameters.HighContrast` / Electron `nativeTheme.shouldUseHighContrastColors` and respect `SystemColors`; do not override with a brand gradient.
- Tab order = visual reading order, not creation order.

## Report format
`file:line - [a11y] <criterion> - <finding> -> <fix>`; a browser finding: `route@viewport - [a11y] ...` + screenshot.

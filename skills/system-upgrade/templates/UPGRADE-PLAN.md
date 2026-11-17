# UPGRADE PLAN — <system name>

> Based on the UPGRADE-REPORT from <date>. autonomy: <full | mechanical-only | plan-only>. branch: `upgrade/<YYYY-MM-DD>`.
> Each sprint = one commit (or several small ones), lint + typecheck clean before the commit, re-detect + "after" screenshots at the end.
> Iron rule: small steps, no rewrite, no change to business logic / DB / auth (→ `[needs-human]`).

## Direction (brand mode only — 3 lines)
1. The signature element: …
2. Typeface + palette: …
3. "The one thing" people will remember: …

## Sprints

### S1 — Mechanical and automatic (low risk)
**Scope:** … (for example: eslint-plugin-rtl-friendly --fix, a missing token, dvh, min-h-0, transition-all)
**Contract (Done when):**
- [ ] `detect.py` → 0 `rtl.physical-class` findings in `src/components` (exceptions marked `rtl-exception`)
- [ ] `npx eslint` + `npx tsc --noEmit` clean
- [ ] "after" screenshots at 3 viewports identical to "before" **except** … (no visual regression)
**Risk:** … · **`[needs-human]`:** …

### S2 — RTL / layout / responsive
**Scope:** …
**Contract:**
- [ ] No overflow-x at 375 on N routes (browser.json)
- [ ] Targets < 44px = 0 at 375
- [ ] The mirror test passes on N routes + modals
- [ ] Project rules updated (design-rules R3 → logical) if approved
**Risk:** … · **`[needs-human]`:** …

### S3 — Accessibility
**Contract:**
- [ ] axe violations ≤ 2 per route (light + dark)
- [ ] 0 `a11y.div-onclick`, 0 `a11y.icon-button-no-label`, 0 `a11y.outline-none`
- [ ] Tab pass on N routes: focus ring visible, not hidden
- [ ] An accessibility statement exists and is linked (Israeli Standard SI 5568)

### S4 — Design and polish
**Contract:**
- [ ] 0 `design.hex-in-tsx` (except token/theme files)
- [ ] Type scale: 0 `text-[≤11px]` outside badges
- [ ] dark: every token in all 3 blocks; `color-scheme` + `theme-color`
- [ ] "Remove one accessory" done on N screens

### S5 — UX flows / states / forms
**Contract:**
- [ ] 4 states for every main list (empty/loading/error/success) — lists: …
- [ ] Forms: labels/autocomplete/inputmode/errors next to the field — forms: …
- [ ] URL state for tabs/filters in …
- [ ] 0 `window.alert/confirm`

### S6 — Setup and AI
**Contract:**
- [ ] Settings grouped, instant save with feedback
- [ ] At least one AI pattern embedded with edit-before-save + fallback: …
- [ ] `[needs-human]`: …

## Execution order and dependencies
S1 → S2 → S3 → S4 → S5 → S6. S3/S4 can run in parallel after S2.

## Out of scope (explicit)
- …

## Final target
Professional: every dimension ≥ 8, 0 blocker/high, axe ≤ 2, 0 console errors. (See scoring.md)

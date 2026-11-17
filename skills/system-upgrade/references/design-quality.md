# Design quality: modern, marketing-grade, distinctive, not generic

Sources: Anthropic `frontend-design` skill, `impeccable` (pbakaus) audit rules, Vercel guidelines (visual design), SaaS design trends 2026 (Linear/Vercel/Attio/Stripe), STANDARDS §3/§15/§18.5/§19/§21.

## D-0. First: brand mode or product mode?
| | **brand** (landing page, marketing site, onboarding, splash) | **product** (dashboard, app, settings, work tools) |
|---|---|---|
| Goal | emotion, differentiation, conversion | speed, clarity, the right information density |
| Typography | a distinctive display font + large sizes, a hero characteristic of the domain | compact scale, hierarchy from weight and spacing |
| Color | strong accent, **one** dominant gradient/image | color reserved for state and meaning; quiet chrome |
| Motion | one orchestrated load sequence | micro-interactions of 150-250ms only |
| Layout | full-bleed, deliberate asymmetry, whitespace | grid, tables before charts, cards only for entities |
Do not mix: a dashboard with a hero gradient is slop; a landing page that looks like an admin panel does not convert.

## D-1. Anti-"AI slop": the blacklist (medium each)
- A default font (Inter / Roboto / Arial / system-ui) as the **only** font. For Hebrew: Assistant/Heebo/Rubik/Noto Sans Hebrew; pick **one** primary and at most one secondary.
- A purple->blue gradient / warm-cream + terracotta / near-black + acid-green as a default with no brand reason.
- Cards inside cards; everything in `rounded-2xl shadow-lg`; the same border-radius on every element.
- Eyebrow labels in `uppercase tracking-widest`; highlighting one word in color in a headline; emoji as icons.
- A 3-column "features" row with an identical icon-title-paragraph; inflated stats in the hero.
- Pure gray (`#808080`, `gray-500`) on a colored background; pure black `#000` for text (prefer a tinted dark ink).
- `bounce`/`elastic` easing; `transition: all`; hover that enlarges with `scale-110`.
- **Test:** if you can swap the logo and it looks like every other SaaS, it is slop.

## D-2. Commit to one design direction: high (brand mode)
Before changing anything, write 3 lines of "direction" in the PLAN: (1) the element most characteristic of the product's world (smart home? family? files?) and how it appears in the hero; (2) font + palette (max 2 fonts, one accent + neutrals); (3) the "one thing" people remember. If a `BRAND.md`/`brand-kit.json` exists, it is the source; do not invent.

## D-3. Token system: high
Every color/space/radius/shadow/duration goes through tokens (`--accent`, `--surface`, `--ink`, `--line`, `--radius-sm/md/lg`, `--shadow-1/2`, `--motion-fast/base`). A hex value in component code is a finding (exceptions: the tokens file, a third-party logo, a `token-exception` comment).
- Tailwind v4: `@theme inline { --color-accent: var(--accent); }` to get `bg-accent`. **Every** token must be mapped (in home-hub `--weather` is missing).
- Tints: `color-mix(in srgb, var(--x) 12%, var(--surface))` instead of a new hex.
- STANDARDS §3: `design-tokens.json` (W3C format) for every tool; spacing 4/8/12/16/24/32; motion 150/250/400.

## D-4. Dark mode: medium
- Every token is defined in 3 places: `:root`, `@media (prefers-color-scheme: dark) :root:not([data-theme="light"])`, `:root[data-theme="dark"]` (home-hub R4). A new token goes into all three or does not go in.
- `color-scheme: light dark` on `html` (scrollbars, inputs, select on Windows); `<meta name="theme-color">` matching the background (one per theme).
- Dark is not inverted: layered surfaces (`--surface` < `--surface-2` < `--surface-3`, lighter the higher they sit), weaker shadows, a slightly brightened accent, text that is not pure white (`#EAEAEA`).
- Contrast is checked in **both** modes.

## D-5. Typography: medium
- A defined scale (12/14/16/18/20/24/30/36/48), not scattered `text-[13px]`/`text-[11px]`.
- Hierarchy from weight + size + color (`ink` / `ink-dim`), not from 4 different colors.
- line-height: 1.2 for headings, 1.5-1.7 for body (Hebrew toward the higher end); `max-w-prose`.
- `tabular-nums` for numbers in tables; `text-wrap: balance` for headings; use `…`, not `...`.

## D-6. Surfaces, shadows, borders: low
- Layered shadows (`0 1px 2px rgba(0,0,0,.04), 0 4px 12px rgba(0,0,0,.06)`), not a single `shadow-2xl`; a semi-transparent border and a shadow together.
- Child radius <= parent radius (a button inside a card: `rounded-lg` inside `rounded-xl`).
- On a colored background: border/shadow/text tinted toward the same hue, not gray.
- A card = an entity; not every section needs a card. A list = rows with `divide-y`, not 20 cards.

## D-7. Motion and micro-interactions: medium (§18.5)
- Hover on everything clickable (a subtle color/shadow change, not scale); active (`scale-[0.98]` allowed); a focus-visible ring.
- Success feedback after an action (a "Saved ✓" toast / a 300ms checkmark), not a silent state change.
- A skeleton that matches the final structure (not a lone spinner; the skeleton appears after 150-300ms and stays at least 300ms so it does not flicker).
- Loading inside a button: the spinner goes **beside** the text, and the text stays.
- Animate only `transform`/`opacity`; honor `prefers-reduced-motion`; correct `transform-origin`; cancelable.
- One orchestrated page-load sequence (brand mode) beats a fade-in on every element.

## D-8. Layout and rhythm: medium
- Grid spacing from one scale (`gap-4`/`gap-6`), not `mt-[13px]`.
- Optical alignment (icon + text balanced); every element aligned on purpose.
- A uniform page container (`.page-shell` in home-hub R1), not a different `max-w-* mx-auto px-*` on every page.
- Widgets in the same row have the same height (`h-full` + `auto-rows-fr`); lists inside a widget show at most 4 items + "See all (N)" (R6).
- No layout shift: dimensions on images, `min-h` for dynamic regions, a skeleton of the same size.

## D-9. Icons and logo: low
One icon set (lucide), a uniform size (16/20/24), uniform stroke; a real SVG logo (STANDARDS §3); favicon + `apple-touch-icon` + `theme-color`; Chrome extension: PNG 16/32/48/128.

## D-10. Desktop tools: STANDARDS §19/§21
A branded splash (brand gradient, dominant logo, >= 800ms, 8s timeout, `show:false` until ready); an installer in the same visual language; Fluent-ish (§15): toast 300-400px wide for 3-6s, click target >= 36px.

## D-11. "Remove one accessory": the finishing check
Before finishing a design sprint, look at the screen and remove one thing (a shadow, border, icon, gradient, badge) that does not help comprehension. If it looks better after removal, it was unnecessary.

## Design dimension score (see scoring.md)
1-3: scattered hex values, slop, no tokens, broken dark mode. 4-6: partial tokens, consistent but generic. 7-8: one system, a clear direction, full dark mode. 9-10: a distinctive identity recognizable without the logo + polish in every state.

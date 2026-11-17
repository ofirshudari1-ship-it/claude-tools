# Auditing Hebrew and RTL: verifiable rules

An English guide for auditing apps that support Hebrew and other right-to-left (RTL) languages. Hebrew is written right to left, so layout, icons, inputs and mixed Hebrew/Latin text must all be checked.

Sources: skills-il `hebrew-rtl-best-practices`, Crawlix RTL audit 2026, Microsoft Learn mirroring, the shared `STANDARDS.md` (§4/§11.6/§18.1/§20.3).
Each rule has an ID, a severity, how to check it, and Wrong/Right examples. Hebrew strings in examples are real UI text, each glossed in English.

## RTL-1. Document direction is set in HTML, not only in CSS: blocker
`<html lang="he" dir="rtl">`. Without it, screen readers, `:dir()` and logical properties do not work.
- Check: `grep -n 'dir="rtl"' src/app/layout.tsx` (Next) / `index.html` / `popup.html` (Chrome extension).
- Bilingual app: `dir` is derived from the locale at runtime, not hard-coded.

## RTL-2. Logical properties, not physical ones: high
| Physical (forbidden) | Logical (correct) | CSS |
|---|---|---|
| `ml-*` / `mr-*` | `ms-*` / `me-*` | `margin-inline-start/end` |
| `pl-*` / `pr-*` | `ps-*` / `pe-*` | `padding-inline-start/end` |
| `left-*` / `right-*` | `start-*` / `end-*` (Tailwind >= 4.3: `inset-s-*` / `inset-e-*`) | `inset-inline-start/end` |
| `text-left` / `text-right` | `text-start` / `text-end` | `text-align: start/end` |
| `rounded-l-*` / `rounded-r-*` | `rounded-s-*` / `rounded-e-*` | `border-start-start-radius` ... |
| `border-l` / `border-r` | `border-s` / `border-e` | `border-inline-start/end` |
| `float-left` / `float-right` | `float-start` / `float-end` | `float: inline-start` |
| `space-x-*` (without `rtl:space-x-reverse`) | `gap-*` in flex | `gap` |
| `scroll-ml-*` / `scroll-pl-*` | `scroll-ms-*` / `scroll-ps-*` | |

- Wrong: `<div className="pl-4 mr-2 text-right absolute left-0">`
- Right: `<div className="ps-4 me-2 text-start absolute start-0">`
- **Legitimate exception:** an element that must sit on a physical side regardless of language (a map, a canvas, a third-party logo). Mark it with a comment `// rtl-exception: <reason>`.
- **Automation:** `eslint-plugin-rtl-friendly` (ESLint 9 flat config) with `--fix` automatically fixes `ml/mr/pl/pr/left/right`:
  ```js
  import rtlFriendly from "eslint-plugin-rtl-friendly";
  export default [rtlFriendly.configs.recommended, { rules: { "rtl-friendly/no-physical-properties": "error" } }];
  ```

## RTL-3. Flex in RTL: do not use `row-reverse`: medium
`dir="rtl"` already reverses the flex order. `flex-row-reverse` on top of it is a double reversal (back to LTR).
- In `flex-col`, "right" is `items-start`; `items-end` puts content on the **left**.
- Exception: a bottom-sheet `items-end sm:items-center` (vertical axis) is not a finding.

## RTL-4. Numeric/Latin inputs stay LTR: high
`type="tel" | "email" | "url" | "password"`, OTP codes, card numbers, SKUs and URLs get `dir="ltr"` + `text-start`.
- Wrong: `<input type="tel" placeholder="050-1234567" />` (the digits jump around)
- Right: `<input type="tel" dir="ltr" inputMode="tel" autoComplete="tel" className="text-start" />`

## RTL-5. Free-text input uses `dir="auto"`: low
`<input type="text" dir="auto">`, `<textarea dir="auto">`, so an English word typed in a Hebrew form does not jump to the wrong side.
User-generated content (chat messages, notes): `dir="auto"` on the container, or `<bdi>`.

## RTL-6. Bidi inside Hebrew text: high
A phone number, email, code, signed amount or ISO date inside a Hebrew sentence needs `<span dir="ltr">...</span>` or `<bdi>`.
- Wrong: `<p>התקשרו: 050-321-4450</p>` ("Call us: 050-321-4450"; can render as 4450-321-050)
- Right: `<p>התקשרו: <span dir="ltr">050-321-4450</span></p>`
- CSS: `unicode-bidi: isolate; direction: ltr;` on an `.ltr-inline` class.
- **Canonical test string**: enter it in every field/heading and take a screenshot: `שלום John 050-1234567 ₪1,234` (Hebrew "Hello", then a Latin name, a phone number and an amount in shekels).

## RTL-7. Numbers, dates and currency via Intl: medium
```ts
new Intl.NumberFormat('he-IL', { style: 'currency', currency: 'ILS' }).format(1234)  // ‏1,234 ₪
new Intl.DateTimeFormat('he-IL', { dateStyle: 'medium' }).format(d)
new Intl.RelativeTimeFormat('he')
```
Do not use `toLocaleDateString()` without a locale, and do not hand-build `${d.getDate()}/${d.getMonth()+1}`. Use Latin digits (123), not Hebrew-letter numerals.
`font-variant-numeric: tabular-nums` in number tables.

## RTL-8. Icons: what to mirror and what not: medium
**Mirror (truly directional):** navigation arrows (next/previous/back/forward), expand/breadcrumb chevrons, send/reply arrows, drag handles, indentation, progress bars (fill right to left), undo/redo, carousel/pagination arrows.
**Do not mirror:** logos, ✓ / ✗, search (magnifier), settings, hamburger, bell, star/heart, clock/calendar, play/pause/fast-forward/rewind (a Microsoft convention), circular refresh, QR/barcode, credit cards, on/off toggles, vertical sort arrows.
- Tailwind: `<ChevronLeft className="rtl:-scale-x-100" />` or CSS `.icon-directional:dir(rtl){transform:scaleX(-1)}`.
- lucide: `ArrowLeft`/`ChevronLeft` in Hebrew code means "forward"; prefer `ArrowRight` + an `rtl:` variant, or a `<DirectionalIcon>` component.
- A global `transform: scaleX(-1)` on every `svg` is **forbidden**.

## RTL-9. What does not flip automatically: medium
`box-shadow` / `text-shadow` offsets, `linear-gradient(90deg...)`, `background-position`, `transform-origin`, and `translateX` in animations (drawer, slide-in, shimmer, carousel).
```css
.slide-in { --dir: -1; animation: slide 250ms ease-out; }
.slide-in:dir(rtl) { --dir: 1; }
@keyframes slide { from { transform: translateX(calc(var(--dir) * 100%)); } to { transform: none; } }
```
Tailwind: for `translate-x-full`, add `rtl:-translate-x-full`.

## RTL-10. Portalled UI (modal/dropdown/tooltip/toast): high
This is the most common RTL miss. Radix: `<DirectionProvider dir="rtl">` at the root. MUI: `createTheme({direction:'rtl'})` + `stylis-plugin-rtl`. Headless/custom: make sure `document.body` inherits `dir`. **Open every modal/dropdown during the live check.**

## RTL-11. Scrolling, tables, charts: medium
- The scrollbar sits on the left in RTL: `scrollbar-gutter: stable` prevents reflow.
- Tables: columns flip by themselves; numeric/code/date cells need `<td dir="ltr" className="text-end tabular-nums">`.
- SVG/charts have no logical properties, so use the charting library's `reversed`/`rtl` option (Recharts `reversed` on XAxis), not CSS.
- Grid with `grid-column: 2 / 4` uses physical indexes; prefer `grid-template-areas`.

## RTL-12. Hebrew typography: medium
- Font stack: `'Heebo','Assistant','Rubik','Noto Sans Hebrew',sans-serif` (Next: `next/font/google` with `subsets:['hebrew','latin']`).
- Hebrew type looks smaller than Latin at the same size, so body >= 16px, `line-height` 1.5-1.7 (§20.3: 120%-145%), **no** positive `letter-spacing` for Hebrew; `word-spacing: 0.05em` is allowed.
- Line length 70-80 characters (`max-w-prose` / `max-w-[65ch]`).
- Headings 30-50px by hierarchy. No ALL-CAPS (Hebrew has no case, but Latin eyebrow labels in `uppercase tracking-widest` are an anti-pattern anyway).
- `<html lang="he">` gives correct hyphenation/quotes; use Hebrew quotation marks („” or "") consistently.
- Unicode range for detecting Hebrew text in scripts: U+0590-U+05FF (Hebrew block), plus U+FB1D-U+FB4F (presentation forms).

## RTL-13. The "mirror test" (STANDARDS §18.1): acceptance check
Open every Hebrew screen and ask: "If I draw a vertical line down the middle and flip it like a mirror, does it look like the English version flipped, or is there one detail that was forgotten, or flipped by mistake?"
Quick checklist per route:
- [ ] header/nav/sidebar on the correct side (in RTL the sidebar is on the right, its inner border is `border-e`, not `border-l`)
- [ ] an icon before text sits to the right of the text
- [ ] the primary dialog button is on the side the OS puts it (Windows RTL: primary on the right)
- [ ] the badge/close button is in the correct corner (`end-2 top-2`)
- [ ] phone/email/numbers did not flip
- [ ] modal/dropdown/toast open on the correct side
- [ ] no horizontal scroll at 375px at the end edge

## RTL-14. Content i18n: low
`translate="no"` on brand names/code; `lang="en"` on an English passage inside Hebrew text (3.1.2); no hard-coded strings when an i18n system exists (STANDARDS §4).

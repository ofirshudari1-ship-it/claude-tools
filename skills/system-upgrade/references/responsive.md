# Responsiveness: mobile, tablet, desktop, wide screen

Sources: Vercel web-interface-guidelines, WCAG 2.2 (1.4.10 Reflow, 2.5.8 Target Size), home-hub `design-rules` R7, STANDARDS §14.2.

## RS-1. Required viewports: blocker if the viewport meta is missing
| Name | Width | What to check |
|---|---|---|
| mobile | 375 (+320 for Reflow) | bottom-nav, no horizontal scroll, 44px targets, 16px inputs, headings do not break mid-word |
| tablet | 768 | is there an intermediate layout, or is it a stretched mobile / squeezed desktop |
| desktop | 1440 | sidebar, 2-3 column grid, max-width for content |
| wide | 2560 (or zoom 50%) | content is anchored (RTL: to the right), not "floating" in the middle of a 27" screen |
`<meta name="viewport" content="width=device-width, initial-scale=1">` with no `maximum-scale=1` / `user-scalable=no` (blocking zoom is forbidden).

## RS-2. Graded breakpoints, not everything at `sm:`: medium
A pattern found in home-hub: `sm:` x412 vs `md:` x39, meaning there is no tablet mode. Rule: a layout that changes between mobile and desktop needs at least two breakpoints (`md:` for tablet, `lg:`/`xl:` for desktop). Grid: `grid-cols-1 md:grid-cols-2 xl:grid-cols-3`.

## RS-3. Screen height: `dvh`, not `vh`: medium
`h-screen`/`100vh` on mobile means the browser address bar covers the bottom. Use `h-dvh` / `min-h-dvh` (fallback: `min-height:100vh; min-height:100dvh`).

## RS-4. Bottom-nav and safe areas: medium
`fixed bottom-0` needs `pb-[env(safe-area-inset-bottom)]` (iPhone home indicator); Capacitor/PWA: `viewport-fit=cover`. Page content gets `pb-20` (or `padding-bottom: calc(nav-height + safe-area)`) so the last item is not hidden.

## RS-5. Hit targets: high on mobile
>= 44x44 CSS px on mobile, >= 24x24 on desktop (WCAG 2.5.8). A 16px icon inside a button needs at least `p-3`. Spacing between adjacent targets >= 8px. `touch-action: manipulation` on buttons (removes the double-tap zoom delay).
- Live check: `[...document.querySelectorAll('button,a,[role=button]')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&(r.width<44||r.height<44)})`.

## RS-6. Text and input on mobile: high
- `input`/`select`/`textarea` >= 16px (`text-base`), otherwise iOS Safari zooms in automatically.
- Body text >= 16px; secondary >= 14px (`text-sm`); `text-[10px]`/`text-[11px]` is unreadable on mobile, allowed only for a single badge/caption.
- One type scale (for example 12/14/16/18/20/24/30/36) instead of arbitrary values like `text-[13px]`.

## RS-7. Reflow (1.4.10): high
At 320px and 200% zoom there is no two-axis scrolling and no clipped content. Wide tables: `overflow-x-auto` on a wrapper **or** cards on mobile. `min-w-0` on flex children with long text; deliberate `break-words` / `truncate`.
- Live check: `document.documentElement.scrollWidth > window.innerWidth`.

## RS-8. No large fixed width: medium
`w-[600px]` / `min-w-[500px]` breaks mobile. Use `w-full max-w-[600px]`. Images: `max-w-full h-auto` + explicit `width/height` (prevents CLS).

## RS-9. Navigation per device: medium
Mobile: bottom-nav (<= 5 items) or a drawer; desktop: sidebar/top-nav. **The same items in the same order** on both (3.2.3 Consistent Navigation). Hover-only interactions need a tap alternative.

## RS-10. Wide screen: medium (home-hub R7)
Content at xl/2xl is anchored to the reading side (RTL: right) with a cap: `max-w-[800px] lg:max-w-[920px] xl:max-w-[1080px] 2xl:max-w-[1220px]`. Dashboard: a grid that fills the width, not a single narrow column in the middle.

## RS-11. Desktop tools (Electron/WPF/PyQt): STANDARDS §14.2
"Responsive" = DPI 100-200% (`PerMonitorV2` awareness), a defined minimum window size, works at 1366x768, remembers window position/size, never opens off-screen.

## RS-12. Chrome extension popup: STANDARDS §13
Popup <= 800x600; fixed width (360-420px) with `min-height`; long content goes to the options page, not a scrolling popup.

## Live-run checklist for every route
- [ ] 375: no overflow-x, bottom-nav does not hide content, targets >= 44, inputs >= 16px
- [ ] 768: a sensible intermediate layout (not one stretched column)
- [ ] 1440: sidebar + content, no text lines longer than 80 characters
- [ ] 2560: content is anchored and not lost in the middle
- [ ] light + dark at each of the above

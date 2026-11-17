# Browser pass — live-check protocol

Goal: evidence from the **running** app, not only from the code. Tools: `mcp__Claude_Browser__*` (preview_start / navigate / resize_window /
screenshot / read_page / javascript_tool / read_console_messages / computer) or `mcp__playwright__*` as an alternative.
Every result is saved to `.claude/upgrade/browser.json` and screenshots go to `.claude/upgrade/screenshots/<before|after>/`.

## 0. How to run
1. If `.claude/launch.json` exists **and the project is the session's cwd** → `preview_start {name}`. Otherwise (`preview_start {name}` resolves launch.json from the primary cwd, not from a path): run `npm run dev` in Bash with `run_in_background: true` from the project root, wait for "Ready", then `preview_start {url: "http://localhost:<port>/"}`.
   - **Screenshots to a file:** `computer screenshot` returns an image for viewing only. For `screenshots/before|after/*.png` use `mcp__playwright__browser_take_screenshot {filename}` (if available) or a Node+Playwright script (lesson learned by the agent: use the headless shell from the npx cache, and call `page.evaluate` with a function string). Never invent files that were not actually written.
2. An Electron app that wraps a website → run the website (production/dev URL). A Chrome extension → open `popup.html`/`options.html` directly (file:// or a dev server).
3. If the app requires login (OAuth only) and there is no way around it → mark dimensions 2/3/5/6/7 as `❓ (login blocks)` **and do not make anything up**. If public pages exist (login, landing, privacy, accessibility) — check those.
4. If the user is already logged in in the built-in browser — use that session, do not log out, and do not change real data (create an item named "test — delete me" and delete it at the end).

## 1. Route list
`src/app/**/page.tsx` (Next) / router / manifest. Up to 12 key routes: home, every main module, settings, login, one form, one public page. Record them in browser.json.

## 2. For every route × viewport × theme
viewports: `resize_window` mobile (375×812), tablet (768×1024), desktop (1440×900); wide 2560 only if the project has a wide-screen rule.
themes: `resize_window colorScheme: light|dark` (or the app's own toggle).
For every combination:
- `screenshot` → `screenshots/before/<route>__<w>__<theme>.png` (route name: `/` = `home`, `/family-chat` = `family-chat`).
- `read_console_messages onlyErrors` → the count plus the first messages.
- `javascript_tool` (run once per route@viewport, returns JSON):
```js
(() => {
  const vw = innerWidth, mobile = vw < 768;
  const els = [...document.querySelectorAll('button,a[href],[role=button],input,select,textarea')].filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; });
  const min = mobile ? 44 : 24;
  const small = els.filter(e => { const r = e.getBoundingClientRect(); return r.width < min || r.height < min; }).map(e => ({ tag: e.tagName, text: (e.innerText || e.getAttribute('aria-label') || '').slice(0, 30), w: Math.round(e.getBoundingClientRect().width), h: Math.round(e.getBoundingClientRect().height) }));
  const inputs = [...document.querySelectorAll('input,select,textarea')];
  const smallFont = inputs.filter(i => parseFloat(getComputedStyle(i).fontSize) < 16).length;
  const ltrInputs = inputs.filter(i => ['tel', 'email', 'url', 'password'].includes(i.type) && getComputedStyle(i).direction !== 'ltr').length;
  const noLabel = inputs.filter(i => i.type !== 'hidden' && !i.labels?.length && !i.getAttribute('aria-label') && !i.getAttribute('aria-labelledby')).length;
  const iconBtns = [...document.querySelectorAll('button')].filter(b => !b.innerText.trim() && !b.getAttribute('aria-label') && !b.getAttribute('aria-labelledby')).length;
  const h1 = document.querySelectorAll('h1').length;
  return {
    route: location.pathname, vw, dir: document.documentElement.dir, lang: document.documentElement.lang,
    overflowX: document.documentElement.scrollWidth > vw,
    smallTargets: small.length, smallTargetsSample: small.slice(0, 8),
    inputsUnder16px: smallFont, ltrInputsWrongDir: ltrInputs, inputsNoLabel: noLabel, iconButtonsNoLabel: iconBtns,
    h1Count: h1, hasMain: !!document.querySelector('main'), hasSkipLink: !!document.querySelector('a[href="#main"],a[href^="#content"]'),
    title: document.title,
  };
})()
```
- **axe** (once per route@desktop+mobile, light+dark): load from `node_modules/axe-core/axe.min.js` (inject its text) or from `https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.2/axe.min.js`, then run:
```js
await axe.run(document, { runOnly: ['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa'] }).then(r => ({ violations: r.violations.map(v => ({ id: v.id, impact: v.impact, nodes: v.nodes.length, sample: v.nodes[0]?.target?.[0] })) }))
```

## 3. RTL test (once per form / main search field)
- Type `שלום John 050-1234567 ₪1,234` into the field (mixed Hebrew + Latin + phone number + shekel amount; keep the Hebrew word as is, it is the test input) → screenshot → verify that the numbers did not get reversed and that the text is right-aligned.
- **Mirror test** for every route@1440: go through the checklist in `rtl-hebrew.md` RTL-13 and record each ✗ with its location.
- Open **every** modal / dropdown / toast / bottom-sheet you find (click "Add", "…", settings) → screenshot → is it on the correct side? Does Esc close it? Does focus return?

## 4. Keyboard (main route + one form + one modal)
Press `computer key Tab` ×15 starting from body; after each Tab run `javascript_tool` → `document.activeElement` (tag, text, `getComputedStyle(el).outlineStyle`, `getBoundingClientRect()` against the sticky header / bottom-nav rect). Record: is the focus ring visible? Is the order logical? Is the element hidden behind something? Is there a keyboard trap? Does Esc close the modal?

## 5. States
- empty: if the list can be filtered down to nothing (search "zzzz") → screenshot.
- loading: network throttling is not available → check the skeleton in the code; in the browser: reload and take a screenshot at 200ms if possible.
- error: going offline cannot be faked (`navigator.onLine` is read-only) → check in the code; in the browser: submit an empty form → are the errors next to the fields? Where does focus go?

## 6. browser.json
```json
{ "ranAt": "...", "how": "preview_start home-hub-dev", "routes": [
  { "route": "/", "checks": { "375-light": {...js result..., "consoleErrors": 0, "axe": [...] }, "768-light": {...}, "1440-light": {...}, "375-dark": {...}, "1440-dark": {...} },
    "mirrorTest": ["badge close at left-2 (should be end-2)"], "modals": [{ "name": "add-task", "rtlOk": true, "escCloses": true }],
    "keyboard": { "focusRingVisible": false, "obscuredBy": "bottom-nav", "trap": false } } ],
  "totals": { "overflowX": 2, "smallTargets": 14, "consoleErrors": 3, "axeViolations": 21 } }
```

## 7. After
Exactly the same protocol, on the same routes and the same viewports → `screenshots/after/` + `browser-after.json`. The comparison (before/after totals) goes into the final report.

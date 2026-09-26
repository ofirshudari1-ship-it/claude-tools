# Browser pass — פרוטוקול הבדיקה החיה

מטרה: ראיות מהאפליקציה **הרצה**, לא רק מהקוד. הכלים: `mcp__Claude_Browser__*` (preview_start / navigate / resize_window /
screenshot / read_page / javascript_tool / read_console_messages / computer) או `mcp__playwright__*` כחלופה.
כל תוצאה נשמרת ב-`.claude/upgrade/browser.json` וצילומים ב-`.claude/upgrade/screenshots/<before|after>/`.

## 0. איך מריצים
1. `.claude/launch.json` קיים **והפרויקט הוא ה-cwd של ה-session** → `preview_start {name}`. אחרת (`preview_start {name}` פותר launch.json מה-cwd הראשי, לא מ-path): `npm run dev` ב-Bash עם `run_in_background: true` מתוך שורש הפרויקט, המתן ל-"Ready", ואז `preview_start {url: "http://localhost:<port>/"}`.
   - **צילומים לקובץ:** `computer screenshot` מחזיר תמונה לעיניים בלבד. ל-`screenshots/before|after/*.png` השתמש ב-`mcp__playwright__browser_take_screenshot {filename}` (אם זמין) או בסקריפט Node+Playwright (הלקח בזיכרון הסוכן: headless-shell מה-npx cache, `page.evaluate` עם מחרוזת פונקציה). לא ממציאים קבצים שלא נכתבו.
2. Electron שעוטף אתר → להריץ את האתר (URL של production/dev). Chrome extension → `popup.html`/`options.html` ישירות (file:// או dev server).
3. דורש login (OAuth בלבד) ואין דרך לעקוף → סמן ממדים 2/3/5/6/7 כ-`❓ (login חוסם)` **ואל תמציא**. אם יש דף public (login, landing, privacy, accessibility) — בדוק אותם.
4. אם המשתמש מחובר בדפדפן הפנימי — להשתמש בזה, לא להתנתק, לא לשנות נתונים אמיתיים (ליצור פריט "בדיקה — למחוק" ולמחוק בסוף).

## 1. רשימת routes
`src/app/**/page.tsx` (Next) / router / manifest. עד 12 routes מרכזיים: בית, כל מודול ראשי, הגדרות, login, טופס אחד, עמוד public אחד. לתעד ב-browser.json.

## 2. לכל route × viewport × theme
viewports: `resize_window` mobile (375×812), tablet (768×1024), desktop (1440×900); wide 2560 רק אם יש כלל wide-screen.
themes: `resize_window colorScheme: light|dark` (או toggle של האפליקציה).
לכל שילוב:
- `screenshot` → `screenshots/before/<route>__<w>__<theme>.png` (שם route: `/` = `home`, `/family-chat` = `family-chat`).
- `read_console_messages onlyErrors` → מספר + הודעות ראשונות.
- `javascript_tool` (רץ פעם אחת לכל route@viewport, מחזיר JSON):
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
- **axe** (פעם לכל route@desktop+mobile, light+dark): טעינה מ-`node_modules/axe-core/axe.min.js` (להזריק את הטקסט) או `https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.2/axe.min.js`, ואז:
```js
await axe.run(document, { runOnly: ['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa'] }).then(r => ({ violations: r.violations.map(v => ({ id: v.id, impact: v.impact, nodes: v.nodes.length, sample: v.nodes[0]?.target?.[0] })) }))
```

## 3. מבחן RTL (פעם אחת לכל טופס/שדה חיפוש ראשי)
- להקליד `שלום John 050-1234567 ₪1,234` בשדה → screenshot → לוודא שהמספר לא התהפך ושהטקסט מיושר לימין.
- **מבחן המראה** לכל route@1440: לעבור על הצ'קליסט ב-`rtl-hebrew.md` RTL-13 ולרשום ✗ עם מיקום.
- לפתוח **כל** modal / dropdown / toast / bottom-sheet שנמצא (לחיצה על "הוסף", "…", הגדרות) → screenshot → צד נכון? Esc סוגר? פוקוס חוזר?

## 4. מקלדת (route ראשי + טופס אחד + modal אחד)
`computer key Tab` ×15 מ-body; אחרי כל Tab: `javascript_tool` → `document.activeElement` (tag, text, `getComputedStyle(el).outlineStyle`, `getBoundingClientRect()` מול sticky header/bottom-nav rect). לרשום: focus ring גלוי? סדר לוגי? מוסתר? keyboard trap? Esc סוגר modal?

## 5. States
- empty: אם אפשר לפלטר לרשימה ריקה (חיפוש "zzzz") → screenshot.
- loading: throttling לא זמין → לבדוק בקוד skeleton; בדפדפן: reload ו-screenshot ב-200ms אם אפשר.
- error: לנתק רשת (`navigator.onLine` לא ניתן לזייף) → לבדוק בקוד; בדפדפן: submit טופס ריק → שגיאות ליד השדות? פוקוס?

## 6. browser.json
```json
{ "ranAt": "...", "how": "preview_start home-hub-dev", "routes": [
  { "route": "/", "checks": { "375-light": {...js result..., "consoleErrors": 0, "axe": [...] }, "768-light": {...}, "1440-light": {...}, "375-dark": {...}, "1440-dark": {...} },
    "mirrorTest": ["badge close at left-2 (should be end-2)"], "modals": [{ "name": "add-task", "rtlOk": true, "escCloses": true }],
    "keyboard": { "focusRingVisible": false, "obscuredBy": "bottom-nav", "trap": false } } ],
  "totals": { "overflowX": 2, "smallTargets": 14, "consoleErrors": 3, "axeViolations": 21 } }
```

## 7. after
אותו פרוטוקול בדיוק, לאותם routes ואותם viewports → `screenshots/after/` + `browser-after.json`. ההשוואה (totals לפני/אחרי) נכנסת לדוח הסיום.

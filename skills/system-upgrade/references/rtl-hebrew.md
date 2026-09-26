# RTL ועברית — כללים ניתנים לבדיקה

מקורות: skills-il `hebrew-rtl-best-practices`, Crawlix RTL audit 2026, Microsoft Learn mirroring, `_AUDIT/STANDARDS.md` §4/§11.6/§18.1/§20.3.
כל כלל: מזהה, severity, איך בודקים, Wrong/Right.

## RTL-1. כיוון המסמך מוגדר ב-HTML, לא רק ב-CSS — blocker
`<html lang="he" dir="rtl">`. בלי זה קוראי מסך, `:dir()`, ו-logical properties לא עובדים.
- בדיקה: `grep -n 'dir="rtl"' src/app/layout.tsx` (Next) / `index.html` / `popup.html` (Chrome ext).
- אפליקציה דו-לשונית: `dir` נגזר מה-locale בזמן ריצה, לא קבוע.

## RTL-2. מאפיינים לוגיים, לא פיזיים — high
| פיזי (אסור) | לוגי (נכון) | CSS |
|---|---|---|
| `ml-*` / `mr-*` | `ms-*` / `me-*` | `margin-inline-start/end` |
| `pl-*` / `pr-*` | `ps-*` / `pe-*` | `padding-inline-start/end` |
| `left-*` / `right-*` | `start-*` / `end-*` (Tailwind ≥4.3: `inset-s-*` / `inset-e-*`) | `inset-inline-start/end` |
| `text-left` / `text-right` | `text-start` / `text-end` | `text-align: start/end` |
| `rounded-l-*` / `rounded-r-*` | `rounded-s-*` / `rounded-e-*` | `border-start-start-radius` … |
| `border-l` / `border-r` | `border-s` / `border-e` | `border-inline-start/end` |
| `float-left` / `float-right` | `float-start` / `float-end` | `float: inline-start` |
| `space-x-*` (בלי `rtl:space-x-reverse`) | `gap-*` ב-flex | `gap` |
| `scroll-ml-*` / `scroll-pl-*` | `scroll-ms-*` / `scroll-ps-*` | |

- Wrong: `<div className="pl-4 mr-2 text-right absolute left-0">`
- Right: `<div className="ps-4 me-2 text-start absolute start-0">`
- **חריג לגיטימי:** אלמנט שחייב להיות בצד פיזי בלי קשר לשפה (מפה, canvas, לוגו של צד שלישי) — מסמנים בקומנט `// rtl-exception: <סיבה>`.
- **אוטומציה:** `eslint-plugin-rtl-friendly` (ESLint 9 flat config) עם `--fix` מתקן `ml/mr/pl/pr/left/right` אוטומטית:
  ```js
  import rtlFriendly from "eslint-plugin-rtl-friendly";
  export default [rtlFriendly.configs.recommended, { rules: { "rtl-friendly/no-physical-properties": "error" } }];
  ```

## RTL-3. flex ב-RTL: לא `row-reverse` — medium
`dir="rtl"` כבר הופך את סדר ה-flex. `flex-row-reverse` מעליו = היפוך כפול (חוזר ל-LTR).
- ב-`flex-col`, "ימין" הוא `items-start`; `items-end` שם תוכן **בשמאל**.
- חריג: bottom-sheet `items-end sm:items-center` (ציר אנכי) — לא ממצא.

## RTL-4. קלט מספרי/לטיני נשאר LTR — high
`type="tel" | "email" | "url" | "password"`, קודי OTP, מספר כרטיס, SKU, כתובת URL → `dir="ltr"` + `text-start`.
- Wrong: `<input type="tel" placeholder="050-1234567" />` (הספרות קופצות)
- Right: `<input type="tel" dir="ltr" inputMode="tel" autoComplete="tel" className="text-start" />`

## RTL-5. קלט חופשי → `dir="auto"` — low
`<input type="text" dir="auto">`, `<textarea dir="auto">` — כך מילה באנגלית בטופס עברי לא קופצת לצד הלא נכון.
תוכן שנוצר ע"י משתמש (הודעות צ'אט, הערות) — `dir="auto"` על המכולה או `<bdi>`.

## RTL-6. Bidi בתוך טקסט עברי — high
טלפון, אימייל, קוד, סכום עם סימן, תאריך ISO בתוך משפט עברי → `<span dir="ltr">…</span>` או `<bdi>`.
- Wrong: `<p>התקשרו: 050-321-4450</p>` (יכול להתרנדר 4450-321-050)
- Right: `<p>התקשרו: <span dir="ltr">050-321-4450</span></p>`
- CSS: `unicode-bidi: isolate; direction: ltr;` לקלאס `.ltr-inline`.
- **מחרוזת בדיקה קנונית** — להכניס בכל שדה/כותרת: `שלום John 050-1234567 ₪1,234` ולצלם.

## RTL-7. מספרים, תאריכים, מטבע דרך Intl — medium
```ts
new Intl.NumberFormat('he-IL', { style: 'currency', currency: 'ILS' }).format(1234)  // ‏1,234 ₪
new Intl.DateTimeFormat('he-IL', { dateStyle: 'medium' }).format(d)
new Intl.RelativeTimeFormat('he')
```
לא `toLocaleDateString()` בלי locale, לא `${d.getDate()}/${d.getMonth()+1}` ידני. ספרות לטיניות (123), לא עבריות.
`font-variant-numeric: tabular-nums` בטבלאות מספרים.

## RTL-8. אייקונים — מה כן ומה לא למראר — medium
**כן (כיווני באמת):** חצי ניווט (הבא/הקודם/חזור/קדימה), chevron של expand/breadcrumb, חץ שליחה/reply, ידית גרירה, indentation, progress bar (מתמלא ימין→שמאל), undo/redo, חצי carousel/pagination.
**לא:** לוגו, ✓ / ✗, חיפוש (זכוכית מגדלת), הגדרות, המבורגר, פעמון, כוכב/לב, שעון/לוח שנה, play/pause/FF/rewind (מוסכמה של Microsoft), refresh מעגלי, QR/barcode, כרטיסי אשראי, on/off toggle, חצי מיון אנכיים.
- Tailwind: `<ChevronLeft className="rtl:-scale-x-100" />` או CSS `.icon-directional:dir(rtl){transform:scaleX(-1)}`.
- lucide: `ArrowLeft`/`ChevronLeft` בקוד עברי = "קדימה" — עדיף `ArrowRight` + `rtl:` variant, או קומפוננט `<DirectionalIcon>`.
- **אסור** `transform: scaleX(-1)` גלובלי על כל `svg`.

## RTL-9. מה לא הופך אוטומטית — medium
`box-shadow` / `text-shadow` offset, `linear-gradient(90deg…)`, `background-position`, `transform-origin`, `translateX` באנימציות (drawer, slide-in, shimmer, carousel).
```css
.slide-in { --dir: -1; animation: slide 250ms ease-out; }
.slide-in:dir(rtl) { --dir: 1; }
@keyframes slide { from { transform: translateX(calc(var(--dir) * 100%)); } to { transform: none; } }
```
Tailwind: `translate-x-full` → להוסיף `rtl:-translate-x-full`.

## RTL-10. Portalled UI (modal/dropdown/tooltip/toast) — high
זה ה-RTL miss הנפוץ ביותר. Radix: `<DirectionProvider dir="rtl">` בשורש. MUI: `createTheme({direction:'rtl'})` + `stylis-plugin-rtl`. Headless/custom: לוודא ש-`document.body` יורש `dir`. **לפתוח כל modal/dropdown בבדיקה החיה**.

## RTL-11. גלילה, טבלאות, גרפים — medium
- פס גלילה בצד שמאל ב-RTL: `scrollbar-gutter: stable` מונע reflow.
- טבלאות: עמודות מתהפכות לבד; תאים מספריים/קוד/תאריך → `<td dir="ltr" className="text-end tabular-nums">`.
- SVG/גרפים אין להם logical properties → להשתמש ב-option `reversed`/`rtl` של ספריית הגרפים (Recharts `reversed` על XAxis), לא ב-CSS.
- Grid עם `grid-column: 2 / 4` = אינדקסים פיזיים — עדיף `grid-template-areas`.

## RTL-12. טיפוגרפיה עברית — medium
- font stack: `'Heebo','Assistant','Rubik','Noto Sans Hebrew',sans-serif` (Next: `next/font/google` עם `subsets:['hebrew','latin']`).
- גופן עברי נראה קטן יותר מלטיני באותו size → body ≥ 16px, `line-height` 1.5–1.7 (§20.3: 120%-145%), **בלי** `letter-spacing` חיובי לעברית, `word-spacing: 0.05em` מותר.
- אורך שורה 70–80 תווים (`max-w-prose` / `max-w-[65ch]`).
- כותרות 30–50px לפי היררכיה; לא ALL-CAPS (אין בעברית — אבל eyebrows לטיניים ב-`uppercase tracking-widest` הם anti-pattern בכל מקרה).
- `<html>` עם `lang="he"` נותן hyphenation/quotes נכונים; מרכאות עבריות „” או "" עקביות.

## RTL-13. "מבחן המראה" (STANDARDS §18.1) — בדיקת קבלה
לפתוח כל מסך בעברית ולשאול: "אם אצייר קו אנכי באמצע ואהפוך כמו מראה — זה נראה כמו גרסה אנגלית הפוכה, או שיש פרט אחד ששכחו להפוך / שהפכו בטעות?"
צ'קליסט מהיר לכל route:
- [ ] header/nav/sidebar בצד הנכון (sidebar ב-RTL מימין, border בצד הפנימי = `border-e` לא `border-l`)
- [ ] אייקון לפני טקסט = מימין לטקסט
- [ ] כפתור ראשי בדיאלוג בצד שה-OS שם אותו (Windows RTL: ראשי מימין)
- [ ] badge/סגירה בפינה הנכונה (`end-2 top-2`)
- [ ] טלפון/אימייל/מספרים לא התהפכו
- [ ] modal/dropdown/toast נפתחים בצד הנכון
- [ ] אין גלילה אופקית ב-375px בקצה ה-end

## RTL-14. i18n של תוכן — low
`translate="no"` על שמות מותג/קוד; `lang="en"` על קטע באנגלית בתוך עברית (3.1.2); בלי מחרוזות קשיחות כשיש מערכת i18n (STANDARDS §4).

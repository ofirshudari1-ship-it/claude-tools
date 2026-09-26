# נגישות — WCAG 2.2 AA + ת"י 5568

מקורות: WCAG 2.2 AA audit checklist 2026 (digitalapplied), WebAIM Million 2026, ת"י 5568 (= WCAG 2.0/2.1 AA, חובה חוקית בישראל לפי תקנה 35), STANDARDS §14.3/§18.2/§20.1-20.2, Vercel guidelines.

## למה זה לא "nice to have"
עסק ישראלי עם אתר/אפליקציה ללא נגישות חשוף לתביעה. ת"י 5568 דורש גם **עמוד הצהרת נגישות** עם שם רכז נגישות, פרטי קשר ותאריך עדכון. axe/Lighthouse תופסים ~57% מהבעיות לפי נפח, אבל רק ~30% מהקריטריונים — **ממצא ידני שווה יותר מציון**.

## 5 המעברים (בסדר הזה)
1. **אוטומטי** — axe-core על כל route (mobile+desktop, light+dark). תופס: ניגודיות, alt חסר, label חסר, כפתור/קישור ריק, `lang` חסר, ARIA לא תקין, heading order.
2. **מקלדת** — Tab דרך כל המסך: כל אינטראקטיבי נגיש, focus ring **גלוי**, סדר לוגי (סדר קריאה RTL), Enter/Space מפעילים, Esc סוגר, אין keyboard trap, פוקוס לא מוסתר תחת sticky header / bottom-nav (2.4.11).
3. **קורא מסך** (NVDA / Narrator / VoiceOver) — שם, תפקיד, מצב מוכרזים; `aria-live` לטוסטים/עדכוני async (4.1.3); ARIA תואם התנהגות.
4. **Reflow + Zoom** — 320px, zoom 200%, text-spacing bookmarklet: אין חיתוך, אין גלילה דו-צירית, אין חפיפה.
5. **קריטריוני 2.2 החדשים** — ראה A-9.

## A-1. ניגודיות — high (הכשל הנפוץ ביותר: 84% מהאתרים)
- טקסט רגיל ≥ 4.5:1; טקסט גדול (≥18pt או ≥14pt bold) ≥ 3:1; **רכיבי UI לא-טקסטואליים** (border של input, focus ring, אייקון לחיץ) ≥ 3:1 מול הסביבה (1.4.11).
- לבדוק **בנפרד** light ו-dark — פלטה שעובדת באחד לא בהכרח בשני (§20.1).
- `text-ink-dim` / `text-gray-400` על רקע בהיר = בדרך כלל נכשל. placeholder גם צריך 4.5:1.
- כלי: axe מודד; WebAIM Contrast Checker לכל accent חדש לפני שנכנס לקוד; APCA כמדד משני.

## A-2. תמונות ואייקונים — high (53%)
- `<img alt="תיאור">`; דקורטיבי → `alt=""`; `<svg aria-hidden="true">` בתוך כפתור עם טקסט.
- **כפתור-אייקון בלי טקסט** → `aria-label="…"` (בעברית). lucide icons הם `aria-hidden` כברירת מחדל — הכפתור עצמו חייב label.
- אייקון שמעביר משמעות לבד (סטטוס) → טקסט נלווה או `aria-label`.

## A-3. טפסים — high (51%)
- כל שדה עם `<label htmlFor>` (או `aria-label`/`aria-labelledby`); placeholder ≠ label.
- `autocomplete` (1.3.5): `name`, `email`, `tel`, `street-address`, `cc-number`, `one-time-code`.
- `type`/`inputmode` נכונים: `tel`, `email`, `numeric`, `decimal`, `url`.
- שגיאה: `aria-invalid="true"` + `aria-describedby` להודעה, ההודעה **ליד השדה**, פוקוס לשגיאה הראשונה ב-submit, ניסוח שאומר מה לתקן (3.3.3).
- לא לחסום הקלדה; לא לנעול submit לפני ניסיון; לא `alert()`.
- `spellCheck={false}` לאימייל/קוד/שם משתמש.

## A-4. סמנטיקה — high
- ניווט = `<a href>` / `<Link>` (Cmd+click, middle-click, קורא מסך); פעולה = `<button type="button">`. **לא** `<div onClick>` / `<span onClick>` / `<li onClick>`.
- landmarks: `<header>`, `<nav aria-label="ראשי">`, `<main>`, `<footer>`; heading hierarchy h1→h2→h3 בלי דילוג; `h1` אחד לעמוד.
- Skip link ("דלג לתוכן") ראשון ב-DOM.
- `<button>` ריק / `<a>` ריק (46% / 31%) — תמיד טקסט או `aria-label`.
- רשימות = `<ul>/<ol>`; טבלאות נתונים = `<table>` עם `<th scope>`.
- ARIA רק כשאין אלמנט native (`role="dialog" aria-modal="true" aria-labelledby`).

## A-5. פוקוס — high
- `outline-none` / `focus:outline-none` **אסור** בלי `focus-visible:ring-2 focus-visible:ring-offset-2` (2.4.7 + 2.4.13 Focus Appearance: ≥ 2px, ניגודיות 3:1).
- Modal: focus trap, פוקוס נכנס לדיאלוג בפתיחה וחוזר לטריגר בסגירה; `inert` על הרקע.
- Dropdown/menu: חצים לניווט, Esc סוגר, Home/End.
- אחרי ניווט SPA: פוקוס ל-`<main>` או ל-h1, ו-`document.title` מתעדכן.

## A-6. סטטוס לא בצבע בלבד — medium (1.4.1)
אדום=שגיאה / ירוק=הצלחה חייב גם אייקון או טקסט. גרפים: פלטה color-blind-safe + labels/patterns.

## A-7. תנועה — medium
`@media (prefers-reduced-motion: reduce)` מבטל/מקצר אנימציות; `transition: all` אסור (מפורש: `transition-colors`, `transition-transform`); אין autoplay > 5s בלי pause; אנימציה 150–250ms (§18.5). אין parallax/blink.

## A-8. עדכונים דינמיים — medium
Toast/סטטוס = `role="status"` / `aria-live="polite"`; שגיאה קריטית = `role="alert"`; מונה עגלה/התראות מתעדכן → `aria-live`. Loading: `aria-busy="true"` על האזור.

## A-9. WCAG 2.2 — 9 הקריטריונים החדשים
| # | קריטריון | רמה | בדיקה |
|---|---|---|---|
| 2.4.11 | Focus Not Obscured (Minimum) | AA | Tab ליד sticky header / bottom-nav / cookie banner — האלמנט הממוקד לא מוסתר לגמרי |
| 2.4.12 | Focus Not Obscured (Enhanced) | AAA | (רשות) לא מוסתר בכלל |
| 2.4.13 | Focus Appearance | AAA→ מומלץ | ring ≥ 2px, 3:1 |
| 2.5.7 | Dragging Movements | AA | כל drag (kanban, slider, reorder) — יש חלופת click/tap/מקלדת |
| 2.5.8 | Target Size (Minimum) | AA | ≥ 24×24 או רווח מספיק; במובייל שואפים ל-44 |
| 3.2.6 | Consistent Help | A | עזרה/צור-קשר באותו מקום בכל העמודים |
| 3.3.7 | Redundant Entry | A | טופס רב-שלבי לא מבקש שוב מידע שכבר הוזן |
| 3.3.8 | Accessible Authentication (Minimum) | AA | login בלי מבחן קוגניטיבי; password manager / paste עובדים; OTP עם `autocomplete="one-time-code"` |
| 3.3.9 | Accessible Authentication (Enhanced) | AAA | (רשות) |

## A-10. ת"י 5568 — ספציפי לישראל
- [ ] עמוד `/accessibility` (הצהרת נגישות) קיים, מקושר מה-footer בכל עמוד, כולל: רמת התאימות, רכז נגישות (שם+טלפון+מייל), תאריך עדכון, התאמות שבוצעו, דרך לדווח על בעיה.
- [ ] `lang="he"` + `dir="rtl"`; כתוביות לווידאו; מסמכים (PDF) נגישים או חלופה.
- [ ] ווידג'ט נגישות **לא מחליף** נגישות אמיתית בקוד — הוא תוספת בלבד.

## A-11. Desktop (WPF/WinForms/Electron) — STANDARDS §18.2/§20.2
- פקדים custom-drawn → `AutomationProperties.Name` (WPF) / `AccessibleName` (WinForms) כדי ש-Narrator ידע מה זה.
- Windows High Contrast: לבדוק `SystemParameters.HighContrast` / Electron `nativeTheme.shouldUseHighContrastColors` ולכבד `SystemColors`, לא לדרוס בגרדיאנט מותג.
- Tab order = סדר קריאה חזותי, לא סדר יצירה.

## פורמט דיווח
`file:line - [a11y] <קריטריון> — <ממצא> → <תיקון>` ; ממצא מהדפדפן: `route@viewport - [a11y] …` + צילום.

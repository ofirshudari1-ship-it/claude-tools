# UX — זרימות, states, טפסים, ניווט, copy, onboarding

מקורות: Vercel guidelines (forms/navigation/content/tooltips), Nielsen heuristics, `impeccable` harden/onboard/clarify, STANDARDS §5/§14.4/§16/§18.3.

## U-1. ארבעת ה-states של כל רשימה/טופס/widget — high
| state | דרישה |
|---|---|
| **empty** | לא "אין נתונים" ריק: הסבר קצר + CTA ראשי ("הוסף משימה ראשונה") + איור/אייקון קל; דאטה דמו ריאליסטית באונבורדינג (לא lorem/example.txt) |
| **loading** | skeleton במבנה הסופי (150–300ms delay, ≥ 300ms visible), לא spinner לבד; `aria-busy` |
| **error** | מה קרה + מה לעשות + כפתור "נסה שוב"; לא stack trace; לא `alert()` |
| **success** | אישור מיידי (toast/checkmark), ואז חזרה למצב עבודה |
+ **sparse** (פריט אחד) ו-**dense** (200 פריטים: virtualize / pagination / "ראה הכל") — לבדוק שניהם. תוכן ארוך מאוד (שם של 80 תווים) לא שובר layout.

## U-2. טפסים — high
- שדות מינימום; שדות אופציונליים מסומנים (לא "חובה" בכוכבית על 8 מתוך 9).
- Enter שולח בשדה יחיד; Ctrl/Cmd+Enter ב-textarea.
- submit **לא** disabled לפני ניסיון — לוחצים, מקבלים שגיאות ליד השדות, פוקוס לראשונה. במהלך שליחה: disabled + spinner + הטקסט נשאר.
- לא לחסום הקלדה (מסכות) — לאפשר כל קלט ולוודא; trim רווחים.
- `autocomplete`/`name`/`type`/`inputmode`; placeholder = דוגמה לפורמט ("050-1234567"), לא label.
- שינויים לא שמורים → אזהרה לפני ניווט (`beforeunload` / router guard).
- טופס רב-שלבי: progress, "חזור" שומר ערכים, לא לבקש שוב (3.3.7).
- מחיקה/פעולה הרסנית: confirm **או** Undo (עדיף Undo-toast 5s).

## U-3. ניווט ומצב — high
- ניווט = `<a href>` (Cmd+click, back, share). `router.push` ב-`<div onClick>` = ממצא.
- **URL = state**: טאב פעיל, פילטר, חיפוש, עמוד, פאנל פתוח → query params (`?tab=…&q=…`). רענון/Back/שיתוף משחזרים.
- Back/Forward מחזירים scroll; `scroll-margin-top` לכותרות עם anchor.
- Active state ברור בניווט (`aria-current="page"`); breadcrumbs בעומק > 2; כל עמוד חשוב ≤ 3 קליקים מהבית.
- ניווט זהה בכל העמודים ובאותו סדר (מובייל ודסקטופ).
- `document.title` משקף את ההקשר ("משימות · HOMEY").

## U-4. פעולה ראשית אחת לכל מסך — medium (STANDARDS §3)
כפתור primary אחד (accent מלא), secondary outline, tertiary text. אם יש 3 כפתורי accent במסך — אין היררכיה. Command bar / FAB במובייל לפעולה השכיחה.

## U-5. Optimistic UI ומהירות נתפסת — medium
פעולות שכיחות (toggle, סימון משימה, לייק) מתעדכנות מיד ומתגלגלות אחורה בכישלון עם הודעה. יעד: POST/PATCH < 500ms נתפס. Skeleton במקום מסך לבן; `content-visibility: auto` / virtualization לרשימות > 100.

## U-6. Copy — medium (בעברית: דרך copywriting-agent / hebrew-copywriting)
- פועל + מושא בכפתור: "שמור שינויים", לא "המשך"; אותו פועל בכל הזרימה ("פרסם" → "פורסם").
- שגיאה = מה קרה + מה לעשות ("הטלפון צריך 10 ספרות, למשל 0501234567"), לא "קלט לא תקין".
- אפשרות שפותחת המשך → "שנה שם…"; מצב טעינה → "שומר…"; `…` תו אחד.
- מספרים: "8 משימות" לא "שמונה"; יחידות עם רווח `10 MB`; `&nbsp;` בין מספר ליחידה.
- טון: גוף שני, פעיל, קצר, אנושי; אין "אופס!"/"משהו השתבש" בלי פרטים.
- inline help > tooltip; tooltips רק לאייקונים.
- טרמינולוגיה עקבית (GLOSSARY — §20.4: "הגדרות" לא "אפשרויות" באותו הקשר).

## U-7. Onboarding ו-TTFV — medium (§18.3)
- מדד: **זמן עד ערך ראשון < 60 שניות** — לא מספר מסכים. ~30% מצעדי onboarding מיותרים.
- "דלג" גלוי בכל שלב; progressive disclosure (tip בפעם הראשונה שפיצ'ר רלוונטי), לא dump.
- צ'קליסט "השלמת הגדרה" (3–4 פריטים) במקום אשף חד-פעמי.
- Empty state של המודול הראשון = ה-onboarding האמיתי.

## U-8. Modals, drawers, toasts — medium
- modal רק לפעולה שדורשת החלטה; עריכה ארוכה → עמוד/drawer.
- toast: `aria-live`, 3–6s, פעולה אחת (Undo), לא ערימה של 5.
- כל overlay: Esc סוגר, קליק בחוץ סוגר (חוץ מטפסים עם שינויים), focus trap, גלילת רקע נעולה, RTL נכון.
- bottom-sheet במובייל, dialog במרכז בדסקטופ (`items-end sm:items-center`).

## U-9. עקביות ופרדיקטביליות — medium
אותו רכיב = אותה התנהגות בכל מקום (card לחיץ בכל המודולים או באף אחד); אותם אייקונים לאותן פעולות; אותו מיקום ל"עזרה"/"צור קשר" (3.2.6). Settings/Uninstall/Update UX לפי STANDARDS §16.

## U-10. Robustness — medium (impeccable `harden`)
- טקסט ארוך, שם ריק, 0 פריטים, 10k פריטים, offline, timeout, 401 באמצע פעולה, שעון של המכשיר שגוי, double-click על submit, חזרה מ-background במובייל.
- console נקי (0 errors, warnings מוסברים) בכל route.

## פורמט דיווח
`route@viewport - [ux] <state/flow> — <ממצא> → <תיקון>` + צילום; ממצא קוד: `file:line - [ux] …`.

# Rubric — 10 ממדים × ציון 1–10, והגדרת Done

הציון ניתן **רק על סמך ראיות** (detect.json, browser.json, צילומים, file:line). ממד שלא נבדק = `❓` ולא ציון.
לקח Anthropic (harness design): מעריך ללא כיול משבח. לכן — **ברירת המחדל היא 5**, ועולים רק עם ראיה לכל דרגה.

## סולם כללי
| ציון | משמעות | דוגמה |
|---|---|---|
| 1–3 | שבור / חסר — משתמש נתקל בזה בדקה הראשונה | טלפון מתהפך, אין dark mode בכלל, div-onClick בכל מקום |
| 4–6 | עובד אבל לא מקצועי — עקבי חלקית, יש חובות | 4:1 פיזי/לוגי, tokens עם 60 חריגים, empty states בחצי מהמודולים |
| 7–8 | מקצועי — מערכת אחת, מעט חריגים מתועדים | 0 high ב-detect, כל route עבר 3 viewports, axe ≤ 2 |
| 9–10 | מצטיין — נבדל, מלוטש, נבדק בכל state | זהות שמזוהה בלי לוגו; keyboard+SR מלא; AI מוטמע ומנוהל |

## 10 הממדים
| # | ממד | ראיות מרכזיות (מה מוריד/מעלה) |
|---|---|---|
| 1 | **RTL ועברית** | `rtl.*` findings; מבחן המראה ב-≥ 5 routes; מחרוזת הבדיקה; modals; טיפוגרפיה עברית |
| 2 | **רספונסיביות** | overflow-x ב-375/320; targets < 44; inputs < 16px; tablet layout; `dvh`; wide-screen anchoring |
| 3 | **נגישות** | axe violations לכל route; Tab pass; focus ring; labels; landmarks; 2.2 criteria; הצהרת נגישות |
| 4 | **עיצוב ומותג** | anti-slop list; tokens (hex בקוד); dark בשני מצבים; כיוון עיצובי אחד; טיפוגרפיה סולם |
| 5 | **UX flows ו-states** | 4 states לכל רשימה/טופס; URL state; ניווט עקבי; Undo; onboarding TTFV |
| 6 | **טפסים** | labels/autocomplete/inputmode; שגיאות ליד השדה; Enter; unsaved-changes; לא חוסם הקלדה |
| 7 | **ביצועים נתפסים** | skeleton; optimistic; console errors; layout shift; תמונות עם מידות; bundle של client ענק |
| 8 | **קלות הגדרה ותפעול** | defaults; settings מקובצים; חיבורים עם סטטוס; command bar/quick-add; זוכר מצב |
| 9 | **שכבת AI** | דפוסים מהטבלה ב-config-and-ai; עריכה לפני שמירה; fallback; eval; עלות |
| 10 | **בריאות קוד-UI** | קבצים > 800 שורות; רכיבים כפולים; inline styles; lint/tsc נקיים; audit script קיים ורץ ב-CI/hook |

## הגדרת Done לפרויקט
- **Baseline**: כל ממד ≥ 6 ואפס `blocker`.
- **Professional** (יעד ברירת מחדל): כל ממד ≥ 8, אפס `blocker`/`high` ב-detect, axe ≤ 2 לכל route, 0 console errors.
- **Excellent**: כל ממד ≥ 9 + evaluator מאשר "3 הדברים הכי גרועים" הם Nit בלבד.

## Severity של ממצא בודד
| תג | הגדרה | SLA בתוכנית |
|---|---|---|
| `[Blocker]` | שובר שימוש / חוקי (אין `dir=rtl`, אין viewport, form בלי labels בזרימה ראשית) | S1 — מיד |
| `[High]` | משתמש רגיל נתקל בזה בשימוש רגיל (טלפון מתהפך, target < 32px, hex ב-10+ מקומות, div-onClick) | S1–S3 |
| `[Medium]` | מקצוענות/עקביות (breakpoint חסר, skeleton חסר, slop) | S2–S5 |
| `[Nit]` | פוליש (`…`, tabular-nums, צל) | S4+ או backlog |

## Few-shot כיול למעריך
**דוגמה לציון נכון (RTL, home-hub לפני):**
> 100 classes פיזיים מול 24 לוגיים (detect.json), `family-chat-client.tsx:375` `pr-9 pl-3 text-right`, `app-shell.tsx:180` `md:border-l` על sidebar ימני, `contact/page.tsx` input tel עם `dir="ltr"` ✓. מבחן המראה: sidebar ✓, chat bubbles ✓, badge סגירה ב-`left-2` ✗ (3 routes). modal הגדרות נפתח נכון ✓. → **ציון 5**. לא 7: יחס 4:1 פיזי אומר שכל שינוי עתידי ישבור; לא 3: כלום לא "שבור" למשתמש היום כי האפליקציה חד-לשונית.

**דוגמה לציון שגוי (מה לא לעשות):**
> "ה-RTL נראה טוב, האפליקציה ב-dir=rtl והכל מיושר לימין. 8/10." — אין ראיה, אין file:line, לא נפתח modal, לא הוזרקה מחרוזת בדיקה. פסול.

**דוגמה ל-FAIL של contract:**
> Contract S2-3 "0 findings `rtl.physical-class` ב-src/components": detect.json אחרי = 7 findings (`hero-illustration.tsx` ×6 עם `rtl-exception` מתועד ✓, `task-card.tsx:41` `pl-2` ✗ בלי קומנט). → **FAIL** — פריט אחד לא מכוסה.

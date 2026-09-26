---
name: system-upgrade
description: שדרוג מערכת קיימת מקצה לקצה (web/Next/React, Electron, תוסף Chrome) — סריקה דטרמיניסטית + דפדפן חי, דוח מבוסס-ראיות ב-10 ממדים (RTL עברית, מובייל/דסקטופ, נגישות WCAG 2.2/ת"י 5568, עיצוב לא-גנרי, UX/states, טפסים, ביצועים נתפסים, קלות הגדרה, שכבת AI, בריאות קוד), תוכנית ספרינטים עם contracts, ביצוע אוטונומי עם commit וצילומי לפני/אחרי, והערכה ע"י סוכן נפרד. Trigger on - תשדרג את המערכת, תעבור ותשפר, המערכת מבולגנת, תקן RTL, תאימות מובייל, audit UX, שדרוג כלי, system upgrade, /system-upgrade.
---

# System Upgrade — שדרוג מערכת קיימת מקצה לקצה

הסקיל הזה הוא ה-**orchestrator**. הוא רץ ב-session הראשי ומפעיל שני סוכנים נפרדים (sub-agent לא יכול להפעיל sub-agent):
`system-upgrader` (סורק → מתכנן → מבצע) ואז `upgrade-evaluator` (מעריך סקפטי ב-context נקי). הפרדה זו היא הלקח המרכזי
של Anthropic ב-harness design: מודל שמעריך את עבודתו משבח אותה.

## פרמטרים
`/system-upgrade [path] [--mode product|brand|mixed] [--autonomy full|mechanical-only|plan-only] [--routes /a,/b] [--sprints S1-S3]`
- `path` — שורש הפרויקט (ברירת מחדל: cwd).
- `--mode` — `product` (dashboard/אפליקציה/כלי), `brand` (דף נחיתה/שיווקי), `mixed` (אפליקציה עם landing). ברירת מחדל: זיהוי אוטומטי (routes של marketing → mixed).
- `--autonomy` — ברירת מחדל **`full`** (החלטת המשתמש 2026-09-24): מבצע את כל הספרינטים בלי לעצור. `mechanical-only`: S1 בלבד אוטומטית, השאר מדווח. `plan-only`: סריקה + REPORT + PLAN + צילומי before, בלי לגעת בקוד.
- מה שלא צוין — הסוכן מחליט ומתעד ב-REPORT.

## 10 הממדים (מלא ב-`references/scoring.md`)
1 RTL ועברית · 2 רספונסיביות · 3 נגישות · 4 עיצוב ומותג · 5 UX flows ו-states · 6 טפסים · 7 ביצועים נתפסים · 8 קלות הגדרה ותפעול · 9 שכבת AI · 10 בריאות קוד-UI.
לכל ממד קובץ reference עם כללים ממוספרים, severity ו-Wrong/Right: `references/rtl-hebrew.md`, `responsive.md`, `a11y-wcag22.md`, `design-quality.md`, `ux-flows.md`, `config-and-ai.md`.

## תהליך (מה ה-session הראשי עושה)

### 1. הכנה
- ודא ש-`path` קיים, ושיש git (אם אין — `git init` + commit בסיס לפני הכל; אם המשתמש לא רוצה git — עצור ושאל).
- `git status` — working tree מלוכלך? רשום ב-REPORT ותן ל-upgrader ליצור branch `upgrade/<YYYY-MM-DD>` (הוא עושה stash/commit של העבודה הקיימת לפי הכללים שלו).

### 2. הפעלת `system-upgrader` (Agent tool, run_in_background: false)
פרומפט חובה כולל: path מוחלט, mode, autonomy, routes אם צוינו, ההנחיה "פעל לפי `~/.claude/skills/system-upgrade/SKILL.md` — כל שלבי 0-7", ומיקום התוצרים `<path>/.claude/upgrade/`.
הסוכן מחזיר: טבלת ממדים לפני/אחרי, commits, `[needs-human]`, 3 צעדים הבאים.

### 3. הפעלת `upgrade-evaluator` (Agent tool, context חדש)
פרומפט חובה: path, "קרא `<path>/.claude/upgrade/UPGRADE-PLAN.md` ו-`UPGRADE-REPORT.md`; בדוק כל contract בפועל (אפליקציה רצה + detect.py); כתוב `EVAL.md` לפי `templates/EVAL.md`; ברירת מחדל ציון 5, עולים רק עם ראיה". **אל תעביר** לו את ההסברים של ה-upgrader למה משהו בסדר.
ב-`plan-only` — ה-evaluator מעריך את **מצב הבסיס** ואת איכות ה-PLAN (האם ה-contracts מדידים? האם משהו קריטי חסר?).

### 4. סבב תיקון (עד 2)
אם EVAL = `ANOTHER-ROUND` → הפעל שוב את `system-upgrader` עם רשימת ה-FAIL בלבד ("תקן רק את אלה, אל תפתח חזיתות חדשות"), ואז evaluator שוב. אחרי 2 סבבים — עצור ודווח מה נשאר.

### 5. סיכום למשתמש (בעברית, קצר)
טבלת 10 הממדים לפני/אחרי · מה בוצע (commits) · מה דורש החלטה אנושית · קישורים ל-REPORT/PLAN/EVAL וצילומי before/after · 3 הצעדים הבאים.
עדכן זיכרון (`memory/`) אם נלמד משהו על הפרויקט שלא נגזר מהקוד (למשל: "ב-X ה-login חוסם בדיקה חיה — יש route public ב-/demo").

## תוצרים (ב-`<path>/.claude/upgrade/`)
| קובץ | מי כותב | מה |
|---|---|---|
| `detect.json` | detect.py | ממצאים דטרמיניסטיים (file:line, rule, severity, fix) |
| `detect-ignore.json` | upgrader (עם סיבה) | חריגים מתועדים — לא לחזור על false-positives |
| `browser.json` / `browser-after.json` | upgrader | תוצאות הבדיקה החיה לכל route × viewport × theme |
| `screenshots/before/`, `screenshots/after/` | upgrader | `<route>__<w>__<theme>.png` |
| `UPGRADE-REPORT.md` | upgrader | ציון בסיס + ממצאים לפי severity (תבנית `templates/UPGRADE-REPORT.md`) |
| `UPGRADE-PLAN.md` | upgrader | ספרינטים S1-S6 עם contracts (תבנית `templates/UPGRADE-PLAN.md`) |
| `EVAL.md` | evaluator | PASS/FAIL לכל contract, ציונים, verdict (תבנית `templates/EVAL.md`) |

## הרצה ידנית של הכלים
```bash
python ~/.claude/skills/system-upgrade/scripts/detect.py <root> --md            # סיכום Markdown + detect.json
python ~/.claude/skills/system-upgrade/scripts/detect.py <root> --out x.json    # exit 2 = יש blocker/high
```
פרוטוקול הדפדפן החי: `scripts/browser-pass.md`.

## חוקי ברזל (חלים על שני הסוכנים)
1. **ראיה או כלום** — כל ממצא: `file:line` או `route@viewport` + צילום. `❓` עדיף על ניחוש.
2. **כללי הפרויקט גוברים** — `design-rules`, `_AUDIT/STANDARDS.md`, `BRAND.md`, `DESIGN.md`, `CLAUDE.md`. סתירה עם הסטנדרט (למשל כלל שמורה על classes פיזיים) → הצעת מיגרציה ב-PLAN, לא דריסה שקטה.
3. **צעדים קטנים, אף פעם לא rewrite** (STANDARDS חוק ברזל #1). קובץ ענק מפרקים בספרינט נפרד עם contract משלו.
4. **טקסט עברי חדש** למשתמש (labels, שגיאות, empty states) → `copywriting-agent` אם קיים בפרויקט, אחרת סקיל `anthropic-skills:hebrew-copywriting` (STANDARDS §20.5).
5. **לא נוגעים** בלוגיקה עסקית, DB, auth, תשלומים, API contracts — מסמנים `[needs-human]`. UI/UX/layout/tokens/a11y/copy בלבד.
6. **git**: branch `upgrade/<date>`, commit לכל ספרינט עם הודעה `upgrade(S2): rtl logical classes + tablet breakpoints`, `lint`+`typecheck` (ומה שיש: tests) נקיים לפני commit. אין force-push, אין מחיקת branches.
7. **בדיקה חיה לפני ואחרי** באותם routes/viewports. אם אי אפשר להריץ — הממדים התלויים מסומנים `❓` ולא מקבלים ציון.
8. **Definition of Done** = Professional (`scoring.md`): כל ממד ≥ 8, 0 blocker/high, axe ≤ 2 לכל route, 0 console errors — או דיווח מפורש מה חסר ולמה.

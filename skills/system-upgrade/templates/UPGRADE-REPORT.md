# UPGRADE REPORT — <שם המערכת>

> תאריך: <YYYY-MM-DD> · stack: <Next 16 / Electron / Chrome ext / WPF> · mode: <product | brand | mixed>
> הורץ: detect.py ✅/❌ · דפדפן חי ✅/❌ (<איך: launch.json name / URL>) · axe ✅/❌ · lint/tsc ✅/❌
> כללי פרויקט שנמצאו: <design-rules / STANDARDS.md §… / BRAND.md / אין>
> כל שורה כאן מגובה ב-file:line או בצילום ב-`.claude/upgrade/screenshots/before/`. `❓` = לא נבדק, לא נוחש.

## ציון בסיס (לפני)

| # | ממד | ציון | הראיה המרכזית |
|---|---|---|---|
| 1 | RTL ועברית | | |
| 2 | רספונסיביות | | |
| 3 | נגישות | | |
| 4 | עיצוב ומותג | | |
| 5 | UX flows ו-states | | |
| 6 | טפסים | | |
| 7 | ביצועים נתפסים | | |
| 8 | קלות הגדרה ותפעול | | |
| 9 | שכבת AI | | |
| 10 | בריאות קוד-UI | | |

**סיכום detect.json:** blocker N · high N · medium N · low N · (top rule ids: …)
**סיכום browser.json:** routes N × viewports N · overflow-x ב-N · targets<44 ב-N · console errors N · axe violations N

## ממצאים לפי severity

### [Blocker]
- `file:line - [category] ממצא → תיקון`

### [High]
- …

### [Medium]
- …

### [Nit]
- …

## ממצאי דפדפן (לפי route)

| route | 375 | 768 | 1440 | dark | הערות |
|---|---|---|---|---|---|
| / | ✅/❌ | | | | overflow / targets / console / axe |

צילומים: `screenshots/before/<route>__<viewport>__<theme>.png`

## מה עובד טוב (לשמור)
- …

## התנגשויות בין כללי הפרויקט לסטנדרט
- <כלל פרויקט> מול <סטנדרט> → הצעה: … (לא שונה בשלב זה)

## לא נבדק (❓) ולמה
- …

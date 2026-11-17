---
name: secrets-hygiene-check
description: "Zero-secrets check before commit or release: scans source for API keys, tokens, passwords and connection strings, verifies .gitignore and environment-based config. Stops and reports on any real finding. Trigger on: check for secrets, before commit, leaked key worry."
---

# Secrets Hygiene Check

`_AUDIT/STANDARDS.md` מגדיר "אפס secrets בקוד" כדרישת חובה לכל כלי, ובודק אותה
בכל מחזור audit. הסקיל הזה מריץ את אותה בדיקה בצורה עקבית, בלי לגלות אותה
מחדש כל פעם.

## שלבים

1. **סרוק תבניות secrets נפוצות** בעזרת Grep על `src/`/קוד המקור של הפרויקט
   (לא `node_modules`, `dist`, `build`, `win-unpacked`):
   - מפתחות API (`api[_-]?key`, `sk-`, `AIza`, `ghp_`, מחרוזות ארוכות עם אותיות+מספרים)
   - טוקנים/סודות (`token`, `secret`, `password`, `client_secret`)
   - connection strings (`mongodb://`, `postgres://`, `Server=...;Password=`)
   - מפתחות פרטיים מוטבעים (`-----BEGIN PRIVATE KEY-----`)
2. **בדוק את `.gitignore`** — מוודא שהוא כולל `.env`, קבצי credentials, ותיקיות
   config שעלולות להכיל סודות אמיתיים בסביבת הפיתוח.
3. **בדוק את דרך טעינת הקונפיג בפועל** — אמור להשתמש ב-`%APPDATA%`/משתני סביבה/
   קובץ קונפיג מקומי לא-מגורסן, ולא בנתיבים קשיחים עם ערכים רגישים מוטבעים בקוד.
4. **דווח בפורמט תמציתי** (✅/❌ לכל בדיקה), באותו סגנון שכבר קיים בטבלת הסטטוס
   של `_AUDIT/STANDARDS.md`, כדי שאפשר יהיה להזין את התוצאה ישירות לשם או
   ל-`_AUDIT/AUDIT-<Tool>.md`.

## כללים

- ממצא = ציטוט קובץ+שורה, לא ניחוש. אם משהו נראה חשוד אבל לא ודאי (למשל מחרוזת
  שנראית כמו מפתח אבל היא בעצם דוגמה/placeholder) — לסמן כ-⚠️ לבדיקה ידנית,
  לא לקבוע בוודאות.
- אם נמצא secret אמיתי בקוד: לדווח מיד למשתמש ולא להמשיך בפעולות נוספות
  (commit/release/publish) עד שהוא יטפל בזה. אל תמחק/תחליף את הסוד בעצמך בלי
  אישור מפורש.

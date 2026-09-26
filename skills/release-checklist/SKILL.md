---
name: release-checklist
description: מפעיל checklist שחרור גרסה לפני כל release/build של כלי מ-PC-Software או Chrome-Extensions (AutoProcessTwin, FamilyQuest PC, TabToTable-AI ואחרים). משתמש ב-RELEASE-CHECKLIST.md הייעודי אם קיים, ואם לא — נופל לכלל הסנכרון הגלובלי מ-_AUDIT/STANDARDS.md. Trigger on - מוכן לשחרור, בדוק לפני release, גרסה חדשה, לפני שאני מוציא installer, בדוק לפני publish, checklist שחרור.
---

# Release Checklist — כל כלי ב-CLAUDE BOTS

לפני שמסמנים release/build כ"גמור" לכל אחד מהכלים בתיקיות `PC-Software/` או
`Chrome-Extensions/`, יש להריץ את הבדיקות הבאות. אל תדלג על שלב כי "זו רק גרסה קטנה" —
`_AUDIT/STANDARDS.md` מגדיר את זה כחוק ברזל שחל גם על שינויים קטנים.

## שלב 1 — זיהוי הפרויקט וה-checklist הרלוונטי

1. זהה את שם הכלי מתוך הבקשה/הנתיב (למשל `PC-Software/AutoProcessTwin`,
   `PC-Software/FamilyQuest PC`, `Chrome-Extensions/TabToTable-AI`).
2. חפש `<project>/RELEASE-CHECKLIST.md`.
   - **אם קיים** (נכון לעכשיו: AutoProcessTwin) — עקוב אחריו **כמו שהוא, שורה-שורה**.
     אל תשכפל את התוכן שלו כאן ואל תמציא גרסה מקבילה — הוא מקור האמת לאותו כלי.
   - **אם לא קיים** (FamilyQuest PC, TabToTable-AI, כלים אחרים) — המשך לשלב 2.

## שלב 2 — כלל הסנכרון הגלובלי (מ-`_AUDIT/STANDARDS.md`)

כשאין קובץ checklist ייעודי, אכוף את חוקי הברזל הבאים, כולם **באותה פעולה**:

- [ ] מספר הגרסה מעודכן בו-זמנית בכל המקומות: `version.json`/`package.json`/
      `.csproj`/`manifest.json`, שם קובץ ההתקנה (`<Tool>-Setup-<version>.exe`),
      כותרת חלון/מסך About, ו-`CHANGELOG.md`. אסור שאחד מהם יפגר אחרי השני.
- [ ] קובץ ההתקנה/ה-build עצמו **נבנה מחדש בפועל** ומוחלף בשורש הפרויקט — לא
      נשאר קובץ ישן/לא-תואם-גרסה לצד קוד מעודכן.
- [ ] `CHANGELOG.md` מתעד מה בדיוק השתנה (Keep a Changelog: Added/Changed/Fixed/Removed).
- [ ] `SPEC.md` מעודכן אם הפונקציונליות השתנתה.
- [ ] `README.md` מעודכן אם ההתקנה/השימוש השתנו.
- [ ] תיקיית השורש נקייה — רק installer/CHANGELOG/SPEC/README (בלי סקריפטי build,
      `dist/`/`build/` ביניים, כפילויות של installer ישן).
- [ ] אפס secrets בקוד (אם יש חשד — הפעל את סקיל `secrets-hygiene-check`).

## שלב 3 — כלל ייעודי ל-FamilyQuest PC

לפי לקח מתועד בזיכרון: **כל שדרוג ל-FamilyQuest PC חייב, יחד ובאותה פעולה**:

- [ ] עדכון דף הנחיתה (Artifact) — חפש אותה עם `Artifact` tool `action: "list"`,
      קרא את התוכן הנוכחי, ופרסם גרסה מעודכנת שמשקפת את הפיצ'רים/הגרסה החדשים.
      אל תשאיר אותה עם מספר גרסה/פיצ'רים ישנים.
- [ ] עדכון `package.json`'s `"version"` (לא רק README/SPEC — הבאג התועד: הגרסה
      נשארה `1.0.0` דרך כמה סבבים בזמן שה-README כבר עדכן מספרים).
- [ ] `npm run build && npm run dist` — בניית installer מחדש בפועל, לא רק commit לקוד.
      שם הקובץ יציב (`FamilyQuest-PC-Setup.exe`, בלי `${version}` בשם) — כל
      `npm run dist` דורס את אותו קובץ, **אל תחזיר** את `${version}` לשם הקובץ.
- [ ] אחרי כל build: מחק את `release/win-unpacked/` (תיקיית ביניים בת ~250MB+
      שניתנת לשחזור מלא) — נשארים ב-`release/` רק `.exe`/`.blockmap`/`latest.yml`/
      `builder-debug.yml`.

## שלב 4 — סיום

- [ ] עדכן את השורה המתאימה בטבלת הסטטוס ב-`_AUDIT/STANDARDS.md` עבור הכלי.
- [ ] אם קיים `_AUDIT/AUDIT-<Tool>.md` — עדכן גם אותו בהתאם.
- [ ] אם יש git בפרויקט — הצע לתייג את הגרסה (`git tag vX.Y.Z`), אל תעשה זאת אוטומטית.

## הערות

- זהו סקיל אכיפה/checklist, לא מחליף בדיקה ידנית של הפונקציונליות עצמה
  (smoke test) — אם יש `RELEASE-CHECKLIST.md` ייעודי, הוא כולל גם את זה.
- אם מתגלה שחסר `RELEASE-CHECKLIST.md` לכלי שמשתחרר בקביעות (כמו FamilyQuest PC
  או TabToTable-AI), שווה להציע למשתמש ליצור אחד במבנה של AutoProcessTwin —
  אך רק בבקשה מפורשת, לא באופן יזום באמצע release.

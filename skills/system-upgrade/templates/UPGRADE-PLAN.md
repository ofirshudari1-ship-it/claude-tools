# UPGRADE PLAN — <שם המערכת>

> מבוסס על UPGRADE-REPORT מ-<תאריך>. autonomy: <full | mechanical-only | plan-only>. branch: `upgrade/<YYYY-MM-DD>`.
> כל ספרינט = commit אחד (או כמה קטנים), lint+typecheck נקיים לפני commit, re-detect + צילומי after בסוף.
> כלל ברזל: צעדים קטנים, בלי rewrite, בלי שינוי לוגיקה עסקית/DB/auth (→ `[needs-human]`).

## כיוון (brand mode בלבד — 3 שורות)
1. האלמנט האופייני: …
2. גופן + פלטה: …
3. "הדבר האחד" שזוכרים: …

## ספרינטים

### S1 — מכני ואוטומטי (סיכון נמוך)
**היקף:** … (למשל: eslint-plugin-rtl-friendly --fix, token חסר, dvh, min-h-0, transition-all)
**Contract (Done כש-):**
- [ ] `detect.py` → 0 findings `rtl.physical-class` ב-`src/components` (חריגים עם `rtl-exception`)
- [ ] `npx eslint` + `npx tsc --noEmit` נקיים
- [ ] צילומי after ב-3 viewports זהים ל-before **חוץ** מ-… (אין רגרסיה חזותית)
**סיכון:** … · **`[needs-human]`:** …

### S2 — RTL / layout / responsive
**היקף:** …
**Contract:**
- [ ] אין overflow-x ב-375 ב-N routes (browser.json)
- [ ] targets < 44px = 0 ב-375
- [ ] מבחן המראה עובר ב-N routes + modals
- [ ] עדכון כללי הפרויקט (design-rules R3 → logical) אם אושר
**סיכון:** … · **`[needs-human]`:** …

### S3 — נגישות
**Contract:**
- [ ] axe violations ≤ 2 לכל route (light+dark)
- [ ] 0 `a11y.div-onclick`, 0 `a11y.icon-button-no-label`, 0 `a11y.outline-none`
- [ ] Tab pass ב-N routes: focus ring גלוי, לא מוסתר
- [ ] הצהרת נגישות קיימת ומקושרת (ת"י 5568)

### S4 — עיצוב ופוליש
**Contract:**
- [ ] 0 `design.hex-in-tsx` (חוץ מ-tokens/theme קבצים)
- [ ] סולם טיפוגרפי: 0 `text-[≤11px]` מחוץ ל-badge
- [ ] dark: כל token ב-3 הבלוקים; `color-scheme` + `theme-color`
- [ ] "הסר אקססורי אחד" בוצע ב-N מסכים

### S5 — UX flows / states / forms
**Contract:**
- [ ] 4 states לכל רשימה ראשית (empty/loading/error/success) — רשימה: …
- [ ] טפסים: labels/autocomplete/inputmode/שגיאות ליד השדה — טפסים: …
- [ ] URL state לטאבים/פילטרים ב-…
- [ ] 0 `window.alert/confirm`

### S6 — הגדרה ו-AI
**Contract:**
- [ ] settings מקובצים, שמירה מיידית עם feedback
- [ ] דפוס AI אחד לפחות מוטמע עם עריכה-לפני-שמירה + fallback: …
- [ ] `[needs-human]`: …

## סדר ביצוע ותלויות
S1 → S2 → S3 → S4 → S5 → S6. S3/S4 יכולים להתבצע במקביל אחרי S2.

## מחוץ להיקף (במפורש)
- …

## יעד סופי
Professional: כל ממד ≥ 8, 0 blocker/high, axe ≤ 2, 0 console errors. (ראה scoring.md)

# רספונסיביות — מובייל, טאבלט, דסקטופ, מסך רחב

מקורות: Vercel web-interface-guidelines, WCAG 2.2 (1.4.10 Reflow, 2.5.8 Target Size), home-hub `design-rules` R7, STANDARDS §14.2.

## RS-1. Viewports חובה לבדיקה — blocker אם חסר viewport meta
| שם | רוחב | מה בודקים |
|---|---|---|
| mobile | 375 (+320 ל-Reflow) | bottom-nav, שום גלילה אופקית, 44px targets, 16px inputs, כותרות לא נשברות באמצע מילה |
| tablet | 768 | האם יש layout ביניים או שזה מובייל מתוח / דסקטופ דחוס |
| desktop | 1440 | sidebar, grid 2-3 עמודות, max-width לתוכן |
| wide | 2560 (או zoom 50%) | תוכן מעוגן (RTL: לימין), לא "צף" במרכז מסך 27" |
`<meta name="viewport" content="width=device-width, initial-scale=1">` — בלי `maximum-scale=1` / `user-scalable=no` (אסור לחסום zoom).

## RS-2. Breakpoints מדורגים, לא הכל ב-`sm:` — medium
דפוס שנמצא ב-home-hub: `sm:` ×412 מול `md:` ×39 — כלומר אין מצב טאבלט. כלל: layout שמשתנה בין מובייל לדסקטופ צריך לפחות שתי נקודות (`md:` לטאבלט, `lg:`/`xl:` לדסקטופ). Grid: `grid-cols-1 md:grid-cols-2 xl:grid-cols-3`.

## RS-3. גובה מסך: `dvh` לא `vh` — medium
`h-screen`/`100vh` במובייל = שורת הכתובת של הדפדפן מכסה את התחתית. `h-dvh` / `min-h-dvh` (fallback: `min-height:100vh; min-height:100dvh`).

## RS-4. Bottom-nav ואזורים בטוחים — medium
`fixed bottom-0` → `pb-[env(safe-area-inset-bottom)]` (iPhone home indicator); Capacitor/PWA: `viewport-fit=cover`. תוכן הדף מקבל `pb-20` (או `padding-bottom: calc(nav-height + safe-area)`) כדי שהפריט האחרון לא יוסתר.

## RS-5. Hit targets — high במובייל
≥ 44×44 CSS px במובייל, ≥ 24×24 בדסקטופ (WCAG 2.5.8). אייקון 16px בתוך כפתור = `p-3` לפחות. רווח בין targets סמוכים ≥ 8px. `touch-action: manipulation` על כפתורים (מבטל double-tap zoom delay).
- בדיקה חיה: `[...document.querySelectorAll('button,a,[role=button]')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&(r.width<44||r.height<44)})`.

## RS-6. טקסט וקלט במובייל — high
- `input`/`select`/`textarea` ≥ 16px (`text-base`) — אחרת iOS Safari עושה zoom-in אוטומטי.
- טקסט גוף ≥ 16px; משני ≥ 14px (`text-sm`); `text-[10px]`/`text-[11px]` = לא קריא במובייל, מותר רק ל-badge/caption בודד.
- סולם טיפוגרפי אחד (למשל 12/14/16/18/20/24/30/36) במקום ערכים שרירותיים `text-[13px]`.

## RS-7. Reflow (1.4.10) — high
ב-320px ו-zoom 200% אין גלילה בשני צירים, אין תוכן חתוך. טבלאות רחבות → `overflow-x-auto` על wrapper **או** cards במובייל. `min-w-0` על flex children עם טקסט ארוך; `break-words` / `truncate` מכוון.
- בדיקה חיה: `document.documentElement.scrollWidth > window.innerWidth`.

## RS-8. אין רוחב קבוע גדול — medium
`w-[600px]` / `min-w-[500px]` שובר מובייל. השתמש `w-full max-w-[600px]`. תמונות: `max-w-full h-auto` + `width/height` מפורשים (מונע CLS).

## RS-9. ניווט לפי מכשיר — medium
מובייל: bottom-nav (≤5 פריטים) או drawer; דסקטופ: sidebar/top-nav. **אותם פריטים באותו סדר** בשניהם (3.2.3 Consistent Navigation). Hover-only interactions חייבות חלופת tap.

## RS-10. מסך רחב — medium (R7 של home-hub)
תוכן ב-xl/2xl מעוגן לצד הקריאה (RTL: ימין) עם cap: `max-w-[800px] lg:max-w-[920px] xl:max-w-[1080px] 2xl:max-w-[1220px]`. dashboard: grid שמתמלא, לא עמודה בודדת צרה במרכז.

## RS-11. Desktop tools (Electron/WPF/PyQt) — STANDARDS §14.2
"רספונסיבי" = DPI 100–200% (`PerMonitorV2` awareness), גודל חלון מינימלי מוגדר, עובד ב-1366×768, זוכר מיקום/גודל חלון, לא נפתח מחוץ למסך.

## RS-12. Chrome extension popup — STANDARDS §13
popup ≤ 800×600; רוחב קבוע (360–420px) עם `min-height`; תוכן ארוך → options page, לא גלילה בפופאפ.

## צ'קליסט הרצה חיה לכל route
- [ ] 375: אין overflow-x, bottom-nav לא מסתיר תוכן, targets ≥ 44, inputs ≥ 16px
- [ ] 768: יש layout ביניים סביר (לא עמודה אחת מתוחה)
- [ ] 1440: sidebar + תוכן, אין שורות טקסט > 80 תווים
- [ ] 2560: תוכן מעוגן ולא אבוד במרכז
- [ ] light + dark בכל אחד

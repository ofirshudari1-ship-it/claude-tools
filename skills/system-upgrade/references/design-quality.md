# איכות עיצוב — מודרני, שיווקי, ייחודי, לא גנרי

מקורות: Anthropic `frontend-design` skill, `impeccable` (pbakaus) audit rules, Vercel guidelines (visual design), SaaS design trends 2026 (Linear/Vercel/Attio/Stripe), STANDARDS §3/§15/§18.5/§19/§21.

## D-0. קודם כל: brand mode או product mode?
| | **brand** (דף נחיתה, אתר שיווקי, onboarding, splash) | **product** (dashboard, אפליקציה, הגדרות, כלי עבודה) |
|---|---|---|
| מטרה | רגש, בידול, המרה | מהירות, בהירות, צפיפות מידע נכונה |
| טיפוגרפיה | display font מובחן + גדלים גדולים, hero אופייני לתחום | סולם קומפקטי, היררכיה ממשקל ורווח |
| צבע | accent חזק, גרדיאנט/תמונה **אחת** דומיננטית | צבע שמור ל-state ומשמעות; chrome שקט |
| motion | רצף טעינה מתוזמר אחד | micro-interactions 150–250ms בלבד |
| layout | full-bleed, אסימטריה מכוונת, whitespace | grid, טבלאות לפני גרפים, cards רק לישויות |
לא לערבב: dashboard עם hero-gradient = slop; דף נחיתה שנראה כמו admin = לא ממיר.

## D-1. Anti-"AI slop" — הרשימה השחורה (medium כל אחד)
- גופן ברירת מחדל: Inter / Roboto / Arial / system-ui כגופן **היחיד** (לעברית: Assistant/Heebo/Rubik/Noto Sans Hebrew — ולבחור **אחד** ראשי + לכל היותר אחד משני).
- גרדיאנט סגול→כחול / warm-cream+terracotta / near-black+acid-green כברירת מחדל בלי סיבה מהמותג.
- cards בתוך cards; כל דבר ב-`rounded-2xl shadow-lg`; אותו border-radius לכל האלמנטים.
- eyebrow labels ב-`uppercase tracking-widest`; הדגשת מילה אחת בצבע בכותרת; emoji כאייקונים.
- 3 עמודות "פיצ'רים" עם אייקון-כותרת-פסקה זהות; סטטיסטיקות מנופחות ב-hero.
- אפור טהור (`#808080`, `gray-500`) על רקע צבעוני; שחור טהור `#000` לטקסט (עדיף ink כהה מגוון).
- easing `bounce`/`elastic`; `transition: all`; hover שמגדיל `scale-110`.
- **מבחן:** אם אפשר להחליף את הלוגו וזה נראה כמו כל SaaS אחר — זה slop.

## D-2. להתחייב לכיוון עיצובי אחד — high (brand mode)
לפני שינוי: לכתוב ב-PLAN 3 שורות "כיוון": (1) מה האלמנט הכי אופייני לעולם של המוצר (בית חכם? משפחה? קבצים?) ואיך הוא מופיע ב-hero; (2) גופן+פלטה (מקסימום 2 גופנים, accent אחד + ניטרלים); (3) מה "הדבר האחד" שזוכרים. אם קיים `BRAND.md`/`brand-kit.json` — הוא המקור, לא ממציאים.

## D-3. Token system — high
כל צבע/רווח/רדיוס/צל/משך דרך tokens (`--accent`, `--surface`, `--ink`, `--line`, `--radius-sm/md/lg`, `--shadow-1/2`, `--motion-fast/base`). hex בקוד רכיבים = ממצא (חריג: קובץ tokens, לוגו של צד שלישי, `token-exception` בקומנט).
- Tailwind v4: `@theme inline { --color-accent: var(--accent); }` כדי לקבל `bg-accent` — **כל** token חייב להיות ממופה (ב-home-hub `--weather` חסר).
- tints: `color-mix(in srgb, var(--x) 12%, var(--surface))` במקום hex חדש.
- STANDARDS §3: `design-tokens.json` (W3C format) לכל כלי; spacing 4/8/12/16/24/32; motion 150/250/400.

## D-4. Dark mode — medium
- כל token מוגדר ב-3 מקומות: `:root`, `@media (prefers-color-scheme: dark) :root:not([data-theme="light"])`, `:root[data-theme="dark"]` (home-hub R4). token חדש נכנס לשלושתם או לא נכנס.
- `color-scheme: light dark` על `html` (scrollbars, inputs, select ב-Windows); `<meta name="theme-color">` תואם רקע (אחד לכל theme).
- dark ≠ inverted: משטחים מדורגים (`--surface` < `--surface-2` < `--surface-3` בהירים יותר ככל שגבוהים), צללים חלשים יותר, accent מעט מבוהר, טקסט לא לבן טהור (`#EAEAEA`).
- ניגודיות נבדקת **בשני** המצבים.

## D-5. טיפוגרפיה — medium
- סולם מוגדר (12/14/16/18/20/24/30/36/48) — לא `text-[13px]`/`text-[11px]` פזורים.
- היררכיה ממשקל+גודל+צבע (`ink` / `ink-dim`), לא מ-4 צבעים שונים.
- line-height: 1.2 לכותרות, 1.5–1.7 לגוף (עברית לכיוון הגבוה); `max-w-prose`.
- `tabular-nums` למספרים בטבלאות; `text-wrap: balance` לכותרות; `…` לא `...`.

## D-6. משטחים, צללים, גבולות — low
- צל בשכבות (`0 1px 2px rgba(0,0,0,.04), 0 4px 12px rgba(0,0,0,.06)`), לא `shadow-2xl` אחד; border חצי-שקוף + צל יחד.
- radius ילד ≤ radius הורה (כפתור בתוך card: `rounded-lg` בתוך `rounded-xl`).
- על רקע צבעוני: border/צל/טקסט מגוונים לכיוון אותו hue, לא אפור.
- card = ישות; לא כל section צריך card. רשימה = שורות עם `divide-y`, לא 20 cards.

## D-7. Motion ומיקרו-אינטראקציות — medium (§18.5)
- hover על כל לחיץ (צבע/צל עדין, לא scale); active (`scale-[0.98]` מותר); focus-visible ring.
- success feedback אחרי פעולה (toast "נשמר ✓" / checkmark 300ms), לא state דומם.
- skeleton תואם למבנה הסופי (לא spinner בודד; skeleton מופיע אחרי 150–300ms ונשאר ≥ 300ms כדי לא להבהב).
- טעינה בכפתור: spinner **ליד** הטקסט, הטקסט נשאר.
- animate רק `transform`/`opacity`; `prefers-reduced-motion`; `transform-origin` נכון; cancelable.
- רצף page-load אחד מתוזמר (brand mode) > fade-in על כל אלמנט.

## D-8. Layout ו-rhythm — medium
- grid רווחים מסולם אחד (`gap-4`/`gap-6`), לא `mt-[13px]`.
- יישור אופטי (אייקון+טקסט מאוזנים), כל אלמנט מיושר בכוונה.
- page container אחיד (`.page-shell` ב-home-hub R1) — לא `max-w-* mx-auto px-*` שונה בכל עמוד.
- widgets באותה שורה באותו גובה (`h-full` + `auto-rows-fr`); רשימות ב-widget ≤ 4 פריטים + "ראה הכל (N)" (R6).
- אין layout shift: מידות לתמונות, `min-h` לאזורים דינמיים, skeleton באותו גודל.

## D-9. אייקונים ולוגו — low
סט אייקונים אחד (lucide), גודל אחיד (16/20/24), stroke אחיד; לוגו SVG אמיתי (STANDARDS §3), favicon + `apple-touch-icon` + `theme-color`; Chrome ext: PNG 16/32/48/128.

## D-10. Desktop tools — STANDARDS §19/§21
Splash ממותג (גרדיאנט מותג, לוגו דומיננטי, ≥ 800ms, timeout 8s, `show:false` עד מוכן); installer באותה שפה ויזואלית; Fluent-ish (§15): toast 300–400px 3–6s, click target ≥ 36px.

## D-11. "הסר אקססורי אחד" — בדיקת סיום
לפני שמסיימים ספרינט עיצובי: להסתכל על המסך ולהוריד דבר אחד (צל, גבול, אייקון, גרדיאנט, badge) שלא משרת הבנה. אם אחרי ההסרה זה נראה טוב יותר — הוא היה מיותר.

## ציון ממד "עיצוב" (ראה scoring.md)
1–3: hex פזור, slop, אין tokens, dark שבור · 4–6: tokens חלקיים, עקבי אבל גנרי · 7–8: מערכת אחת, כיוון ברור, dark מלא · 9–10: זהות ייחודית שמזוהה בלי לוגו + פוליש בכל state.

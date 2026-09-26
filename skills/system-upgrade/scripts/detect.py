#!/usr/bin/env python3
"""
detect.py - deterministic UI/UX/RTL/a11y detector for the system-upgrade skill.

Usage:
  python detect.py <root> [--out .claude/upgrade/detect.json] [--stack auto|next|react|html|electron|chrome-ext]
                          [--ignore .claude/upgrade/detect-ignore.json] [--md] [--quiet]

Exit codes: 0 = no blocker/high findings, 2 = blocker/high findings exist, 1 = scan failure.
Every finding carries file, line, rule id, severity, category, snippet and a fix hint.
No LLM, no network. Windows/macOS/Linux, Python 3.8+.
"""
import argparse
import fnmatch
import json
import os
import re
import sys
from collections import Counter, defaultdict

SKIP_DIRS = {
    "node_modules", ".next", "dist", "build", "out", "android", "ios", ".git", "coverage",
    ".playwright-mcp", "__pycache__", "vendor", ".turbo", ".vercel", "public", ".claude",
    "storybook-static", "release", "bin", "obj", "packages",
}
CODE_EXT = {".tsx", ".jsx", ".ts", ".js", ".vue", ".svelte", ".astro", ".html", ".htm"}
MARKUP_EXT = {".tsx", ".jsx", ".vue", ".svelte", ".astro", ".html", ".htm"}
CSS_EXT = {".css", ".scss", ".sass", ".less"}
ALL_EXT = CODE_EXT | CSS_EXT

SEV_ORDER = {"blocker": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
HEBREW_RE = re.compile(r"[\u0590-\u05FF]")

VARIANT = r"(?:(?:sm|md|lg|xl|2xl|hover|focus|focus-visible|focus-within|active|group-hover|peer-checked|disabled|first|last|odd|even|dark|print|motion-safe|motion-reduce|has-\[[^\]]+\]|data-\[[^\]]+\]|aria-\[[^\]]+\]|\[[^\]]+\]):)*"
PHYSICAL_TOKEN_RE = re.compile(
    r"(?<![\w:\-\[/])" + VARIANT + r"-?(?:"
    r"(?:ml|mr|pl|pr|scroll-ml|scroll-mr|scroll-pl|scroll-pr)-(?:\[[^\]]+\]|[\w./]+)"
    r"|(?:left|right)-(?:\[[^\]]+\]|[\w./]+)"
    r"|rounded-(?:l|r|tl|tr|bl|br)(?:-[\w.]+)?"
    r"|border-(?:l|r)(?:-[\w./\[\]]+)?"
    r"|text-(?:left|right)"
    r"|float-(?:left|right)"
    r"|space-x-[\w.]+"
    r")(?![\w-])"
)
LOGICAL_TOKEN_RE = re.compile(
    r"(?<![\w:\-\[/])" + VARIANT + r"-?(?:(?:ms|me|ps|pe|start|end|inset-s|inset-e|scroll-ms|scroll-me|scroll-ps|scroll-pe)-(?:\[[^\]]+\]|[\w./]+)|rounded-(?:s|e|ss|se|es|ee)(?:-[\w.]+)?|border-(?:s|e)(?:-[\w./\[\]]+)?|text-(?:start|end)|float-(?:start|end))(?![\w-])"
)
CSS_PHYSICAL_RE = re.compile(
    r"\b(?:margin-left|margin-right|padding-left|padding-right|border-left(?:-[a-z]+)?|border-right(?:-[a-z]+)?|border-(?:top|bottom)-(?:left|right)-radius)\s*:"
    r"|(?<![\w-])(?:left|right)\s*:\s*[^;]+;"
    r"|text-align\s*:\s*(?:left|right)\b"
    r"|float\s*:\s*(?:left|right)\b"
)
DIRECTIONAL_ICON_RE = re.compile(r"\b(?:ArrowLeft|ArrowRight|ChevronLeft|ChevronRight|ChevronsLeft|ChevronsRight|ArrowLeftRight|ArrowBigLeft|ArrowBigRight|CornerDownLeft|CornerDownRight|PanelLeft|PanelRight)\b")
HEX_RE = re.compile(r"(?<![\w&#])#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b(?![0-9a-fA-F])")
RAW_PALETTE_RE = re.compile(r"(?<![\w-])(?:text|bg|border|ring|from|to|via|fill|stroke|divide|outline|shadow)-(?:gray|slate|zinc|neutral|stone|red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose)-\d{2,3}(?![\w-])")
TINY_FONT_RE = re.compile(r"text-\[(\d+(?:\.\d+)?)px\]")
FIXED_W_RE = re.compile(r"(?<![\w-])(?:w|min-w)-\[(\d+)px\]")
# [^>] alone stops at the '>' inside an inline arrow handler's "=>" (e.g. onChange={(e) => ...}),
# truncating the match before later attributes like aria-label — treat "=>" as one unit instead.
TAG_INPUT_RE = re.compile(r"<(?:input|Input)\b(?:=>|[^>])*?/?>", re.S)
TAG_TEXTAREA_RE = re.compile(r"<(?:textarea|Textarea)\b(?:=>|[^>])*?>", re.S)
TAG_IMG_RE = re.compile(r"<(?:img|Image)\b[^>]*?/?>", re.S)
TAG_BUTTON_RE = re.compile(r"<button\b([^>]*)>(.*?)</button>", re.S)
TAG_CLICKY_RE = re.compile(r"<(div|span|li|p|section|article|tr|td|header|footer|label|h[1-6])\b([^>]*?)\bonClick=", re.S)
ALERT_RE = re.compile(r"(?<![\w.])(?:window\.)?(?:alert|confirm|prompt)\s*\(")
DATE_RE = re.compile(r"\.toLocale(?:Date|Time)?String\(\s*\)|getMonth\(\)\s*\+\s*1")
FONT_DEFAULT_RE = re.compile(r"font-family\s*:[^;]*\b(?:Inter|Roboto|Arial)\b|from\s+['\"]next/font/google['\"]|\b(?:Inter|Roboto)\s*\(\s*\{")

def rel(path, root):
    return os.path.relpath(path, root).replace("\\", "/")

def line_of(text, idx):
    return text.count("\n", 0, idx) + 1

def snippet(text, idx, width=110):
    start = text.rfind("\n", 0, idx) + 1
    end = text.find("\n", idx)
    end = len(text) if end == -1 else end
    s = text[start:end].strip()
    return (s[:width] + "…") if len(s) > width else s

def detect_stack(root):
    pj = os.path.join(root, "package.json")
    deps = {}
    if os.path.exists(pj):
        try:
            with open(pj, encoding="utf-8", errors="ignore") as f:
                d = json.load(f)
            deps = {**d.get("dependencies", {}), **d.get("devDependencies", {})}
        except Exception:
            pass
    if "next" in deps:
        return "next", deps
    if os.path.exists(os.path.join(root, "manifest.json")) or any(os.path.exists(os.path.join(root, p, "manifest.json")) for p in ("src", "extension", "public")):
        return "chrome-ext", deps
    if "electron" in deps:
        return "electron", deps
    if "react" in deps:
        return "react", deps
    if any(os.path.exists(os.path.join(root, f)) for f in ("index.html",)):
        return "html", deps
    return "unknown", deps

def iter_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for fn in filenames:
            ext = os.path.splitext(fn)[1].lower()
            if ext in ALL_EXT and not fn.endswith((".d.ts", ".min.js", ".min.css")):
                yield os.path.join(dirpath, fn)

class Detector:
    def __init__(self, root, stack, deps, ignore):
        self.root = root
        self.stack = stack
        self.deps = deps
        self.ignore = ignore
        self.findings = []
        self.stats = Counter()
        self.has_token_system = False
        self.has_theme_color = False
        self.has_color_scheme = False
        self.has_reduced_motion_global = False
        self.file_count = 0
        self.is_bilingual = any(k in deps for k in ("next-intl", "i18next", "react-i18next", "next-i18next", "@lingui/core", "vue-i18n")) or \
            any(os.path.isdir(os.path.join(root, d)) for d in ("locales", "_locales", "src/locales", "src/i18n", "i18n", "messages"))

    # ---------- helpers ----------
    def add(self, rule, sev, cat, path, line, snip, fix):
        r = rel(path, self.root)
        for ig in self.ignore:
            if ig.get("rule") not in (None, rule):
                continue
            if ig.get("glob") and not fnmatch.fnmatch(r, ig["glob"]):
                continue
            if ig.get("pattern") and not re.search(ig["pattern"], snip or ""):
                continue
            self.stats["ignored"] += 1
            return
        self.findings.append({"id": rule, "severity": sev, "category": cat, "file": r, "line": line, "snippet": snip, "fix": fix})

    @staticmethod
    def read(path):
        with open(path, encoding="utf-8", errors="ignore") as f:
            return f.read()

    # ---------- pre-pass ----------
    def prepass(self, files):
        for p in files:
            ext = os.path.splitext(p)[1].lower()
            t = self.read(p)
            if HEBREW_RE.search(t):
                self.stats["hebrew_files"] += 1
            if ext in CSS_EXT:
                if len(re.findall(r"^\s*--[\w-]+\s*:", t, re.M)) >= 8 or "@theme" in t:
                    self.has_token_system = True
                if "color-scheme" in t:
                    self.has_color_scheme = True
                if "prefers-reduced-motion" in t:
                    self.has_reduced_motion_global = True
            if "theme-color" in t or "themeColor" in t:
                self.has_theme_color = True
            if "color-scheme" in t:
                self.has_color_scheme = True

    # ---------- per-file ----------
    def scan(self, path):
        ext = os.path.splitext(path)[1].lower()
        t = self.read(path)
        self.file_count += 1
        lines = t.split("\n")
        name = os.path.basename(path).lower()
        if ext in CSS_EXT:
            self.scan_css(path, t, lines)
            return
        is_markup = ext in MARKUP_EXT
        token_file = bool(re.search(r"token|theme|palette|colou?rs|brand|icons", name))
        rpath = rel(path, self.root)
        infra_file = bool(re.search(r"(^|/)(desktop|electron|scripts|build|installer|config)/|\.config\.|splash\.html|main\.js$|preload\.js$", rpath))
        is_skeleton = bool(re.search(r"loading\.tsx$|skeleton", rpath))

        # ---- line rules ----
        physical, logical = 0, 0
        tiny = []
        sm_count = md_count = 0
        for i, ln in enumerate(lines, 1):
            if "rtl-exception" in ln or "eslint-disable" in ln:
                continue
            quoted = ('"' in ln or "'" in ln or "`" in ln)
            if is_markup or quoted:
                for m in PHYSICAL_TOKEN_RE.finditer(ln):
                    tok = m.group(0)
                    if tok.startswith("rtl:") or "rtl:" in ln[:m.start()][-6:]:
                        continue
                    if re.search(r"(?:left|right)-1/2\b", tok):
                        continue  # centering idiom
                    if tok.startswith("space-x") and "space-x-reverse" in ln:
                        continue
                    physical += 1
                    self.add("rtl.physical-class", "high", "rtl", path, i, ln.strip()[:110],
                             "החלף ל-logical: ml→ms, mr→me, pl→ps, pr→pe, left→start, right→end, text-left/right→text-start/end, rounded-l/r→rounded-s/e, border-l/r→border-s/e, space-x→gap (או eslint-plugin-rtl-friendly --fix)")
                logical += len(LOGICAL_TOKEN_RE.findall(ln))
                if "flex-row-reverse" in ln and "rtl:" not in ln:
                    self.add("rtl.row-reverse", "medium", "rtl", path, i, ln.strip()[:110], "dir=rtl כבר הופך flex; row-reverse = היפוך כפול. השתמש flex-row ותן לדפדפן להפוך")
                if re.search(r"(?<![\w-])-?translate-x-(?!1/2)", ln) and "rtl:" not in ln:
                    self.add("rtl.translateX-anim", "medium", "rtl", path, i, ln.strip()[:110], "translateX לא הופך ב-RTL — הוסף rtl:-translate-x-* או השתמש ב-:dir(rtl) עם משתנה כיוון")
                if DIRECTIONAL_ICON_RE.search(ln) and not re.search(r"rtl:|scale-x|DirectionalIcon|rtl-exception|^\s*import|ArrowLeftRight", ln):
                    self.add("rtl.icon-directional", "medium" if self.is_bilingual else "low", "rtl", path, i, ln.strip()[:110],
                             "אייקון כיווני (חץ/chevron): ב-RTL 'הבא' מצביע שמאלה. באפליקציה דו-לשונית — rtl:-scale-x-100 / DirectionalIcon; בחד-לשונית עברית — לוודא שהכיוון הפיזי נכון")
                if re.search(r"(?<![\w-])(?:h-screen|min-h-screen)(?![\w-])|100vh", ln) and "dvh" not in ln:
                    self.add("resp.h-screen", "medium", "responsive", path, i, ln.strip()[:110], "השתמש h-dvh / min-h-dvh (100dvh) — שורת הכתובת במובייל מכסה vh")
                for m in TINY_FONT_RE.finditer(ln):
                    if float(m.group(1)) <= 11:
                        tiny.append(i)
                for m in FIXED_W_RE.finditer(ln):
                    if int(m.group(1)) > 360:
                        self.add("resp.fixed-px-width", "medium", "responsive", path, i, ln.strip()[:110], "רוחב קבוע > 360px שובר מובייל — w-full max-w-[Npx]")
                if re.search(r"(?<![\w-])sm:", ln): sm_count += 1
                if re.search(r"(?<![\w-])(?:md|lg|xl|2xl):", ln): md_count += 1
                if re.search(r"(?<![\w-])outline-none(?![\w-])|outline:\s*(?:none|0)", ln) and not re.search(r"focus-visible|ring-", ln):
                    if re.search(r"focus:(?:border|bg|shadow|text)", ln):
                        self.add("a11y.outline-none", "low", "a11y", path, i, ln.strip()[:110], "outline-none עם focus:border בלבד — שינוי גבול הוא אינדיקציה חלשה (3:1?). עדיף focus-visible:ring-2")
                    else:
                        self.add("a11y.outline-none", "high", "a11y", path, i, ln.strip()[:110], "outline-none בלי תחליף = אין focus ring. הוסף focus-visible:ring-2 focus-visible:ring-offset-2")
                if re.search(r"(?<![\w-])transition-all(?![\w-])|transition:\s*all", ln):
                    self.add("a11y.transition-all", "low", "a11y", path, i, ln.strip()[:110], "transition: all יקר ולא צפוי — פרט: transition-colors / transition-transform")
                if re.search(r"\bautoFocus\b", ln):
                    self.add("a11y.autofocus-mobile", "low", "a11y", path, i, ln.strip()[:110], "autoFocus במובייל פותח מקלדת ומזיז layout — הפעל רק בדסקטופ / אחרי אינטראקציה")
                if RAW_PALETTE_RE.search(ln) and self.has_token_system and not token_file:
                    self.add("design.raw-palette", "low", "design", path, i, ln.strip()[:110], "פלטת Tailwind גולמית כשיש token system — השתמש ב-token (text-ink-dim, bg-surface-2)")
            if is_markup and not token_file and not infra_file and "href=" not in ln and "token-exception" not in ln and "R2 exception" not in ln and "url(" not in ln:
                for m in HEX_RE.finditer(ln):
                    self.add("design.hex-in-tsx", "medium", "design", path, i, ln.strip()[:110], "צבע קשיח בקומפוננט — העבר ל-token ב-globals.css (var(--x)) או סמן token-exception עם סיבה")
            if ALERT_RE.search(ln) and "console." not in ln and not re.search(r"\bfunction\s+(?:alert|confirm|prompt)|const\s+(?:alert|confirm|prompt)", ln) and not re.match(r"\s*(?://|\*|/\*)", ln):
                self.add("ux.alert-confirm", "medium", "ux", path, i, ln.strip()[:110], "window.alert/confirm חוסמים ולא נגישים — dialog/undo-toast של המערכת")
            if DATE_RE.search(ln):
                self.add("ux.hardcoded-date-format", "low", "ux", path, i, ln.strip()[:110], "פורמט תאריך/מספר דרך Intl.DateTimeFormat('he-IL') / Intl.NumberFormat('he-IL')")
            if FONT_DEFAULT_RE.search(ln) and re.search(r"\b(?:Inter|Roboto|Arial)\b", ln):
                self.add("design.font-default", "medium", "design", path, i, ln.strip()[:110], "Inter/Roboto/Arial כגופן יחיד = anti-slop. לעברית: Assistant/Heebo/Rubik/Noto Sans Hebrew — גופן ראשי אחד + משני לכל היותר")

        self.stats["physical_classes"] += physical
        self.stats["logical_classes"] += logical
        if tiny:
            self.add("resp.tiny-font", "medium", "responsive", path, tiny[0], f"{len(tiny)}× text-[≤11px] (שורות {', '.join(map(str, tiny[:8]))}{'…' if len(tiny) > 8 else ''})",
                     "טקסט ≤ 11px לא קריא במובייל — סולם: text-xs (12) לcaption, text-sm (14) למשני, text-base (16) לגוף")
        if is_markup and sm_count >= 5 and md_count == 0 and re.search(r"client|page|layout|shell|grid|list|dashboard", name):
            self.add("resp.no-md-lg", "low", "responsive", path, 1, f"{sm_count}× sm: ו-0× md:/lg:/xl:", "אין מצב טאבלט/דסקטופ — layout שמשתנה צריך md: (768) ו-lg:/xl: (1024+), לא רק sm:")
        if is_markup and re.search(r"\bfixed\b[^\n]*\bbottom-0\b|\bbottom-0\b[^\n]*\bfixed\b", t) and "safe-area" not in t:
            m = re.search(r"\bfixed\b[^\n]*\bbottom-0\b|\bbottom-0\b[^\n]*\bfixed\b", t)
            self.add("resp.safe-area", "medium", "responsive", path, line_of(t, m.start()), snippet(t, m.start()), "fixed bottom בלי env(safe-area-inset-bottom) — מוסתר ע\"י home indicator ב-iPhone")
        if is_markup and len(lines) > 800:
            self.add("code.giant-client", "low", "health", path, 1, f"{len(lines)} שורות", "קובץ UI > 800 שורות — פרק ל-sections/קומפוננטים (settings → טאבים)")
        inline = t.count("style={{")
        if inline > 20:
            self.add("code.inline-style-count", "info", "health", path, 1, f"{inline}× style={{{{", "הרבה inline styles — העבר ל-classes/tokens אלא אם זה --card-color דינמי")

        if not is_markup:
            return

        # ---- tag rules (multiline) ----
        for m in TAG_INPUT_RE.finditer(t):
            tag = m.group(0)
            if "rtl-exception" in tag:
                continue
            typ = re.search(r"\btype\s*=\s*[\"'](\w+)[\"']", tag)
            typ = typ.group(1) if typ else "text"
            if typ == "hidden" or re.search(r"aria-hidden|className=\"hidden\"|tabIndex=\{-1\}|sr-only", tag):
                continue
            before = t[max(0, m.start() - 500):m.start()]
            inside_label = before.rfind("<label") > before.rfind("</label>")
            has_dir = re.search(r"\bdir\s*=", tag)
            if typ in ("tel", "email", "url", "password") and not (has_dir and re.search(r"dir\s*=\s*[\"']ltr", tag)):
                self.add("rtl.input-dir", "high", "rtl", path, line_of(t, m.start()), snippet(t, m.start()), f'input type="{typ}" חייב dir="ltr" (+ text-start, inputMode, autoComplete) — אחרת הספרות/אותיות מתהפכות')
            elif typ in ("text", "search") and not has_dir and self.stats["hebrew_files"]:
                self.add("rtl.free-input-no-auto", "low", "rtl", path, line_of(t, m.start()), snippet(t, m.start()), 'קלט חופשי → dir="auto" כדי שמילה באנגלית לא תקפוץ לצד הלא נכון')
            if typ not in ("submit", "button", "checkbox", "radio", "range", "file", "color") and not inside_label and not re.search(r"aria-label(?:ledby)?\s*=|\bid\s*=|\btitle\s*=", tag):
                self.add("a11y.input-no-label", "medium", "a11y", path, line_of(t, m.start()), snippet(t, m.start()), "שדה בלי id (ל-label htmlFor) ובלי aria-label — קורא מסך לא יודע מה זה; placeholder ≠ label")
            if typ in ("tel", "email") and not re.search(r"autoComplete|autocomplete", tag):
                self.add("ux.form-no-autocomplete", "low", "forms", path, line_of(t, m.start()), snippet(t, m.start()), 'הוסף autoComplete="tel"/"email" + inputMode — מילוי אוטומטי ומקלדת נכונה במובייל')
        for m in TAG_TEXTAREA_RE.finditer(t):
            if not re.search(r"\bdir\s*=", m.group(0)) and self.stats["hebrew_files"]:
                self.add("rtl.free-input-no-auto", "low", "rtl", path, line_of(t, m.start()), snippet(t, m.start()), 'textarea → dir="auto"')
        for m in TAG_IMG_RE.finditer(t):
            if not re.search(r"\balt\s*=", m.group(0)):
                self.add("a11y.img-no-alt", "high", "a11y", path, line_of(t, m.start()), snippet(t, m.start()), 'כל תמונה עם alt (דקורטיבית: alt="")')
        for m in TAG_BUTTON_RE.finditer(t):
            attrs, inner = m.group(1), m.group(2)
            text = re.sub(r"<[^>]+>", "", inner)
            text = re.sub(r"\{\s*[\"'`]\s*[\"'`]\s*\}|\{\s*\"\s\"\s*\}", "", text)
            has_expr = bool(re.search(r"\{[^}]*\}", text))
            text = re.sub(r"\{[^}]*\}", "", text).strip()
            if not text and not has_expr and not re.search(r"aria-label(?:ledby)?\s*=|\btitle\s*=", attrs) and "children" not in attrs:
                self.add("a11y.icon-button-no-label", "high", "a11y", path, line_of(t, m.start()), snippet(t, m.start()), 'כפתור-אייקון בלי טקסט → aria-label="…" בעברית (+ title ל-tooltip)')
        for m in TAG_CLICKY_RE.finditer(t):
            tag, attrs = m.group(1), m.group(2)
            if re.search(r"role\s*=\s*[\"'](?:button|link|tab|menuitem|option|checkbox|switch)", attrs) and re.search(r"tabIndex|onKeyDown|onKeyUp", attrs):
                continue
            if re.search(r"inset-0|role\s*=\s*[\"']dialog|aria-modal|stopPropagation", attrs) or "stopPropagation" in t[m.end():m.end() + 80]:
                continue  # backdrop click-to-close / dialog container — legit (Esc + close button are checked live)
            self.add("a11y.div-onclick", "high", "a11y", path, line_of(t, m.start()), snippet(t, m.start()), f"<{tag} onClick> לא נגיש במקלדת/קורא מסך — <button type=\"button\"> לפעולה, <a href>/<Link> לניווט (או role+tabIndex+onKeyDown אם חייבים)")
        # empty state heuristic — only dynamic arrays (not [1,2,3].map / Array.from), not skeletons/thin pages
        dyn_maps = [mm for mm in re.finditer(r"\.map\(\s*\(?\s*\w+[^)]*\)?\s*=>\s*(?:\(|<)", t)
                    if not re.search(r"\]\s*$|Array\.from\([^)]*\)\s*$|Array\(\d+\)\)?\s*$|\.fill\([^)]*\)\s*$", t[max(0, mm.start() - 60):mm.start()])]
        if dyn_maps and not is_skeleton and len(lines) > 60 and not re.search(r"length\s*(?:===|==|!==|!=|>|<|>=)\s*\d|\.length\s*\?|!\w+(?:\.\w+)*\.length|\.length\s*&&|\bisEmpty|\bempty\b|EmptyState|אין\s|לא נמצאו|עדיין אין", t):
            self.add("ux.no-empty-state", "medium", "ux", path, 1, "⚠️ heuristic: .map( ב-JSX בלי טיפול ב-length===0/EmptyState בקובץ", "רשימה בלי empty state — הסבר + CTA כשאין פריטים (ux-flows U-1)")

    def scan_css(self, path, t, lines):
        name = os.path.basename(path).lower()
        for i, ln in enumerate(lines, 1):
            if "rtl-exception" in ln:
                continue
            if CSS_PHYSICAL_RE.search(ln) and ":dir(" not in ln and "[dir=" not in ln:
                self.add("rtl.physical-css", "high", "rtl", path, i, ln.strip()[:110], "margin/padding/border-left|right → -inline-start|end; left/right → inset-inline-start|end; text-align:left|right → start|end")
            if re.search(r"outline\s*:\s*(?:none|0)\b", ln) and ":focus-visible" not in t:
                self.add("a11y.outline-none", "high", "a11y", path, i, ln.strip()[:110], "outline:none בלי :focus-visible תחליף")
            if re.search(r"transition\s*:\s*all\b", ln):
                self.add("a11y.transition-all", "low", "a11y", path, i, ln.strip()[:110], "פרט מאפיינים במקום all")
            if re.search(r"translateX\(", ln) and ":dir(" not in ln and "--dir" not in ln and "[dir=" not in t:
                self.add("rtl.translateX-anim", "medium", "rtl", path, i, ln.strip()[:110], "translateX לא הופך ב-RTL — משתנה --dir + :dir(rtl)")
            if FONT_DEFAULT_RE.search(ln):
                self.add("design.font-default", "medium", "design", path, i, ln.strip()[:110], "גופן ברירת מחדל (Inter/Roboto/Arial) — בחר גופן עברי מובחן")
        if re.search(r"@keyframes|animation\s*:", t) and "prefers-reduced-motion" not in t and not self.has_reduced_motion_global:
            self.add("a11y.no-reduced-motion", "medium", "a11y", path, 1, "יש אנימציות בלי @media (prefers-reduced-motion: reduce)", "הוסף בלוק reduced-motion שמבטל/מקצר אנימציות")
        # token system checks (globals / theme files)
        if re.search(r"^\s*:root\s*\{", t, re.M):
            root_block = self._block(t, r":root\s*\{")
            root_tokens = {m.group(1): m.group(2) for m in re.finditer(r"--([\w-]+)\s*:\s*([^;]+);", root_block)}
            colorish = {k for k, v in root_tokens.items() if re.search(r"#[0-9a-fA-F]{3,8}\b|rgba?\(|hsla?\(|oklch\(|color-mix\(|\bwhite\b|\bblack\b", v)}
            dark_text = " ".join(self._block(t, pat) for pat in [r"\[data-theme=\"?dark\"?\]\s*\{", r"prefers-color-scheme:\s*dark\)\s*\{"])
            if dark_text.strip():
                dark_tokens = set(re.findall(r"--([\w-]+)\s*:", dark_text))
                missing = sorted(colorish - dark_tokens)
                for tok in missing:
                    self.add("design.dark-token-missing", "medium", "design", path, self._line_of_token(t, tok), f"--{tok} מוגדר ב-:root אבל לא בבלוק dark", "כל token צבע חייב ערך dark (R4: :root + prefers-color-scheme + [data-theme=dark])")
            if "@theme" in t:
                theme_block = self._block(t, r"@theme[^{]*\{")
                mapped = set(re.findall(r"var\(--([\w-]+)\)", theme_block))
                for tok in sorted(colorish - mapped):
                    if tok.endswith(("-ink", "-text", "-soft")) or tok in mapped:
                        continue
                    self.add("design.theme-map-missing", "low", "design", path, self._line_of_token(t, tok), f"--{tok} לא ממופה ב-@theme (אין bg-{tok}/text-{tok})", "הוסף --color-<tok>: var(--<tok>) ל-@theme inline")
        if name in ("globals.css", "global.css", "app.css", "index.css", "style.css", "styles.css", "main.css"):
            if not self.has_color_scheme:
                self.add("design.color-scheme-missing", "low", "design", path, 1, "אין color-scheme", "html { color-scheme: light dark } — scrollbars/inputs/select נכונים ב-dark (Windows)")

    @staticmethod
    def _block(t, start_pat):
        out = []
        for m in re.finditer(start_pat, t):
            depth, i = 1, m.end()
            while i < len(t) and depth:
                if t[i] == "{": depth += 1
                elif t[i] == "}": depth -= 1
                i += 1
            out.append(t[m.end():i])
        return "\n".join(out)

    @staticmethod
    def _line_of_token(t, tok):
        m = re.search(r"--" + re.escape(tok) + r"\s*:", t)
        return line_of(t, m.start()) if m else 1

    # ---------- project-level ----------
    def project_rules(self, files):
        hebrew = self.stats["hebrew_files"] > 0
        html_roots = [p for p in files if os.path.basename(p).lower() in ("layout.tsx", "index.html", "popup.html", "options.html", "app.html", "index.astro", "app.vue")]
        for p in html_roots:
            t = self.read(p)
            m = re.search(r"<html\b[^>]*>", t, re.S)
            if not m:
                continue
            tag = m.group(0)
            if hebrew and not re.search(r"\bdir\s*=", tag):
                self.add("rtl.html-dir", "blocker", "rtl", p, line_of(t, m.start()), tag[:110], '<html lang="he" dir="rtl"> (או דינמי לפי locale) — בלי זה logical properties, :dir() וקוראי מסך לא עובדים')
            elif hebrew and re.search(r"dir\s*=\s*[\"']ltr[\"']", tag):
                self.add("rtl.html-dir", "high", "rtl", p, line_of(t, m.start()), tag[:110], "dir=ltr קבוע באפליקציה עברית")
            if hebrew and not re.search(r"\blang\s*=", tag):
                self.add("a11y.html-lang", "high", "a11y", p, line_of(t, m.start()), tag[:110], 'lang="he" חסר — קורא מסך יקרא עברית במבטא אנגלי (WCAG 3.1.1)')
            if self.stack in ("html", "chrome-ext", "electron", "react") and "<head" in t and "viewport" not in t:
                self.add("resp.missing-viewport-meta", "blocker", "responsive", p, 1, "אין <meta name=viewport>", '<meta name="viewport" content="width=device-width, initial-scale=1"> (בלי user-scalable=no)')
        if self.stack in ("next", "react", "html", "electron") and not self.has_theme_color:
            self.add("design.theme-color-missing", "low", "design", self.root, 0, "אין theme-color", "<meta name=theme-color> (Next: metadata.themeColor) תואם רקע לכל theme")
        if not self.has_reduced_motion_global and any(os.path.splitext(p)[1].lower() in CSS_EXT for p in files):
            pass  # reported per css file
        if self.stack == "next":
            if "eslint-plugin-rtl-friendly" not in self.deps and hebrew:
                self.add("tooling.no-rtl-lint", "medium", "health", self.root, 0, "eslint-plugin-rtl-friendly לא מותקן", "npm i -D eslint-plugin-rtl-friendly + rtlFriendly.configs.recommended ב-eslint.config.mjs → --fix מתקן classes פיזיים")
            if not any(k in self.deps for k in ("@axe-core/playwright", "axe-core", "jest-axe", "vitest-axe")):
                self.add("tooling.no-a11y-test", "low", "health", self.root, 0, "אין axe בבדיקות", "npm i -D @playwright/test @axe-core/playwright — סריקת a11y אוטומטית ב-CI")
            if "eslint-plugin-jsx-a11y" not in self.deps and "eslint-config-next" not in self.deps:
                self.add("tooling.no-jsx-a11y", "low", "health", self.root, 0, "אין eslint-plugin-jsx-a11y", "eslint-config-next כולל jsx-a11y; אחרת התקן ידנית")

def load_ignore(path):
    if path and os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f).get("ignore", [])
        except Exception as e:
            print(f"warn: ignore file unreadable: {e}", file=sys.stderr)
    return []

def to_markdown(result):
    s = result["summary"]
    out = [f"# detect.py — {result['root']}", "",
           f"stack: `{result['stack']}` · files: {s['files_scanned']} · hebrew files: {s['hebrew_files']} · physical/logical classes: {s['physical_classes']}/{s['logical_classes']} · ignored: {s['ignored']}", "",
           "| severity | count |", "|---|---|"]
    for sev in ("blocker", "high", "medium", "low", "info"):
        out.append(f"| {sev} | {s['by_severity'].get(sev, 0)} |")
    out += ["", "| rule | severity | count | files |", "|---|---|---|---|"]
    for rid, c in sorted(s["by_rule"].items(), key=lambda kv: (SEV_ORDER[s["rule_severity"][kv[0]]], -kv[1])):
        out.append(f"| `{rid}` | {s['rule_severity'][rid]} | {c} | {s['rule_files'][rid]} |")
    out += ["", "## Top findings (blocker/high, first 40)", ""]
    for f in [x for x in result["findings"] if x["severity"] in ("blocker", "high")][:40]:
        out.append(f"- `{f['file']}:{f['line']}` - [{f['category']}] {f['id']} — {f['snippet']}")
    return "\n".join(out)

def main():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root")
    ap.add_argument("--out", default=None, help="JSON output path (default: <root>/.claude/upgrade/detect.json)")
    ap.add_argument("--stack", default="auto")
    ap.add_argument("--ignore", default=None, help="detect-ignore.json (default: <root>/.claude/upgrade/detect-ignore.json)")
    ap.add_argument("--md", action="store_true", help="print markdown summary to stdout")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    if not os.path.isdir(root):
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 1
    stack, deps = detect_stack(root) if a.stack == "auto" else (a.stack, detect_stack(root)[1])
    ignore = load_ignore(a.ignore or os.path.join(root, ".claude", "upgrade", "detect-ignore.json"))
    files = list(iter_files(root))
    d = Detector(root, stack, deps, ignore)
    d.prepass(files)
    for p in files:
        try:
            d.scan(p)
        except Exception as e:
            print(f"warn: {rel(p, root)}: {e}", file=sys.stderr)
    d.project_rules(files)
    findings = sorted(d.findings, key=lambda f: (SEV_ORDER[f["severity"]], f["id"], f["file"], f["line"]))
    by_sev = Counter(f["severity"] for f in findings)
    by_rule = Counter(f["id"] for f in findings)
    rule_files = {rid: len({f["file"] for f in findings if f["id"] == rid}) for rid in by_rule}
    rule_sev = {f["id"]: f["severity"] for f in findings}
    by_cat = Counter(f["category"] for f in findings)
    result = {
        "root": root, "stack": stack,
        "summary": {
            "files_scanned": d.file_count, "hebrew_files": d.stats["hebrew_files"],
            "physical_classes": d.stats["physical_classes"], "logical_classes": d.stats["logical_classes"],
            "ignored": d.stats["ignored"], "by_severity": dict(by_sev), "by_category": dict(by_cat),
            "by_rule": dict(by_rule), "rule_files": rule_files, "rule_severity": rule_sev,
            "has_token_system": d.has_token_system,
        },
        "findings": findings,
    }
    out = a.out or os.path.join(root, ".claude", "upgrade", "detect.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    if a.md:
        print(to_markdown(result))
    elif not a.quiet:
        print(f"detect.py: {stack} · {d.file_count} files · " + " · ".join(f"{k}={v}" for k, v in sorted(by_sev.items(), key=lambda kv: SEV_ORDER[kv[0]])) + f" → {out}")
    return 2 if (by_sev.get("blocker") or by_sev.get("high")) else 0

if __name__ == "__main__":
    sys.exit(main())

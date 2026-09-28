---
name: local-designer
description: Global, project-independent design skill that produces marketing assets entirely locally - SVG/HTML composed and rendered with sharp and headless Chrome, no paid generative API, no per-image cost. Reads brand identity (colors, font, logo) from the project's own files first; if the brand already exists in Bloom (trybloom.ai), it can pull the profile from there read-only (get_brand/list_brands), never generating images or spending credits. Trigger on - design this, create an image/banner/post/story, compress these images, check the brand colors for X, show me a design example, marketing ad, graphic for the site.
---

# Local Designer — a global, free design skill

A global (not project-specific) skill for producing marketing content/visual assets for any
business or tool, entirely locally and for free. Different from a Bloom-based skill: this never
calls Bloom's paid `generate_image`/`edit_image`/`create_brand_edit` — so it never spends credits.
If Bloom is connected and a Brand session already exists for the business, it can read from it
(colors/font/logo/tone) as an extra data source — read-only, never generation.

Pipeline: brief → brand → copy → design → export → ready assets.

## Step 0 - discovering tools (only if reading brand info from Bloom)

If the user wants to check/pull brand details from Bloom (not generate an image!): search with
`ToolSearch` for a distinctive keyword like `list_brands` to discover the real prefix for this
install (`mcp__<hash>__<action>`), then also load `get_brand`. **Do not load or use**
`generate_image`, `edit_image`, `create_brand_edit`, `apply_brand_edit`, or any other
credit-spending tool — they're out of scope for this skill. If the user wants actual AI generation
through Bloom, that's a separate, explicit, deliberate action they need to ask for — always check
and report the credit balance with `check_credits` first before even suggesting that path.

## Step 1 - brand

Priority order for the brand identity source:
1. **Local project files** — an existing `brand-kit.json`/`brand/` folder, or a real existing
   asset folder (logo/backgrounds/elements) the user already has. **Always prefer and check these
   first** — don't invent colors/logo when real assets already exist.
2. **Bloom, read-only** — if local files are missing or incomplete, and Bloom is connected:
   `list_brands` (filter by `url` if known) to find an existing Brand session, then `get_brand` to
   pull the profile (colors/font/logo/tone/guidance). Save it to a local file (`brand-kit.json` or
   similar) so the next run doesn't need to ask again.
3. If neither exists — stop and ask the user to provide one; never invent it.

## Step 2 - copy

Marketing text that goes on the asset: if the project has a dedicated writing skill/agent, brief
it fully (channel, topic, audience) and use its output rather than writing copy yourself when a
dedicated tool exists. Otherwise write it yourself in plain, natural language — no connecting
hyphens as filler, no emojis, no inflated promises. For RTL languages: right-aligned, `dir="rtl"`,
check punctuation isn't reversed.

## Step 3 - design

Build SVG/HTML with the brand's colors, font, and real logo (not AI-generated when a real asset is
available), and render it with `sharp` (Node) or headless Chrome (screenshotting HTML). This gives
exact control over text rendering — especially important for RTL scripts, which generative image
models frequently distort.

## Step 4 - export

- Export to every needed format (web/social) — WebP/AVIF/JPG, compressed under a size cap, plus
  the PNG source.
- A `meta.json` per asset: alt text, dimensions, an LQIP preview if relevant.
- Folder convention: `assets/<YYYY-MM-DD>_<slug>/{source,web,social}/`.

## Guardrails - don't skip these

1. **Publishing anywhere live (a site, a social account) only after explicit approval.** Local
   export/processing needs no approval.
2. Logo — never stretched or rotated, keep its safe margin (commonly 8%).
3. Text-over-background contrast ≥4.5:1 (WCAG AA) — if it fails, fix it (an overlay or a different
   color), don't ignore it or report "done" without checking.
4. RTL — right-aligned, no reversed punctuation.
5. No asset without alt text.
6. Check for existing similar assets before producing a new one from the same brief — don't
   regenerate from scratch when something close already exists and could be updated instead.
7. **Never call a credit-spending Bloom tool** (generate/edit/brand-edit) unless the user
   explicitly asked for that as a separate, deliberate action — it's out of scope for this skill.

## Output

For each run: a table of files produced (format, dimensions, size), which brand-identity source
was used (local files vs. Bloom read-only), alt-text and contrast status, and a reminder of
anything missing before calling it done.

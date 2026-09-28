---
name: bloom-designer
description: Global, project-independent design skill that wraps the Bloom (trybloom.ai) MCP connection - on-brand image/SVG/video/audio generation and editing for any brand you manage there. Wraps the real MCP tools (onboard_brand, generate_image, edit_image, create_brand_edit, etc.) in a safe workflow that respects credits. Trigger on - design this with Bloom, generate a branded image, generate_image, update the brand identity in Bloom, how many Bloom credits do I have.
---

# Bloom Designer — a global designer via Bloom AI

A global (not project-specific) skill that drives the Bloom (trybloom.ai) MCP connection in any conversation, for
any brand you manage there - not tied to one project or client. Different from a local/offline design workflow
(hand-rolled scripts, Sharp, headless Chrome): this wraps an external paid SaaS with real credits.

## Step 0 - discover the tools

Bloom's MCP tools are registered under a random per-install prefix (`mcp__<hash>__<action>`) that can differ
between environments. At the start of a session:

1. Search with `ToolSearch` for a distinctive keyword, e.g. `onboard_brand` (not `select:`) — this returns the
   full tool name with the correct prefix for this install.
2. Load the rest of the relevant tools in one call with
   `select:<prefix>__list_brands,<prefix>__get_brand,<prefix>__list_workspaces,<prefix>__check_credits,<prefix>__generate_image,<prefix>__edit_image,<prefix>__get_image,<prefix>__list_images,<prefix>__search_user_images,<prefix>__upload_image,<prefix>__create_upload_urls,<prefix>__resize_image,<prefix>__remove_background,<prefix>__vectorize_image,<prefix>__generate_svg,<prefix>__generate_audio,<prefix>__generate_video,<prefix>__find_reference_ads,<prefix>__create_brand_edit,<prefix>__continue_brand_edit,<prefix>__apply_brand_edit,<prefix>__discard_brand_edit,<prefix>__get_brand_edit,<prefix>__list_brand_versions,<prefix>__upload_brand_font,<prefix>__delete_brand,<prefix>__delete_images,<prefix>__view_files,<prefix>__get_account`
3. If `ToolSearch` finds nothing at all, Bloom isn't connected in this session. Tell the user to connect it
   (claude.ai connector settings, or `/mcp` in an interactive session) and stop.

Every Bloom tool call requires `llm_model` — pass the model you're actually running as (e.g. `claude-sonnet-5`).
**Never guess** — pass `"unknown"` if you don't know it with certainty.

## Step 1 - find or create the Brand

- `list_workspaces` once if it's unclear which workspace to use (usually the personal one, the default when
  `workspace_id` is omitted).
- `list_brands` (optionally filtered by `url`) to check whether a Brand session for the target brand already
  exists — **always check before creating a new one**, to avoid duplicates.
- If none exists, `onboard_brand` from `url` (a website) or `sources` (website + Instagram + files, up to 30).
  This builds a Brand Skill (automatic logo/color/font detection). Use `idempotency_key` if a duplicate attempt
  is plausible (e.g. after a timeout).
- After creation the status is `"analyzing"` — call `get_brand` again with `wait: true` until it's ready. Keep
  the `brand_session_id` — every following call needs it.
- **Report back to the user** the detected brand name and a short profile summary (colors/font) before
  generating anything, so they can confirm it's the right brand.

## Step 2 - credits, always before a batch

Bloom is a paid, credit-metered service (2K = 1 credit per image, 4K = 2 credits, each variant counted
separately). **Before any request for more than 2-3 images** (or whenever the user mentions a limited credit
balance), call `check_credits` (needs a `workspace_id` from `list_workspaces`) and report the balance before
continuing. If the balance is lower than what's requested, stop and ask how to proceed (fewer images? lower
resolution? `fast` model instead of `pro`?) instead of burning credits on a request that fails partway through.

## Step 3 - check for existing assets before generating from scratch

Before `generate_image` from nothing, consider `search_user_images` to find relevant images already in the
Brand Library — passing them as `reference_image_ids` measurably improves the result and keeps things visually
consistent. This mirrors a general good practice: always check for real existing assets before generating new
ones from scratch, whether that's a Brand Library search here or a local assets folder elsewhere.

## Step 4 - generate and edit

- **New image**: `generate_image(prompt, brand_session_id, aspect_ratio?, image_size?, model?, variant_count?, reference_image_ids?)`.
  The prompt should describe content/composition only — Bloom adds the brand's own styling automatically, so
  skip aesthetic filler words like "professional" or "stunning". Returns immediately with pending `image_id`(s);
  each image takes roughly 60-90 seconds.
- **Collecting results**: a single image — `get_image(image_id, wait: true)`. Several at once —
  `list_images(image_ids, wait: true)`.
- **Editing an existing image** (from Bloom or uploaded): `edit_image(image_id, prompt, brand_session_id, ...)` —
  describe only what changes; Bloom preserves everything else. The aspect ratio is locked to the original.
- **Vector/SVG**: `generate_svg`. **Background removal**: `remove_background`. **Resize**: `resize_image`.
  **Vectorize a raster**: `vectorize_image`.
- **Video/audio**: `generate_video` / `generate_audio` — same idea, check the tool's own schema for exact
  parameters (less commonly needed, so not detailed here).
- **A specific/more flexible model**: `list_generation_models` → `get_generation_model` (read its
  `input_schema`) → `generate_image_with_model` — note this path does **not** add brand guidance automatically,
  you need to include it in the prompt/input yourself.
- **Uploading a reference/font**: `upload_image` / `create_upload_urls` (for large files) / `upload_brand_font`.

## Step 5 - updating the brand identity itself (not just one-off content)

When the user wants to change the brand itself (color, font, logo), not just generate a single image:
1. `create_brand_edit(brand_session_id, base_skill_id, change)` — `change` is either `instruction` (free text) or
   `profile` (an exact change: `colors`, `typography`, `primary_logo`, `name`).
2. If the edit asks for more input (interactive), answer with `continue_brand_edit` using the `interaction_id`
   from `get_brand_edit`.
3. **Get explicit user confirmation before `apply_brand_edit`** — this actually changes the active brand, not a
   draft. Show them what will change first.

## Safety and working rules

- **Never assume an LLM model** for `llm_model` — read it from your actual system prompt.
- **Never delete** (`delete_brand`, `delete_images`) without explicit user confirmation — irreversible.
- Every generate/edit call spends real credits — don't rerun the same prompt repeatedly without reason; if a
  result isn't quite right, prefer `edit_image` (a targeted fix, still costs a credit) over regenerating from
  scratch.
- Final outputs (`image_url`) live in Bloom — if you need them locally (e.g. to integrate into a site), download
  and save them with the same convention you'd use for any other design asset: a folder with source + web
  formats + a small metadata file (alt text, dimensions).
- If the task clearly belongs to a project that already has its own local, free design pipeline (real
  logo/brand assets on disk, a local rendering script), consider whether that's enough first, and only reach
  for this real generative/paid path when actual AI image generation is what's needed.

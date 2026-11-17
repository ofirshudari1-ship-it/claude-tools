# Rubric: 10 dimensions x score 1-10, and the definition of Done

A score is given **only on the basis of evidence** (detect.json, browser.json, screenshots, file:line). A dimension that was not checked is marked `❓`, not scored.
Lesson from Anthropic (harness design): an uncalibrated evaluator is too generous. Therefore **the default is 5**, and you move up only with evidence for each step.

## General scale
| Score | Meaning | Example |
|---|---|---|
| 1-3 | Broken / missing: the user hits it in the first minute | a phone number flips, no dark mode at all, div-onClick everywhere |
| 4-6 | Works but unprofessional: partly consistent, has debts | 4:1 physical-to-logical classes, tokens with 60 exceptions, empty states in half the modules |
| 7-8 | Professional: one system, few documented exceptions | 0 high in detect, every route passed 3 viewports, axe <= 2 |
| 9-10 | Excellent: distinctive, polished, checked in every state | an identity recognizable without the logo; full keyboard + screen reader; embedded, managed AI |

## The 10 dimensions
| # | Dimension | Key evidence (what lowers/raises the score) |
|---|---|---|
| 1 | **RTL and Hebrew** | `rtl.*` findings; the mirror test on >= 5 routes; the test string; modals; Hebrew typography |
| 2 | **Responsiveness** | overflow-x at 375/320; targets < 44; inputs < 16px; tablet layout; `dvh`; wide-screen anchoring |
| 3 | **Accessibility** | axe violations per route; Tab pass; focus ring; labels; landmarks; 2.2 criteria; accessibility statement |
| 4 | **Design and brand** | anti-slop list; tokens (hex in code); dark mode in both modes; one design direction; type scale |
| 5 | **UX flows and states** | 4 states for every list/form; URL state; consistent navigation; Undo; onboarding TTFV |
| 6 | **Forms** | labels/autocomplete/inputmode; errors next to the field; Enter; unsaved-changes; does not block typing |
| 7 | **Perceived performance** | skeleton; optimistic UI; console errors; layout shift; images with dimensions; huge client bundle |
| 8 | **Ease of setup and operation** | defaults; grouped settings; connections with status; command bar/quick-add; remembers state |
| 9 | **AI layer** | patterns from the table in config-and-ai; edit before saving; fallback; eval; cost |
| 10 | **UI code health** | files > 800 lines; duplicate components; inline styles; clean lint/tsc; an audit script exists and runs in CI/hook |

## Definition of Done for a project
- **Baseline**: every dimension >= 6 and zero `blocker`.
- **Professional** (the default target): every dimension >= 8, zero `blocker`/`high` in detect, axe <= 2 per route, 0 console errors.
- **Excellent**: every dimension >= 9 + the evaluator confirms the "3 worst things" are Nit only.

## Severity of a single finding
| Tag | Definition | SLA in the plan |
|---|---|---|
| `[Blocker]` | Breaks usage / legal (no `dir=rtl`, no viewport, a form without labels in the main flow) | S1: immediately |
| `[High]` | A regular user hits it in regular use (a phone number flips, target < 32px, hex in 10+ places, div-onClick) | S1-S3 |
| `[Medium]` | Professionalism/consistency (a missing breakpoint, a missing skeleton, slop) | S2-S5 |
| `[Nit]` | Polish (`…`, tabular-nums, shadow) | S4+ or backlog |

## Few-shot calibration for the evaluator
**An example of a correct score (RTL, home-hub before):**
> 100 physical classes vs 24 logical (detect.json), `family-chat-client.tsx:375` `pr-9 pl-3 text-right`, `app-shell.tsx:180` `md:border-l` on a right-side sidebar, `contact/page.tsx` tel input with `dir="ltr"` ✓. Mirror test: sidebar ✓, chat bubbles ✓, close badge at `left-2` ✗ (3 routes). The settings modal opens on the correct side ✓. -> **Score 5**. Not 7: a 4:1 physical ratio means every future change will break something; not 3: nothing is "broken" for the user today because the app is single-language.

**An example of a wrong score (what not to do):**
> "The RTL looks good, the app is dir=rtl and everything is right-aligned. 8/10." No evidence, no file:line, no modal opened, no test string injected. Invalid.

**An example of a contract FAIL:**
> Contract S2-3 "0 findings of `rtl.physical-class` in src/components": detect.json after = 7 findings (`hero-illustration.tsx` x6 with a documented `rtl-exception` ✓, `task-card.tsx:41` `pl-2` ✗ with no comment). -> **FAIL**: one item is not covered.

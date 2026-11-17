# Ease of setup and operation + the AI layer

Sources: impeccable `onboard`/`harden`, Vercel guidelines, STANDARDS §16 (Settings/Update UX), §18.3-18.4, Anthropic `claude-api` skill, home-hub `ai-intent-owner` (SmartAddBar pattern).

## Dimension 8: "easy to set up, easy to operate"

### C-1. Smart defaults: high
The product works **immediately** without touching settings: language from the OS/browser (`navigator.languages`, not IP), theme from `prefers-color-scheme`, time zone/currency from the locale, a sensible default location. Any setting that must be filled in before the first value is delivered is a finding.

### C-2. Settings screen: medium (§16)
- Grouped by topic (General / Appearance / Notifications / Account / Advanced), not a flat list of 40 toggles. A settings file over 800 lines (home-hub: 2,080) should be split into tabs/sections.
- Search within settings if there are more than 15 items.
- Every setting: a label + a one-line explanation + the current value visible; a change is saved **immediately** with a "Saved ✓" confirmation (or one Save button per section), never "requires restart".
- "Restore defaults" per section; settings export/import (JSON) for tools.
- Dangerous actions (delete account, reset data) at the bottom, in red, with a confirm step plus typing a confirmation phrase.

### C-3. Connections and integrations: medium
Every integration (Google Calendar, WhatsApp, API key) shows: connected/not connected status that is clear, a "Test connection" button, last sync date, a readable error ("Token expired, reconnect"), and one-click disconnect. API keys are not shown in full after saving.

### C-4. Install/update (desktop, Chrome extension): medium (§7/§16)
Installer in two languages, correct default location, never overwrites user data. Updates: background check, non-blocking notice, a short "What's new", rollback possible. Chrome extension: minimal permissions, an explained options page.

### C-5. In-product documentation: low
A `?` next to complex settings (inline help), a help page/FAQ linked from the same place on every screen (3.2.6), a README/landing page with the "first 5 minutes".

### C-6. Day-to-day operation: medium
- The most frequent action takes 1 click/keystroke (command bar `Ctrl+K`, FAB, quick-add).
- Keyboard shortcuts on desktop (documented under `?`), aware of non-QWERTY layouts.
- Undo for every frequent action; history/versions for what matters.
- Everything remembers state (filter, tab, window size, columns).

## Dimension 9: the AI layer: where it adds real value

### AI-1. Principle: AI removes friction, it does not add a feature: high
For every module ask: "Where does the user type, classify, search or summarize by hand?" That is where AI belongs. Not a generic "chat with the bot" in a corner.
Patterns that prove value:
| Pattern | Example | Metric |
|---|---|---|
| **Smart add** (free line -> structured entity) | "milk tomorrow 8 am" -> a task with a date | % of adds via smart-add, time to add |
| **Auto classification/tagging** | expense -> category; document -> folder | % of manual corrections (< 10%) |
| **Summarization** | an 80-message family chat -> 3 lines | repeat use |
| **Contextual recommendation** | "You have 3 tasks at the same time, move one?" | acceptance rate |
| **Semantic search** | "the insurance document" | success rate |
| **Vision** | photo of a receipt/plant -> data | accuracy |
| **Proactive digest** | morning: "Today: 2 tasks, weather, what is missing in the fridge" | open rate |

### AI-2. UX of an AI feature: high
- **Input**: a placeholder with an example (Hebrew example: "תזכיר לי לשלם ארנונה ב-1 לחודש" = "Remind me to pay property tax on the 1st of the month"), and voice input (mic) on mobile.
- **While working**: streaming or a skeleton, perceived wait <= 3s; the user can cancel.
- **Result**: always **editable** before saving (AI suggests, the user approves), especially for actions with side effects; a short "why" when relevant.
- **Failure**: a clear manual fallback (Hebrew: "לא הבנתי — הוסף ידנית" = "I didn't understand, add it manually"), never a block; offline = the feature is hidden/disabled with an explanation, not an error.
- **Trust**: do not invent data; mark AI-generated content; a privacy policy stating what is sent to the model.
- **Cost**: cache identical answers, use a small model for classification (Haiku), a large one only for summarization/reasoning; a daily budget; do not call the model on every keystroke (debounce/submit).

### AI-3. Engineering: medium (see the `claude-api` skill for current details)
- Defaults: `claude-sonnet-5` for UI, `claude-haiku-4-5-20251001` for classification/intent, `claude-opus-5-5`/`claude-fable-5-1` for complex summarization.
- Tool use / structured output (JSON schema) for smart-add, not regex over free text.
- A system prompt with user context (family member names, modules, time zone), plus a Hebrew eval set (home-hub: the `intent-eval` skill) that runs on every prompt change.
- Keys only server-side (route handler / edge function), per-user rate limit, call logging (tokens, latency, errors).
- Prompt caching for the system prompt; streaming for responses over 2s.

### AI-4. What not to do: medium
- "AI" as a marketing badge on a deterministic feature.
- An open chat with no defined task (users do not know what to ask); better to show 3-5 suggested prompts in context.
- Blocking the normal flow until the AI answers.
- Sending PII to the model without need.

### Dimension 9 score
1-3: no AI, or a generic chat. 4-6: one AI feature works but has no fallback/editing. 7-8: 2-3 patterns from the table, editable, an eval exists. 9-10: transparent AI embedded in every module, usage metrics, managed cost.

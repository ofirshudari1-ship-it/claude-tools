---
name: secrets-hygiene-check
description: "Zero-secrets check before commit or release: scans source for API keys, tokens, passwords and connection strings, verifies .gitignore and environment-based config. Stops and reports on any real finding. Trigger on: check for secrets, before commit, leaked key worry."
---

# Secrets Hygiene Check

Your standards document defines "zero secrets in code" as a mandatory requirement for every tool and checks it in every audit cycle. This skill runs that same check consistently, without rediscovering it each time. Trigger: before a commit or release, or any worry that a key leaked. Input: the project's source folder. Output: a concise pass/fail report (see step 4).

## Steps

1. **Scan for common secret patterns** with Grep over `src/` / the project's source code (not `node_modules`, `dist`, `build`, `win-unpacked`):
   - API keys (`api[_-]?key`, `sk-`, `AIza`, `ghp_`, long strings mixing letters and digits)
   - Tokens/secrets (`token`, `secret`, `password`, `client_secret`)
   - Connection strings (`mongodb://`, `postgres://`, `Server=...;Password=`)
   - Embedded private keys (`-----BEGIN PRIVATE KEY-----`)
2. **Check `.gitignore`**: confirm it includes `.env`, credential files, and config folders that might hold real secrets in the development environment.
3. **Check how config is actually loaded**: it should use `%APPDATA%` / environment variables / a local, non-versioned config file, not hardcoded paths with sensitive values embedded in code.
4. **Report concisely** (a pass or fail mark per check), in the same style as the existing status table in your standards document, so the result can be fed straight into it or into `<audit folder>/AUDIT-<Tool>.md`.

## Rules

- A finding means quoting file and line, not guessing. If something looks suspicious but is uncertain (for example a string that looks like a key but is actually an example/placeholder), mark it with a warning sign for manual review and do not declare it definitively.
- If a real secret is found in code: report it to the user immediately and take no further actions (commit/release/publish) until they deal with it. Do not delete or replace the secret yourself without explicit approval.

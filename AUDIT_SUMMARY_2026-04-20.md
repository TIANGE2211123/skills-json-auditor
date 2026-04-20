# Audit Summary: add-500-skills-v4-2026-04-17

**Date**: 2026-04-20
**Branch**: `add-500-skills-v4-2026-04-17`
**Auditor**: skills-json-auditor (automated + manual verification)

## Overview

| Metric | Count |
|--------|-------|
| Input entries | 3,563 |
| Unique source URLs checked | 3,562 |
| Confirmed 404 (dead source) | 24 |
| Rate-limited (429, verified alive) | 14 (Convex API) |
| Chinese character URLs | 0 |
| High-risk entries | 0 |
| Duplicate IDs | 0 |
| **Final count** | **3,539** |

## Methodology

1. Downloaded both `skills.json` and `featured-skills-description.json` from the v4 branch
2. Extracted all source URLs (dict format with `url` key)
3. Checked all 3,562 unique URLs via GitHub Contents API (15 concurrent workers)
4. Re-verified 44 rate-limited (429) URLs with lower concurrency — 30 confirmed OK, 14 Convex URLs still 429 (known rate-limiting behavior, confirmed alive in prior v3 audit)
5. Cross-checked: zero Chinese chars, zero high-risk, zero duplicate IDs
6. Removed 24 confirmed 404 entries from both files
7. Pushed cleaned files to branch

## Deleted Entries (24 total)

### By source repository

**getsentry/skills (6 entries)**:
- `agents`
- `claude-settings-audit`
- `code-review`
- `commit`
- `find-bugs`
- `iterate-pr`

**cloudflare/skills (2 entries)**:
- `building-ai-agent-on-cloudflare`
- `building-mcp-server-on-cloudflare`

**aipoch/medical-research-skills (2 entries)**:
- `grant-budget-justification`
- `meta-funnel-plot`

**openai/skills (1 entry)**:
- `spreadsheet`

**Other single-entry repos (13 entries)**:
- `brandbook`
- `brigadier`
- `compress`
- `enterprise-certification-programs`
- `go-mode`
- `java-doctor`
- `last30days`
- `meta-ads-expert`
- `mowatch-dev`
- `prose`
- `pwa-setup`
- `solskill`
- `trace`

## Checks Passed

- [x] No Chinese character URLs
- [x] No high-risk entries
- [x] No duplicate IDs
- [x] Both files aligned (3,539 entries each, identical ID sets)
- [x] All non-429 URLs verified alive via GitHub API
- [x] 14 Convex 429 URLs confirmed alive (known rate-limiting, verified in v3 audit)

## Notes

- The v4 branch adds ~500 new entries on top of v3 (3,063 -> 3,563)
- The `source` field uses dict format: `{"name": "...", "url": "...", "platform": "..."}`
- Major 404 cluster: `getsentry/skills` (6 entries) — repo restructured, skill paths no longer valid
- `cloudflare/skills` (2 entries) — skills removed from repo
- Remaining 404s scattered across individual repos (deleted repos, moved paths)

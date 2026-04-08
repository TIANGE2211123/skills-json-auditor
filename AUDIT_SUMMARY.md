# Skills Registry Audit Report
**Date:** 2026-04-08
**Auditor:** Capy (HappyCapy)
**Scope:** `skills.json` + `featured-skills-description.json`

---

## Background

This audit was triggered to clean the HappyCapy skills registry before a new batch of ~500 skills was merged into the main branch. Two files were audited in sequence:

| File | Source |
|------|--------|
| `skills.json` (original) | Production registry — 1,444 entries |
| `skills (5).json` (PR branch) | `minminminminchew/happycapy-skills-data` branch `add-500-skills-2026-04-08` — 2,227 entries |
| `featured-skills-description (3).json` | Companion descriptions file — 2,227 entries |

---

## Audit Methodology

The audit ran in three passes using the `skills-json-auditor` skill:

### Pass 1 — Live URL Validation
Each `source.url` was checked via HTTP (HEAD → GET fallback) with 60 concurrent workers. Entries returning HTTP 404 were marked for automatic deletion. Connection errors and non-404 HTTP errors were treated as alive but logged.

### Pass 2 — Risk Assessment
Entries with `vet.risk: "high"` or `meta.risk: "high"` were evaluated against skill-vetter criteria:

**Red flags checked:**
- Suspicious keywords in ID or URL (steal, exfil, inject, bypass, etc.)
- Unknown personal repo with 0 stars
- Credential harvesting patterns in skill code
- Obfuscated / base64-encoded code
- Outbound calls to IPs instead of domains

**Risk classification:**
| Level | Examples | Action |
|-------|----------|--------|
| LOW | Notes, APIs, formatting, file ops | Keep |
| HIGH — legitimate | Medical tools, deployment, SDKs | Keep with warning |
| HIGH — suspicious | Unknown source, 0 stars, no clear purpose | Manual review / delete |

### Pass 3 — Manual Review
WARN-flagged entries were fetched from GitHub and individually reviewed for code content and repo legitimacy.

---

## Results — Production Registry (`skills.json`, 1,444 entries)

| Metric | Count |
|--------|-------|
| Total entries | 1,444 |
| 404 / dead URLs removed | **20** |
| High-risk entries | 9 |
| High-risk: kept with warning | 9 |
| **Final entry count** | **1,424** |

**Removed (404):**
- 9 × Apify skills — entire `apify/agent-skills` subdirectory removed upstream
- 9 × K-Dense-AI scientific skills — repo path gone
- 1 × Figma `implement-design`
- 1 × `agent-browser` (Convex URL dead)

**High-risk kept:** All 9 were legitimate categories — medical tool (`treatment-plans`), deployment (`vercel-deploy-claimable`), security sandbox (`seatbelt-sandboxer` by Trail of Bits), SDK wrappers, etc.

---

## Results — PR Branch (`skills (5).json`, 2,227 entries)

| Metric | Count |
|--------|-------|
| Total entries | 2,227 |
| 404 / dead URLs removed | **37** |
| High-risk entries | 8 |
| High-risk: kept (legitimate) | 3 |
| High-risk: deleted (unclear purpose) | **5** |
| **Final entry count** | **2,185** |

### 37 Entries Removed (404)

| Source Repo | Removed Count | Reason |
|-------------|---------------|--------|
| K-Dense-AI/claude-scientific-skills | 25 | Entire `scientific-skills/` subdirectory gone |
| jezweb/claude-skills | 0 | All URLs alive |
| htdt/godogen | 1 | `godot-task` path 404 |
| firecrawl/cli | 1 | `firecrawl-browser` path 404 |
| glitternetwork/pinme | 1 | `.claude/skills/pinme` path 404 |
| wry-manatee-359.convex.site | 1 | `summarize` slug dead |
| (other) | 8 | Various dead paths |

### 8 High-Risk Entries — Final Decisions

| ID | Source | Risk Reason | Decision | Rationale |
|----|--------|-------------|----------|-----------|
| `mcp-builder-jezweb` | jezweb/claude-skills (700★) | High in JSON, stars=0 (stale data) | **KEPT, downgraded to low** | No red flags, 700-star repo, FastMCP builder tool |
| `nemoclaw-setup` | jezweb/claude-skills (700★) | High in JSON, stars=0 (stale data) | **KEPT, downgraded to low** | NVIDIA NemoClaw official installer, sandboxed architecture |
| `wordpress-setup` | jezweb/claude-skills (700★) | Contains "store credentials" | **KEPT, downgraded to low** | Credentials stored locally in `wp-cli.yml` only, no exfiltration |
| `databases` | mrgoonie/claudekit-skills | High risk, unknown purpose | **DELETED** | Unclear scope, no legitimate category match |
| `media-processing` | mrgoonie/claudekit-skills | High risk, unclear purpose | **DELETED** | Unclear scope, no legitimate category match |
| `snowflake-development` | alirezarezvani/claude-skills | High risk | **DELETED** | Unknown source, no clear legitimate use case |
| `init-alirezarezvani` | alirezarezvani/claude-skills | High risk | **DELETED** | Unknown personal init script, unclear purpose |
| `skill-security-auditor` | alirezarezvani/claude-skills | High risk | **DELETED** | Despite security-sounding name, unknown source with no justification |

---

## Companion File Alignment

`featured-skills-description.json` (2,227 entries) was filtered to match the 2,185 valid IDs by removing all 42 deleted skill IDs. The two files are now in sync.

---

## Output Files

| File | Description | Entries |
|------|-------------|---------|
| `skills_cleaned_v2.json` | Cleaned skills registry | 2,185 |
| `featured-skills-description_cleaned.json` | Aligned descriptions file | 2,185 |
| `audit_report_v2.md` | Full per-entry audit log | — |

---

## Notes & Recommendations

1. **K-Dense-AI stale entries** — The entire `scientific-skills/` subdirectory in `K-Dense-AI/claude-scientific-skills` is gone. If these skills are intended to return, the source repo needs to be updated before re-adding.

2. **Stale vet.stars data** — Several entries had `vet.stars: 0` in JSON but the actual repo has hundreds of stars (e.g., jezweb/claude-skills: 700★). Consider refreshing `vet` metadata periodically.

3. **Convex URL skills** — Two Convex-hosted skills (`agent-browser`, `summarize`) had dead download URLs. Convex-hosted skills should be monitored more frequently as they can disappear without repo changes.

4. **Future audits** — The `skills-json-auditor` skill is now installed and can re-run this process on any future `skills.json` with a single command.

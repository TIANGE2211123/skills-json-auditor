# skills-json-auditor

A HappyCapy agent skill for auditing `skills.json` registry files.

## What it does

1. **URL validation** — Checks all `source.url` entries via HTTP; removes 404 entries
2. **Risk assessment** — Applies skill-vetter criteria to high-risk entries
3. **Manual deep-check** — Fetches and scans SKILL.md for flagged repos
4. **Companion file alignment** — Syncs `featured-skills-description.json` to same ID set
5. **Audit report** — Produces a full Markdown summary of all decisions

## Files

| File | Description |
|------|-------------|
| `skill-auditor/SKILL.md` | Skill instructions for the agent |
| `skill-auditor/scripts/audit_skills.py` | Python audit script (concurrent URL checker) |
| `AUDIT_SUMMARY.md` | Example audit report from 2026-04-08 run |

## Usage

Install the skill:
```bash
cp -r skill-auditor ~/.claude/skills/skills-json-auditor
```

Run the audit:
```bash
python3 ~/.claude/skills/skills-json-auditor/scripts/audit_skills.py \
  --input skills.json \
  --output skills_cleaned.json \
  --report audit_report.md \
  --workers 60
```

## Audit results (2026-04-08)

- Input: 2,227 entries
- 404 removed: 37
- High-risk deleted: 5
- High-risk downgraded to low: 3
- **Final: 2,185 entries**

## Audit results (2026-04-09)

**Target:** `minminminminchew/happycapy-skills-data` branch `add-500-skills-v2-2026-04-08`

| Metric | Count |
|--------|-------|
| Input entries | 2,685 |
| True 404 removed | 1 (`plotly`) |
| Feishu entries removed (user decision) | 9 |
| High-risk offensive tools removed | 3 |
| High-risk downgraded to low | 25 |
| **Final count** | **2,672** |

**Script bugs identified:**
- Non-ASCII URL paths (Chinese chars) cause false 404 — needs `urllib.parse.quote()`
- Keyword-only risk detection too broad — false-flagged 3 legitimate forensic tools

See [AUDIT_SUMMARY_2026-04-09.md](./AUDIT_SUMMARY_2026-04-09.md) for full details.


## Audit results (2026-04-15)

**Branch:** `add-500-skills-v3-2026-04-14`

| Metric | Count |
|--------|-------|
| Input entries | 3,172 |
| Unique URLs checked | 3,171 |
| True 404 removed | 108 |
| High-risk entries | 0 |
| Final count | 3,064 |

**Key findings:**
- CharlesWiltgen/Axiom accounted for 82/108 removals (repo restructured skill paths)
- No high-risk entries found (cleaned in v2 audit)
- 3-phase URL verification: direct check -> GitHub API re-verify -> final timeout re-check
- All 404s confirmed via authenticated GitHub Contents API

Full report: [AUDIT_SUMMARY_2026-04-15.md](./AUDIT_SUMMARY_2026-04-15.md)


## Audit results (2026-04-20)

**Branch**: `add-500-skills-v4-2026-04-17`

| Metric | Count |
|--------|-------|
| Input entries | 3,563 |
| Confirmed 404 removed | 24 |
| Chinese char URLs | 0 |
| High-risk entries | 0 |
| Duplicate IDs | 0 |
| Final count | 3,539 |

See [AUDIT_SUMMARY_2026-04-20.md](./AUDIT_SUMMARY_2026-04-20.md) for full details.

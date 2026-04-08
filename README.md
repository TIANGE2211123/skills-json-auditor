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

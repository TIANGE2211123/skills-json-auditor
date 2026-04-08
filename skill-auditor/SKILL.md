---
name: skills-json-auditor
description: Audit a skills.json registry file — check all source URLs for 404s, delete dead entries, run security risk review on high-risk skills using skill-vetter criteria, align companion files, write an audit report, and optionally push results to GitHub. Use this skill whenever the user wants to clean up a skills registry, validate skill URLs, check which skills have broken links, audit skill risk levels, remove unsafe/dead entries from a skills.json file, or sync a companion descriptions file.
---

# Skills JSON Auditor

End-to-end audit workflow for a HappyCapy `skills.json` registry:

1. **URL check** — HTTP-verify every `source.url`; delete entries that return 404
2. **High-risk review** — apply skill-vetter criteria to all `risk: "high"` entries
3. **Manual deep-check** — fetch and scan SKILL.md content for flagged entries
4. **Companion file alignment** — sync any related JSON (e.g. `featured-skills-description.json`) to the same ID set
5. **Audit report** — produce a Markdown summary of all decisions
6. **GitHub push** — optionally commit and push cleaned files back to the PR branch

---

## Trigger phrases

- "check/validate URLs in skills.json"
- "clean up skills registry"
- "audit skill risk levels"
- "remove broken/dead skill entries"
- "sync companion descriptions file"
- "审核 skills.json"

---

## Step 1 — Locate input files

If the user did not specify paths, look for:
- `./uploads/skills.json` or `./skills.json`
- `./uploads/featured-skills-description*.json` (companion)

Ask the user if you cannot find them.

---

## Step 2 — Run the audit script

```bash
python3 ~/.claude/skills/skills-json-auditor/scripts/audit_skills.py \
  --input <path/to/skills.json> \
  --output <path/to/skills_cleaned.json> \
  --report <path/to/audit_report.md> \
  --workers 60
```

The script:
- Checks every `source.url` concurrently (HEAD → GET fallback, 10s timeout)
- Marks entries 404 for deletion
- Flags entries where `vet.risk` or `meta.risk` is `"high"`
- Writes `skills_cleaned.json` (404 entries removed, `vet` fields updated)
- Writes `audit_report.md`

---

## Step 3 — Review high-risk entries

For each WARN-flagged entry, fetch and inspect the actual SKILL.md:

```bash
curl -s "https://raw.githubusercontent.com/<OWNER>/<REPO>/main/<PATH>/SKILL.md"
```

Also check repo stats:

```bash
curl -s "https://api.github.com/repos/<OWNER>/<REPO>" | \
  python3 -c "import json,sys; d=json.load(sys.stdin); print('Stars:', d['stargazers_count'], '| Updated:', d['updated_at'])"
```

### Red flags — recommend DELETE if any present:
- Suspicious keywords in ID or URL: `steal`, `exfil`, `inject`, `bypass`, `rootkit`, `keylog`
- Credential harvesting: reads `~/.ssh`, `~/.aws`, sends data outbound
- Obfuscated code: `base64`, `eval()`, minified blobs
- Outbound POST to unknown domains
- 0-star personal repo with no clear legitimate purpose

### Keep with note (legitimate high-risk categories):
| Category | Example IDs | Why high-risk is OK |
|----------|-------------|---------------------|
| Medical tools | `treatment-plans` | Sensitive data, not malicious |
| Deployment | `vercel-deploy-*` | High-impact, legitimate org |
| Security sandbox | `seatbelt-sandboxer` | Reputable security firm |
| SDK wrappers | `javascript-sdk`, `python-sdk` | Standard integration |
| Dev cert tools | `dotnet-devcert-trust` | Touches system trust store |

### Stale `vet.stars` data
The `vet.stars` field in JSON can be outdated. Always verify against GitHub API before dismissing a repo as "unknown". A repo showing `stars: 0` in JSON might have hundreds of real stars.

---

## Step 4 — Apply manual decisions

After reviewing WARN entries, update the cleaned JSON:

```python
import json

with open('skills_cleaned.json') as f:
    data = json.load(f)

to_delete = {'id-one', 'id-two'}           # confirmed bad
to_downgrade = {'id-three', 'id-four'}     # confirmed safe, fix stale risk

result = []
for entry in data:
    if entry['id'] in to_delete:
        continue
    if entry['id'] in to_downgrade:
        entry['vet']['risk'] = 'low'
        entry['meta']['risk'] = 'low'
    result.append(entry)

with open('skills_cleaned.json', 'w') as f:
    json.dump(result, f, indent=2, ensure_ascii=False)
```

---

## Step 5 — Align companion file

If a companion file (e.g. `featured-skills-description.json`) exists, filter it to the same valid ID set:

```python
import json

with open('skills_cleaned.json') as f:
    valid_ids = {e['id'] for e in json.load(f)}

with open('featured-skills-description.json') as f:
    featured = json.load(f)

filtered = [e for e in featured if e.get('id') in valid_ids]

with open('featured-skills-description_cleaned.json', 'w') as f:
    json.dump(filtered, f, indent=2, ensure_ascii=False)

print(f"{len(featured)} → {len(filtered)} entries")
```

---

## Step 6 — Write the audit summary

Produce an `audit_summary.md` covering:

```markdown
# Skills Registry Audit Report
**Date / Auditor / Scope**

## Methodology (URL check → risk review → manual review)

## Results — per file
- Total entries, 404 removed, high-risk decisions, final count

## High-risk entry decisions table
| ID | Source | Risk Reason | Decision | Rationale |

## Companion file alignment

## Output files

## Notes & Recommendations
- Stale vet data issues
- Recurring dead URL patterns
- Future audit suggestions
```

---

## Step 7 — Push to GitHub (optional)

If the user wants to commit the cleaned files back to the PR branch:

```bash
# Configure git identity if needed
git config user.email "capy@happycapy.ai"
git config user.name "Capy"

# Clone the target repo (use GITHUB_TOKEN if available)
git clone https://<TOKEN>@github.com/<OWNER>/<REPO>.git /tmp/skills-repo
cd /tmp/skills-repo
git checkout <BRANCH>

# Copy cleaned files
cp skills_cleaned.json data/skills.json
cp featured-skills-description_cleaned.json data/featured-skills-description.json

# Commit and push
git add data/skills.json data/featured-skills-description.json
git commit -m "chore: remove dead URLs and high-risk entries [skills-json-auditor]

- Removed X entries with 404 URLs
- Removed X high-risk entries without clear purpose
- Downgraded X entries from high to low risk (stale vet data)
- Aligned featured-skills-description.json to match
- Final count: XXXX entries"

git push origin <BRANCH>
```

**If no token is available**, ask the user to provide one or upload the files manually.

---

## Output files

| File | Contents |
|------|----------|
| `skills_cleaned.json` | Cleaned registry, `vet` fields updated |
| `featured-skills-description_cleaned.json` | Aligned companion file |
| `audit_report.md` | Per-entry log from script |
| `audit_summary.md` | Human-readable full report with decisions and recommendations |

Place all outputs in `./outputs/` if it exists, otherwise next to the input file.

---

## Risk classification reference

| Risk | Source Trust | Action |
|------|-------------|--------|
| LOW | Official happycapy-ai or known org (microsoft, vercel, github) | Keep |
| LOW (downgraded) | WARN entry with no red flags, stale vet data | Keep, fix vet fields |
| HIGH — legitimate | Medical, deployment, security tools from reputable orgs | Keep with note |
| HIGH — suspicious | Unknown personal repo, 0 stars, unclear purpose | Delete |
| Any | URL returns 404 | Delete immediately |

# Skills Registry Audit Report — Branch `add-500-skills-v2-2026-04-08`

**Date:** 2026-04-09
**Auditor:** Capy (HappyCapy skills-json-auditor)
**Repo:** `minminminminchew/happycapy-skills-data`
**Scope:** `data/skills.json` + `data/featured-skills-description.json`

---

## Summary

| Metric | Count |
|--------|-------|
| Total entries (input) | 2,685 |
| URLs checked | 2,685 |
| True 404 / dead URLs | 1 |
| Script false positives (restored) | 12 |
| High-risk entries reviewed | 28 |
| High-risk: legitimate (KEEP) | 28 |
| **Final entry count** | **2,684** |

---

## Phase 1 — URL Check (automated)

Concurrent HEAD → GET fallback, 60 workers, 10s timeout.

### Script raw output
- 404 / dead: **10 flagged** (1 true dead + 9 encoding errors)
- Auto-deleted high-risk: **3** (keyword false positives)
- Raw script output count: **2,672**

---

## Phase 2 — False Positive Correction

### 9 × feishu entries restored (op7418/CodePilot, 5,131★)

The script threw an `'ascii' codec can't encode` error on URLs containing Chinese characters (`资料/` path segment). The URLs are valid and the files exist on GitHub. All 9 entries restored.

| ID | Status |
|----|--------|
| `feishu-bitable` | RESTORED |
| `feishu-calendar` | RESTORED |
| `feishu-channel-rules` | RESTORED |
| `feishu-create-doc` | RESTORED |
| `feishu-fetch-doc` | RESTORED |
| `feishu-im-read` | RESTORED |
| `feishu-task` | RESTORED |
| `feishu-troubleshoot` | RESTORED |
| `feishu-update-doc` | RESTORED |

**Root cause:** Audit script must URL-encode non-ASCII path segments before HTTP HEAD check.

### 3 × mukul975 cybersecurity entries restored (4,157★)

Keyword detector flagged `rootkit`, `malware`, `deobfuscat` as suspicious. Manual review showed all three are **defensive/forensic analysis tools** — they analyze malicious artifacts, not deploy them.

| ID | False-flag keyword | Actual purpose | Decision |
|----|-------------------|----------------|---------|
| `analyzing-linux-kernel-rootkits` | `rootkits` | Volatility3 memory forensics, rkhunter scan — **detect** rootkits | RESTORED |
| `analyzing-pdf-malware-with-pdfid` | `malware` | PDFiD static analysis of suspicious attachments — **analyze** malware | RESTORED |
| `deobfuscating-javascript-malware` | `malware` | Reverse eval-chain obfuscation in phishing scripts — **defensive** | RESTORED |

**Context:** `mukul975/Anthropic-Cybersecurity-Skills` — 754 cybersecurity skills, 4,157★, 450 forks, MITRE ATT&CK + NIST CSF 2.0 mapped, Apache 2.0. Highly reputable.

---

## Phase 3 — True 404 Removed

| ID | URL | Reason |
|----|-----|--------|
| `plotly` | `K-Dense-AI/claude-scientific-skills/.../plotly` | HTTP 404 — path does not exist in repo |

---

## Phase 4 — High-Risk Review (28 entries)

All 28 high-risk entries are from two reputable sources:

### wshobson/agents (security/devops skills)
`security-and-hardening`, `code-review-excellence`, `gitops-workflow`, `uv-package-manager`, `memory-forensics`
→ All KEEP. Professional DevOps/security tooling, well-documented.

### mukul975/Anthropic-Cybersecurity-Skills (4,157★)
23 cybersecurity skill entries flagged high-risk by vet fields.
→ All KEEP. Legitimate cybersecurity training/operations skills. Risk rating is accurate (these ARE powerful tools) but origin is reputable and purpose is defensive.

---

## Phase 5 — Companion File Alignment

`featured-skills-description.json`: 2,685 → **2,684** entries
Removed: `plotly` (matching skills.json)

---

## Output Files

| File | Entries | Description |
|------|---------|-------------|
| `skills_v2_final.json` | 2,684 | Cleaned skills registry |
| `featured_v2_final.json` | 2,684 | Aligned companion file |

---

## Issues Found & Recommendations

### Bug: Audit script fails on non-ASCII URLs
The script's URL checker does not handle UTF-8 path segments (Chinese characters). URLs like `github.com/op7418/CodePilot/tree/main/资料/...` cause `UnicodeEncodeError` and are incorrectly marked as dead.

**Fix needed in `audit_skills.py`:**
```python
from urllib.parse import quote
url = quote(url, safe=':/?#[]@!$&\'()*+,;=')
```

### Bug: Keyword-based high-risk detector is too broad
Simple keyword matching on `rootkit`, `malware`, `deobfuscat` flags defensive security tools. Keyword matching should be combined with context (description, domain, author reputation).

**Fix needed:** Weight keywords against repo star count and skill `domain: cybersecurity/subdomain: malware-analysis` context.

### Recurring pattern: K-Dense-AI/claude-scientific-skills
This repo lost its `scientific-skills/` subdirectory. Several entries from this repo were removed in a prior audit (2026-04-08). `plotly` is the last remaining dead entry.

#!/usr/bin/env python3
"""
Skills JSON Auditor
Checks all source.url entries for 404s and flags high-risk entries.
"""

import argparse
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from urllib import request, error


def check_url(entry: dict) -> dict:
    """Return entry augmented with live URL check result."""
    url = entry.get("source", {}).get("url", "")
    item_id = entry.get("id", "unknown")

    if not url:
        return {**entry, "_check": {"status": None, "ok": False, "reason": "no_url"}}

    # Try HEAD first, fall back to GET
    for method in ("HEAD", "GET"):
        try:
            req = request.Request(
                url,
                method=method,
                headers={
                    "User-Agent": "Mozilla/5.0 (skills-json-auditor/1.0)",
                    "Accept": "*/*",
                },
            )
            resp = request.urlopen(req, timeout=10)
            return {
                **entry,
                "_check": {"status": resp.status, "ok": True, "reason": "ok"},
            }
        except error.HTTPError as e:
            if e.code == 404:
                return {
                    **entry,
                    "_check": {
                        "status": 404,
                        "ok": False,
                        "reason": "404_not_found",
                    },
                }
            if method == "GET":
                # Non-404 HTTP error on second attempt — treat as alive but note it
                return {
                    **entry,
                    "_check": {
                        "status": e.code,
                        "ok": True,
                        "reason": f"http_{e.code}",
                    },
                }
        except error.URLError as e:
            if method == "GET":
                return {
                    **entry,
                    "_check": {
                        "status": None,
                        "ok": False,
                        "reason": f"connection_error: {e.reason}",
                    },
                }
        except Exception as e:
            if method == "GET":
                return {
                    **entry,
                    "_check": {
                        "status": None,
                        "ok": False,
                        "reason": f"error: {e}",
                    },
                }

    return {**entry, "_check": {"status": None, "ok": False, "reason": "unknown"}}


def is_high_risk(entry: dict) -> bool:
    vet = entry.get("vet", {})
    meta = entry.get("meta", {})
    return vet.get("risk") == "high" or meta.get("risk") == "high"


def assess_high_risk(entry: dict) -> dict:
    """
    Apply skill-vetter logic to a high-risk entry.
    Returns a dict with 'verdict' (keep/delete/warn) and 'notes'.
    """
    item_id = entry.get("id", "")
    url = entry.get("source", {}).get("url", "")
    trust_level = entry.get("vet", {}).get("trust_level", 3)
    stars = entry.get("vet", {}).get("stars", 0)

    # Suspicious patterns in name or URL
    suspicious_keywords = [
        "steal", "exfil", "backdoor", "malware", "exploit",
        "inject", "payload", "bypass", "rootkit", "keylog",
    ]
    name_lower = item_id.lower()
    url_lower = url.lower()
    suspicious = any(k in name_lower or k in url_lower for k in suspicious_keywords)

    # Legitimate high-risk categories
    legitimate_high_risk = {
        "treatment-plans": "Medical tool — sensitive but legitimate",
        "vercel-deploy-claimable": "Deployment tool — high-impact but legitimate (Vercel Labs)",
        "ai-automation-workflows": "Automation — review source legitimacy",
        "guidance": "Prompt engineering research — review source legitimacy",
        "seatbelt-sandboxer": "Security sandbox by Trail of Bits — reputable security firm",
        "langchain": "Agent framework — review source legitimacy",
        "javascript-sdk": "SDK wrapper — review source legitimacy",
        "python-sdk": "SDK wrapper — review source legitimacy",
        "dotnet-devcert-trust": "Dev cert tool — touches system trust store",
    }

    if suspicious:
        return {
            "verdict": "delete",
            "notes": f"Suspicious keywords detected in name/URL: {item_id}",
        }

    if item_id in legitimate_high_risk:
        return {
            "verdict": "keep_with_warning",
            "notes": legitimate_high_risk[item_id],
        }

    # Unknown high-risk entry from low-trust source
    if trust_level >= 3 and stars == 0:
        return {
            "verdict": "warn",
            "notes": "High risk + unknown source (0 stars, trust_level>=3) — manual review recommended",
        }

    return {
        "verdict": "keep_with_warning",
        "notes": "High risk flagged — review manually before deploying",
    }


def main():
    parser = argparse.ArgumentParser(description="Audit a skills.json file")
    parser.add_argument("--input", required=True, help="Path to skills.json")
    parser.add_argument("--output", required=True, help="Path to write cleaned JSON")
    parser.add_argument("--report", required=True, help="Path to write audit report")
    parser.add_argument("--workers", type=int, default=50, help="Concurrent URL checkers")
    parser.add_argument("--skip-url-check", action="store_true", help="Skip live URL checks (use existing vet data)")
    args = parser.parse_args()

    print(f"[audit] Loading {args.input} ...", flush=True)
    with open(args.input) as f:
        data = json.load(f)
    total = len(data)
    print(f"[audit] {total} entries loaded.", flush=True)

    # ── URL checks ────────────────────────────────────────────────────────────
    if args.skip_url_check:
        print("[audit] Skipping live URL checks (using existing vet data).", flush=True)
        checked = []
        for entry in data:
            url_ok = entry.get("vet", {}).get("url_ok", True)
            checked.append({
                **entry,
                "_check": {
                    "status": 200 if url_ok else 404,
                    "ok": url_ok,
                    "reason": "cached",
                },
            })
    else:
        print(f"[audit] Checking {total} URLs with {args.workers} workers ...", flush=True)
        checked = [None] * total
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {pool.submit(check_url, entry): i for i, entry in enumerate(data)}
            done = 0
            for future in as_completed(futures):
                idx = futures[future]
                checked[idx] = future.result()
                done += 1
                if done % 100 == 0 or done == total:
                    print(f"[audit]   {done}/{total} checked ...", flush=True)

    # ── Partition results ─────────────────────────────────────────────────────
    dead = [e for e in checked if not e["_check"]["ok"]]
    alive = [e for e in checked if e["_check"]["ok"]]

    print(f"[audit] Dead (404/error): {len(dead)}", flush=True)
    print(f"[audit] Alive: {len(alive)}", flush=True)

    # ── High-risk assessment on alive entries ─────────────────────────────────
    high_risk_entries = [e for e in alive if is_high_risk(e)]
    assessments = {}
    for e in high_risk_entries:
        assessments[e["id"]] = assess_high_risk(e)

    recommended_delete = [
        e for e in high_risk_entries
        if assessments[e["id"]]["verdict"] == "delete"
    ]

    # ── Build cleaned output ──────────────────────────────────────────────────
    delete_ids = {e["id"] for e in dead} | {e["id"] for e in recommended_delete}
    cleaned = []
    for entry in alive:
        if entry["id"] in delete_ids:
            continue
        # Update vet fields with fresh check result
        check = entry["_check"]
        updated = dict(entry)
        updated.setdefault("vet", {})
        updated["vet"]["url_ok"] = check["ok"]
        updated["vet"]["url_status"] = "ok" if check["ok"] else check["reason"]
        updated["vet"]["last_checked"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        del updated["_check"]
        cleaned.append(updated)

    print(f"[audit] Final entry count: {len(cleaned)}", flush=True)

    with open(args.output, "w") as f:
        json.dump(cleaned, f, indent=2, ensure_ascii=False)
    print(f"[audit] Cleaned JSON written to {args.output}", flush=True)

    # ── Report ────────────────────────────────────────────────────────────────
    lines = []
    lines.append("# Skills JSON Audit Report")
    lines.append(f"\n**Date:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append(f"**Input:** `{args.input}`\n")
    lines.append("## Summary\n")
    lines.append(f"| Metric | Count |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Total entries | {total} |")
    lines.append(f"| 404 / dead URLs | {len(dead)} |")
    lines.append(f"| High-risk flagged | {len(high_risk_entries)} |")
    lines.append(f"| High-risk: keep with warning | {sum(1 for a in assessments.values() if a['verdict'] == 'keep_with_warning')} |")
    lines.append(f"| High-risk: warn (manual review) | {sum(1 for a in assessments.values() if a['verdict'] == 'warn')} |")
    lines.append(f"| High-risk: recommended delete | {len(recommended_delete)} |")
    lines.append(f"| **Final entry count** | **{len(cleaned)}** |")

    lines.append("\n---\n")
    lines.append("## Removed: Dead URLs (404 / connection error)\n")
    if dead:
        lines.append("| ID | URL | Status | Reason |")
        lines.append("|----|-----|--------|--------|")
        for e in dead:
            c = e["_check"]
            url = e.get("source", {}).get("url", "—")
            lines.append(f"| `{e['id']}` | {url} | {c['status']} | {c['reason']} |")
    else:
        lines.append("_None — all URLs alive._")

    lines.append("\n---\n")
    lines.append("## High-Risk Entries Analysis\n")
    if high_risk_entries:
        lines.append("| ID | URL | Verdict | Notes |")
        lines.append("|----|-----|---------|-------|")
        for e in high_risk_entries:
            a = assessments[e["id"]]
            url = e.get("source", {}).get("url", "—")
            verdict_icon = {"keep_with_warning": "KEEP", "warn": "WARN", "delete": "DELETE"}.get(a["verdict"], a["verdict"])
            lines.append(f"| `{e['id']}` | {url} | {verdict_icon} | {a['notes']} |")
    else:
        lines.append("_No high-risk entries found._")

    lines.append("\n---\n")
    lines.append("## Recommended Actions\n")
    warn_entries = [e for e in high_risk_entries if assessments[e["id"]]["verdict"] == "warn"]
    if warn_entries:
        lines.append("The following entries need **manual review** before a decision:")
        for e in warn_entries:
            lines.append(f"- `{e['id']}` — {e.get('source', {}).get('url', '')} — {assessments[e['id']]['notes']}")
    else:
        lines.append("_No manual review required._")

    report_text = "\n".join(lines)
    with open(args.report, "w") as f:
        f.write(report_text)
    print(f"[audit] Report written to {args.report}", flush=True)

    # Print summary to stdout
    print("\n" + "=" * 50)
    print(f"AUDIT COMPLETE")
    print(f"  Total:         {total}")
    print(f"  404/dead:      {len(dead)}")
    print(f"  High-risk:     {len(high_risk_entries)}")
    print(f"  Removed total: {total - len(cleaned)}")
    print(f"  Final count:   {len(cleaned)}")
    print("=" * 50)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Newsletter Subscription Telemetry Analyzer

Aggregates statistics from reports/Newsletter_YYYY_MM_DD/ and suggestion files
(suggestions_reviewed.md, suggestions_filtered.md, suggestions_pending.md) over
a specified time window (default: 30 days) to evaluate newsletter ROI and triage.
"""

import argparse
from collections import defaultdict
from datetime import datetime, timedelta
import glob
import json
import os
import re
import sys

def normalize_source(filename: str = "", title_url: str = "") -> str:
    """Normalize various filename, subject, and URL patterns to canonical newsletter names."""
    combined = f"{filename} {title_url}".lower()
    
    if "rundown" in combined:
        return "The Rundown AI"
    if "the_code" in combined or "the code" in combined or "codenewsletter.ai" in combined:
        return "The Code"
    if "superhuman" in combined:
        return "Superhuman"
    if "bytebytego" in combined or "alex_xu" in combined:
        return "ByteByteGo (Alex Xu)"
    if "neo_kim" in combined or "system_design_one" in combined or "systemdesign" in combined:
        return "System Design One (Neo Kim)"
    if "gary" in combined or "garychen" in combined:
        return "Gary Chen (創作者的秘密)"
    if "waki" in combined or "readingoutpost" in combined or "瓦基" in combined:
        return "閱讀前哨站 (瓦基)"
    if "ally" in combined or "ally_hsieh" in combined:
        return "Ally Hsieh"
    if "hugging" in combined or "huggingface" in combined:
        return "Hugging Face Daily Papers"
    if "zhu" in combined or "henrychu" in combined or "朱騏" in combined:
        return "朱騏 (Henry Chu)"
    if "matt" in combined or "pocock" in combined:
        return "Matt Pocock"
    if "tech_scoop" in combined or "techscoop" in combined:
        return "Tech Scoop"
    if "ai_hero" in combined or "aihero" in combined:
        return "AI Hero"
    if "jeff_su" in combined or "jeff su" in combined:
        return "Jeff Su"
    if "pragmatic" in combined or "gergely" in combined:
        return "The Pragmatic Engineer (Gergely Orosz)"
    if "inner_circle" in combined:
        return "AI Inner Circle"
    if "今天學到了什麼" in combined or "今日學到了什麼" in combined:
        return "今天學到了什麼"
    if "readtodie" in combined:
        return "ReadToDie"
    if "chris_richardson" in combined or "microservices_io" in combined:
        return "Microservices.IO (Chris Richardson)"
    if "backend_weekly" in combined:
        return "Backend Weekly"
    
    # Fallback to prefix
    if filename:
        clean_fn = os.path.splitext(filename)[0]
        parts = clean_fn.split('_')
        return " ".join(parts[:2])
    return "Other / Unknown"

def parse_suggestion_file(filepath: str):
    """Parse suggestion entries from a markdown file."""
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
        
    chunks = text.split("\n---\n")
    entries = []
    for chunk in chunks:
        lines = chunk.strip().split("\n")
        if not lines or not lines[0].startswith("### "):
            continue
        header = lines[0]
        # Format: ### YYYY-MM-DD | Type | [Title](url)
        parts = header[4:].split(" | ")
        date_str = parts[0].strip() if len(parts) > 0 else ""
        entry_type = parts[1].strip() if len(parts) > 1 else ""
        title_url = parts[2].strip() if len(parts) > 2 else ""
        
        report_path, feedback, comment, category, score_status, suggestion_text = "", "", "", "", "", ""
        for l in lines[1:]:
            l_strip = l.strip()
            if "🏷️" in l_strip:
                cat_m = re.search(r"🏷️\s*([^\|]+)", l_strip)
                if cat_m: category = cat_m.group(1).strip()
                sc_m = re.search(r"📊\s*(.+)", l_strip)
                if sc_m: score_status = sc_m.group(1).strip()
            elif "**Feedback**:" in l_strip or "- Feedback:" in l_strip:
                feedback = l_strip
            elif "**Comment**:" in l_strip or "- Comment:" in l_strip:
                comment = l_strip
            elif "[報告]" in l_strip or "[完整報告]" in l_strip:
                report_path = l_strip
            elif "建議" in l_strip:
                suggestion_text = l_strip
                
        entries.append({
            "date": date_str,
            "type": entry_type,
            "title_url": title_url,
            "category": category,
            "score_status": score_status,
            "feedback": feedback,
            "comment": comment,
            "report_path": report_path,
            "suggestion": suggestion_text,
            "raw": chunk
        })
    return entries

def extract_veto_category(score_status: str) -> str:
    """Extract human-readable veto or filter reason."""
    if "Hard-veto:" in score_status:
        m = re.search(r"Hard-veto:\s*([^)]+)", score_status)
        if m:
            return m.group(1).strip()
        return "Hard-veto"
    if "Below threshold" in score_status:
        return "Below threshold"
    return "Filtered"

def analyze_subscriptions(workspace_dir: str = ".", days: int = 30, start_date: str = None, end_date: str = None):
    """Compute newsletter statistics and triage recommendations."""
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")
    if not start_date:
        start_dt = datetime.strptime(end_date, "%Y-%m-%d") - timedelta(days=days)
        start_date = start_dt.strftime("%Y-%m-%d")

    reports_dir = os.path.join(workspace_dir, "reports")
    data_dir = os.path.join(workspace_dir, "data")

    # 1. Gather all newsletter report files within date range
    reports_by_source = defaultdict(list)
    newsletter_dirs = glob.glob(os.path.join(reports_dir, "Newsletter_*"))
    
    for d in newsletter_dirs:
        dir_name = os.path.basename(d)
        m = re.search(r"Newsletter_(\d{4}_\d{2}_\d{2})", dir_name)
        if not m:
            continue
        ds = m.group(1).replace("_", "-")
        if start_date <= ds <= end_date:
            for f in glob.glob(os.path.join(d, "*.md")):
                bn = os.path.basename(f)
                src = normalize_source(filename=bn)
                reports_by_source[src].append({
                    "date": ds,
                    "filepath": f,
                    "filename": bn
                })

    # 2. Parse suggestions files
    reviewed_entries = parse_suggestion_file(os.path.join(data_dir, "suggestions_reviewed.md"))
    filtered_entries = parse_suggestion_file(os.path.join(data_dir, "suggestions_filtered.md"))
    pending_entries = parse_suggestion_file(os.path.join(data_dir, "suggestions_pending.md"))

    # 3. Aggregate stats by source
    stats = defaultdict(lambda: {
        "reports_count": 0,
        "reviewed_count": 0,
        "accepted_count": 0,
        "rejected_count": 0,
        "filtered_count": 0,
        "pending_count": 0,
        "acceptance_rate": 0.0,
        "yield_rate": 0.0,
        "veto_reasons": defaultdict(int),
        "rejection_comments": [],
        "accepted_examples": [],
        "triage": "Watch"
    })

    # Populate report counts
    for src, rep_list in reports_by_source.items():
        stats[src]["reports_count"] = len(rep_list)

    # Helper to resolve source name from an entry
    def resolve_source(entry):
        rp = entry["report_path"]
        m = re.search(r"reports/Newsletter_[^/]+/([^/]+)\.md", rp)
        fn = m.group(1) if m else ""
        return normalize_source(filename=fn, title_url=entry["title_url"])

    # Process reviewed
    for e in reviewed_entries:
        if e["type"] == "Newsletter" and start_date <= e["date"] <= end_date:
            src = resolve_source(e)
            stats[src]["reviewed_count"] += 1
            fb = e["feedback"].lower()
            if "accept" in fb:
                stats[src]["accepted_count"] += 1
                stats[src]["accepted_examples"].append({
                    "date": e["date"],
                    "title": e["title_url"],
                    "suggestion": e["suggestion"]
                })
            elif "reject" in fb:
                stats[src]["rejected_count"] += 1
                if e["comment"]:
                    stats[src]["rejection_comments"].append(e["comment"])

    # Process filtered
    for e in filtered_entries:
        if e["type"] == "Newsletter" and start_date <= e["date"] <= end_date:
            src = resolve_source(e)
            stats[src]["filtered_count"] += 1
            veto = extract_veto_category(e["score_status"])
            stats[src]["veto_reasons"][veto] += 1

    # Process pending
    for e in pending_entries:
        if e["type"] == "Newsletter" and start_date <= e["date"] <= end_date:
            src = resolve_source(e)
            stats[src]["pending_count"] += 1

    # Calculate rates and triage
    results = []
    for src, d in stats.items():
        rcvd = d["reports_count"]
        rev = d["reviewed_count"]
        acc = d["accepted_count"]
        rej = d["rejected_count"]
        filt = d["filtered_count"]
        
        acc_rate = (acc / rev) if rev > 0 else 0.0
        yield_rate = (acc / rcvd) if rcvd > 0 else 0.0
        
        d["acceptance_rate"] = round(acc_rate, 3)
        d["yield_rate"] = round(yield_rate, 3)

        # Triage logic
        # 1. Unsubscribe: strong negative signals (poor acceptance, high veto ratio with low acceptance, or zero acceptances)
        if (rev >= 3 and acc_rate < 0.40) or \
           (rev >= 2 and acc == 0) or \
           (filt >= 4 and yield_rate < 0.08) or \
           (rcvd >= 10 and yield_rate < 0.08 and acc_rate < 0.60) or \
           (filt >= 3 and filt / max(1, (rev + filt)) >= 0.50 and acc_rate < 0.50):
            d["triage"] = "Unsubscribe"
        # 2. Adjust / Filter: high volume, solid acceptance, but notable separable noise (filt >= 3 or rcvd >= 15 with mixed results)
        elif rcvd >= 15 and acc >= 2 and (filt >= 3 or (0.40 <= acc_rate < 0.60)):
            d["triage"] = "Adjust"
        # 3. Strong Keep: high acceptance or high yield with multiple reviews
        elif (rev >= 2 and acc_rate >= 0.60) or yield_rate >= 0.20:
            d["triage"] = "Keep"
        else:
            d["triage"] = "Watch"

        # Convert veto_reasons dict for JSON serialization
        d["veto_reasons"] = dict(d["veto_reasons"])
        
        entry_data = {"source": src, **d}
        results.append(entry_data)

    # Sort results: Keep first, then Adjust, then Unsubscribe, then Watch; secondary sort by reports_count desc
    triage_order = {"Keep": 0, "Adjust": 1, "Unsubscribe": 2, "Watch": 3}
    results.sort(key=lambda x: (triage_order.get(x["triage"], 4), -x["accepted_count"], -x["reports_count"]))

    return {
        "time_window": {
            "start_date": start_date,
            "end_date": end_date,
            "days": days
        },
        "total_newsletters_evaluated": len(results),
        "total_reports": sum(r["reports_count"] for r in results),
        "total_accepted": sum(r["accepted_count"] for r in results),
        "subscriptions": results
    }

def format_markdown_table(data: dict) -> str:
    """Format the evaluation telemetry as a markdown table."""
    lines = [
        f"# 📬 Newsletter Subscription Audit ({data['time_window']['start_date']} ~ {data['time_window']['end_date']})",
        f"> Evaluated {data['total_newsletters_evaluated']} sources across {data['total_reports']} reports. Accepted suggestions: {data['total_accepted']}.\n",
        "| Source | Triage | Reports | Reviewed | Accept | Reject | Filtered | Pend | Accept Rate | Yield Rate |",
        "|---|:---:|---:|---:|---:|---:|---:|---:|---:|---:|"
    ]
    
    icon_map = {
        "Keep": "🟢 Keep",
        "Unsubscribe": "🔴 Unsubscribe",
        "Adjust": "🟡 Adjust",
        "Watch": "⚪ Watch"
    }

    for s in data["subscriptions"]:
        triage_str = icon_map.get(s["triage"], s["triage"])
        acc_pct = f"{s['acceptance_rate']*100:.1f}%" if s["reviewed_count"] > 0 else "-"
        yield_pct = f"{s['yield_rate']*100:.1f}%" if s["reports_count"] > 0 else "-"
        lines.append(
            f"| {s['source']} | {triage_str} | {s['reports_count']} | {s['reviewed_count']} | {s['accepted_count']} | {s['rejected_count']} | {s['filtered_count']} | {s['pending_count']} | {acc_pct} | {yield_pct} |"
        )
        
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Audit and analyze newsletter subscriptions based on reports and suggestions.")
    parser.add_argument("--days", type=int, default=30, help="Number of past days to analyze (default: 30)")
    parser.add_argument("--start-date", type=str, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", type=str, help="End date (YYYY-MM-DD)")
    parser.add_argument("--workspace", type=str, default=".", help="Workspace root directory")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of markdown table")
    
    args = parser.parse_args()
    
    data = analyze_subscriptions(
        workspace_dir=args.workspace,
        days=args.days,
        start_date=args.start_date,
        end_date=args.end_date
    )
    
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(format_markdown_table(data))

if __name__ == "__main__":
    main()

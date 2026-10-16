"""Rank target companies by how strong your LinkedIn network is there.

Input: Connections.csv from LinkedIn's data export
  (Settings & Privacy > Data privacy > Get a copy of your data > Connections).

Usage:
  python network_map.py Connections.csv [-o report.md]
"""

import argparse
import csv
import io
import re
import sys
from collections import defaultdict
from datetime import datetime

from targets import TARGETS

# Strongest signal first: the first matching role decides a person's weight.
ROLE_RULES = [
    ("Recruiter", 3.0, r"recruit|talent|university|campus|people partner|sourcer"),
    ("PM", 3.0, r"product manag|\bpm\b|product lead|head of product|product director|vp,? product|group product|chief product|\bcpo\b"),
    ("Founder/Exec", 2.5, r"founder|\bceo\b|\bcto\b|\bcoo\b|chief|president|general manager"),
    ("Eng/Research", 2.0, r"engineer|developer|technical staff|research|scientist|\bml\b|architect|swe"),
    ("Design/GTM", 1.5, r"design|marketing|sales|account exec|solutions|forward deployed|customer success|partnership|operations|strategy|bizops"),
]
SENIOR = r"\b(head|director|vp|vice president|principal|staff|senior|sr\.?|lead|manager)\b"

SUFFIXES = r"\b(inc|incorporated|llc|ltd|corp|corporation|co|company|hq|pbc|gmbh|sas)\b"


def normalize(name):
    name = name.lower().replace("&", " and ")
    name = re.sub(r"\(.*?\)", " ", name)
    name = re.sub(r"[^a-z0-9 ]+", " ", name)
    name = re.sub(SUFFIXES, " ", name)
    return re.sub(r"\s+", " ", name).strip()


ALIAS_TO_TARGET = {}
for tier, company, aliases in TARGETS:
    for alias in aliases + [company]:
        ALIAS_TO_TARGET[normalize(alias)] = (tier, company)


def classify(position):
    pos = (position or "").lower()
    for label, weight, pattern in ROLE_RULES:
        if re.search(pattern, pos):
            break
    else:
        label, weight = "Other", 1.0
    if re.search(SENIOR, pos):
        weight += 0.5
    return label, weight


def parse_date(text):
    for fmt in ("%d %b %Y", "%Y-%m-%d", "%m/%d/%y", "%m/%d/%Y"):
        try:
            return datetime.strptime(text.strip(), fmt)
        except (ValueError, AttributeError):
            pass
    return None


def read_connections(path):
    with open(path, encoding="utf-8-sig") as f:
        lines = f.read().splitlines()
    # LinkedIn prepends a "Notes:" block before the real header row.
    start = next(i for i, line in enumerate(lines) if line.startswith("First Name"))
    return list(csv.DictReader(io.StringIO("\n".join(lines[start:]))))


def build(rows, now=None):
    now = now or datetime.now()
    hits = defaultdict(list)
    for r in rows:
        match = ALIAS_TO_TARGET.get(normalize(r.get("Company", "")))
        if not match:
            continue
        label, weight = classify(r.get("Position"))
        connected = parse_date(r.get("Connected On", ""))
        # Recent connections are warmer: full credit under 1 year, tapering to 0.6x.
        if connected:
            years = (now - connected).days / 365
            weight *= max(0.6, 1.0 - 0.1 * max(0.0, years - 1))
        hits[match].append({
            "name": f"{r.get('First Name', '')} {r.get('Last Name', '')}".strip(),
            "position": r.get("Position", ""),
            "url": r.get("URL", ""),
            "role": label,
            "weight": weight,
            "connected": connected,
        })

    results = []
    for tier, company, _ in TARGETS:
        people = sorted(hits.get((tier, company), []), key=lambda p: -p["weight"])
        score = sum(p["weight"] for p in people)
        roles = defaultdict(int)
        for p in people:
            roles[p["role"]] += 1
        results.append({
            "tier": tier, "company": company, "count": len(people),
            "score": round(score, 1), "roles": dict(roles), "people": people,
        })
    return results


def strength(score):
    if score >= 8:
        return "Strong"
    if score >= 3:
        return "Moderate"
    if score > 0:
        return "Thin"
    return "None (cold)"


def report(results, total_rows):
    ranked = sorted(results, key=lambda r: (-r["score"], r["tier"]))
    out = [
        "# Network strength across target companies",
        "",
        f"Scanned {total_rows} first-degree connections. Score weights each person by role "
        "(recruiters and PMs 3, founders and execs 2.5, engineers and researchers 2, "
        "design and GTM 1.5, other 1), adds 0.5 for seniority, and discounts "
        "connections made more than a year ago.",
        "",
        "## Ranking",
        "",
        "| # | Company | Tier | Strength | Score | Connections | PMs | Recruiters | Top contacts |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(ranked, 1):
        top = "; ".join(f"[{p['name']}]({p['url']}) ({p['position']})" for p in r["people"][:3]) or "—"
        out.append(
            f"| {i} | {r['company']} | {r['tier']} | {strength(r['score'])} | {r['score']} | "
            f"{r['count']} | {r['roles'].get('PM', 0)} | {r['roles'].get('Recruiter', 0)} | {top} |"
        )

    gaps = [r for r in results if r["tier"] == 1 and r["score"] < 3]
    out += ["", "## Tier 1 gaps (need Kellogg alumni or second-degree intros)", ""]
    out += [f"- **{r['company']}**: {strength(r['score']).lower()}, {r['count']} connection(s)" for r in gaps] or ["- None. Every Tier 1 company has a moderate or strong network."]

    out += ["", "## Everyone at your target companies", ""]
    for r in sorted(results, key=lambda r: (r["tier"], -r["score"])):
        if not r["people"]:
            continue
        out.append(f"### {r['company']} (Tier {r['tier']}, score {r['score']})")
        for p in r["people"]:
            when = p["connected"].strftime("%b %Y") if p["connected"] else "?"
            out.append(f"- [{p['name']}]({p['url']}): {p['position']} ({p['role']}, connected {when})")
        out.append("")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("connections_csv")
    ap.add_argument("-o", "--output", default="network_report.md")
    args = ap.parse_args()

    rows = read_connections(args.connections_csv)
    results = build(rows)
    with open(args.output, "w") as f:
        f.write(report(results, len(rows)))

    ranked = sorted(results, key=lambda r: (-r["score"], r["tier"]))
    print(f"{'Company':<22}{'Tier':>5}{'Score':>8}{'Conns':>7}  Strength")
    for r in ranked:
        if r["count"]:
            print(f"{r['company']:<22}{r['tier']:>5}{r['score']:>8}{r['count']:>7}  {strength(r['score'])}")
    cold = [r["company"] for r in ranked if not r["count"]]
    print(f"\nNo connections at {len(cold)} companies: {', '.join(cold)}")
    print(f"Full report: {args.output}")


if __name__ == "__main__":
    sys.exit(main())

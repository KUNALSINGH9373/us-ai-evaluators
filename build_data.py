"""Regenerate data.js and the site CSV from the project's final table. Run after phase8/build_outputs.py."""
import json, csv, re
P = "/Users/kunalsingh/research_projects/us-ai-evaluators-map"
T = json.load(open(f"{P}/phase8/final_table.json"))
DEVTYPES = r"(Funding from developer|Paid engagement by developer|Developer equity stake|Model access|In-kind support from developer|Research collaboration with developer|Equity stake in developer)"
G = "Google DeepMind (incl. Google, Alphabet, GV)"
NORM = {"Google": G, "Google DeepMind": G, "Alphabet": G, "Google LLC": G, "Meta Platforms, Inc.": "Meta", "NVIDIA Corporation": "NVIDIA",
        "Amazon.com, Inc.": "Amazon", "Amazon Web Services": "Amazon", "Apple, Inc.": "Apple", "xAI / SpaceX": "xAI"}
def developers(rel):
    names = set()
    for it in re.split(r";\s*(?=[A-Z][A-Za-z\- ]+:)", rel or ""):
        m = re.match(DEVTYPES + r"[^:]*:\s*([^(;]+)", it)
        if m:
            n = m.group(2).strip().rstrip(",")
            if "not named" not in n: names.add(NORM.get(n, n))
    return sorted(names)
def form(f):
    return f.split(" (")[0]
rows = []
for t in sorted(T, key=lambda x: x["organisation"].lower()):
    rows.append({"organisation": t["organisation"], "institutional_form": t["institutional_form"], "form": form(t["institutional_form"]),
                 "activity_assessed": t["activity_assessed"], "evaluation_evidence": t["evaluation_evidence"], "evidence_url": t["evidence_url"],
                 "evidence_author": "Organisation itself" if "organisation-authored" in t["evaluation_evidence"] else "Developer or other publisher",
                 "relationships": t["relationships"], "properties": t["properties"], "methods": t["methods"], "domains": t["domains"],
                 "relationship_types": t["relationship_types"], "developer_relationship": t["developer_relationship"],
                 "developers": developers(t["relationships"])})
open("data.js", "w").write("window.DATA=" + json.dumps(rows, ensure_ascii=False) + ";window.ASOF='10 October 2026';")
with open("us_ai_evaluators.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["Organisation", "Institutional form", "Activity assessed", "Evaluation evidence", "Evidence link", "Funding and relationships",
                "Properties", "Methods", "Domains", "Relationship types", "Developer relationship", "Developers named"])
    for r in rows:
        w.writerow([r["organisation"], r["institutional_form"], r["activity_assessed"], r["evaluation_evidence"], r["evidence_url"], r["relationships"],
                    "; ".join(r["properties"]), "; ".join(r["methods"]), "; ".join(r["domains"]), "; ".join(r["relationship_types"]),
                    r["developer_relationship"], "; ".join(r["developers"])])
print(len(rows), "rows")

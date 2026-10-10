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
    rows.append({"organisation": t["organisation"], "website": t["website"], "institutional_form": t["institutional_form"], "form": form(t["institutional_form"]),
                 "activity_assessed": t["activity_assessed"], "evaluation_evidence": t["evaluation_evidence"], "evidence_url": t["evidence_url"],
                                  "relationships": t["relationships"], "properties": t["properties"], "methods": t["methods"], "domains": t["domains"],
                 "relationship_types": t["relationship_types"], "developer_relationship": t["developer_relationship"],
                 "developers": developers(t["relationships"]), "contact": t["contact"], "contact_emails": t["contact_emails"], "contact_form": t["contact_form"],
                 "known_as": t["known_as"], "aliases": t["aliases"], "controlled_by": t["controlled_by"], "controller_row": t["controller_row"],
                 "sector": t["sector"], "legal_form": t["legal_form"], "tax_status": t["tax_status"], "designation": t["designation"], "operator": t["operator"],
                 "relationship_items": t["relationship_items"], "other_evaluations": t["other_evaluations"], "roles": t["roles"],
                 "publisher_type": t["roles"]["published_by_type"] if t["roles"]["published_by_type"] != "Not yet checked"
                 else ("Evaluating organisation" if "organisation-authored" in t["evaluation_evidence"] else "Developer, government or other publisher")})
INDEP = len(rows) - sum(1 for r in rows if r["controller_row"])
open("data.js", "w").write("window.DATA=" + json.dumps(rows, ensure_ascii=False) + f";window.ASOF='10 October 2026';window.INDEP={INDEP};")
import shutil, os
for src, dst in [("us_ai_evaluators_relationships_2026-10-10.csv", "us_ai_evaluators_relationships.csv")]:
    if os.path.exists(f"{P}/deliverables/{src}"): shutil.copy(f"{P}/deliverables/{src}", dst)
with open("us_ai_evaluators.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["Organisation", "Also known as", "Website", "Controlled by", "Sector", "Legal form", "Tax status", "Federal designation", "Operator or fiscal sponsor",
                "Activity assessed (in the selected publication)", "Recent evaluation publication", "Publication link", "Conducted by", "Published by", "Publisher type",
                "Commissioned or paid by", "Publication control", "Other evaluation publications", "Funding and relationships", "Relationship sources",
                "Properties", "Methods", "Domains", "Relationship types", "Developer relationship", "Developers named", "Contact"])
    for r in rows:
        ro = r["roles"]
        w.writerow([r["organisation"], r["known_as"], r["website"], r["controlled_by"], r["sector"], r["legal_form"], r["tax_status"], r["designation"], r["operator"],
                    r["activity_assessed"], r["evaluation_evidence"], r["evidence_url"], ro["conducted_by"], ro["published_by"], ro["published_by_type"],
                    ro["commissioned_by"], ro["publication_control"], "; ".join(f"{o['title']} <{o['url']}>" for o in r["other_evaluations"]), r["relationships"],
                    " | ".join(f"{i['text']} <{' '.join(s['url'] for s in i['sources']) or i.get('data_file') or 'sources checked: ' + i.get('scope', '')}>" for i in r["relationship_items"]),
                    "; ".join(r["properties"]), "; ".join(r["methods"]), "; ".join(r["domains"]), "; ".join(r["relationship_types"]),
                    r["developer_relationship"], "; ".join(r["developers"]), r["contact"]])
print(len(rows), "rows")

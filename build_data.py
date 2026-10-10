"""Regenerate data.js and the CSV from the project's final table. Run after phase8/build_outputs.py."""
import json, shutil
P = "/Users/kunalsingh/research_projects/us-ai-evaluators-map"
T = json.load(open(f"{P}/phase8/final_table.json"))
keep = ["organisation", "institutional_form", "activity_assessed", "evaluation_evidence", "evidence_url", "relationships",
        "properties", "methods", "domains", "relationship_types", "developer_relationship", "status"]
rows = [{k: t[k] for k in keep} for t in sorted(T, key=lambda x: x["organisation"].lower())]
open("data.js", "w").write("window.DATA=" + json.dumps(rows, ensure_ascii=False) + ";window.ASOF='10 October 2026';")
shutil.copy(f"{P}/deliverables/us_ai_evaluators_2026-10-10.csv", "us_ai_evaluators.csv")
print(len(rows), "rows")

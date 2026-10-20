"""Validate portable internal links, source pagination and exercise integrity."""
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
S=ROOT/"skills/shi-metal-materials-heat-treatment"
errors=[]
entries=json.loads((S/"exercises/index.json").read_text(encoding="utf-8"))
expected={0:6,1:14,2:21,3:17,4:20,5:55,6:25,7:11,8:6,9:9}
ids=[x["id"] for x in entries]
if len(ids)!=184 or len(set(ids))!=184:errors.append("Exercise IDs missing or duplicated")
for ch,n in expected.items():
    actual={x["number"] for x in entries if x["chapter"]==ch}
    if actual!=set(range(1,n+1)):errors.append(f"Chapter {ch} question sequence incomplete")
for x in entries:
    page=ROOT/"skills/shi-metal-materials-heat-treatment"/x["file"]
    text=page.read_text(encoding="utf-8")
    if len(re.findall(r"^## "+re.escape(x["id"])+r" ",text,re.M))!=1:errors.append(f"Missing/duplicate section for {x['id']}")
    p,q=x["pdf_pages"];a,b=x["printed_pages"]
    if p-8!=a or q-8!=b or not 10<=p<=q<=24:errors.append(f"Bad pagination: {x['id']}")
for f in ROOT.rglob("*.md"):
    if ".git" in f.parts:continue
    text=f.read_text(encoding="utf-8")
    for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)",text):
        target=target.split("#")[0]
        if not target or "://" in target or target.startswith("mailto:"):continue
        if not (f.parent/target).resolve().exists():errors.append(f"Broken link {f.relative_to(ROOT)}: {target}")
for f in ROOT.rglob("*"):
    if ".git" in f.parts or not f.is_file():continue
    if f.suffix.lower() in {".pdf",".png",".jpg",".jpeg",".epub"}:errors.append(f"Source/media accidentally packaged: {f.relative_to(ROOT)}")
    if f.name in {"full_text.txt","combined.txt","textbook.txt","workbook.txt"}:errors.append(f"OCR corpus accidentally packaged: {f.relative_to(ROOT)}")
if errors:
    print("\n".join(errors));raise SystemExit(1)
summary={"status":"passed","exercises":len(entries),"chapters":len(list((S/"chapters").glob("*.md"))),"labs":len(list((S/"labs").glob("lab*.md"))),"flagged_questions":sum(x["status"]!="解题要点" for x in entries),"markdown_files":len(list(S.rglob("*.md")))}
print(json.dumps(summary,ensure_ascii=True,indent=2))

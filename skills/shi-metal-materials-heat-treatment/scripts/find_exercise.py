"""Read-only local lookup by question ID (e.g. 5-40) or keyword."""
import json
import re
import sys
from pathlib import Path


def main():
    if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
    root=Path(__file__).resolve().parents[1]
    entries=json.loads((root/"exercises/index.json").read_text(encoding="utf-8"))
    query=" ".join(sys.argv[1:]).strip()
    if not query:raise SystemExit("Usage: python find_exercise.py 5-40 | keyword")
    matches=[x for x in entries if x["id"]==query] if re.fullmatch(r"[0-9]+-[0-9]+",query) else [x for x in entries if query.casefold() in (x["topic"]+x["status"]).casefold()]
    if not matches:raise SystemExit("No matching question")
    for x in matches:
        text=(root/x["file"]).read_text(encoding="utf-8")
        pattern=r"^## "+re.escape(x["id"])+r" .+?(?=^## |\Z)"
        section=re.search(pattern,text,re.M|re.S)
        print(json.dumps(x,ensure_ascii=False))
        print(section.group(0).strip() if section else "Indexed section not found")
        print()


if __name__=="__main__":main()

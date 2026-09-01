# -*- coding: utf-8 -*-
"""dump 现象学 ch0-8 大纲（形态+环节标题+mode）"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

for n in range(0, 9):
    f = Path(f"notes_pheno/ch{n}.json")
    if not f.exists():
        continue
    d = json.loads(f.read_text(encoding="utf-8"))
    print(f"########## ch{n}（title: {d.get('title','')[:40]}）mode: {d.get('mode','')[:40]} ##########")
    for g in d.get("gestalten", []):
        print(f"【形态】{g.get('name','')}（pages: {g.get('pages','')}）")
        for i, b in enumerate(g.get("bewegung", []), 1):
            sec = b[1] if len(b) > 1 else "?"
            print(f"  {i}. [{sec}] {b[0]}")
    print()

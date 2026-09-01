# -*- coding: utf-8 -*-
"""检查小逻辑 4 个 notes 的填充状态（gestalten/bewegung 数）"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

for name in ["vorbegriff", "sein", "essence", "begriff"]:
    f = Path(f"notes_lp/{name}.json")
    d = json.loads(f.read_text(encoding="utf-8"))
    print(f"=== {name}.json")
    for g in d.get("gestalten", []):
        nb = len(g.get("bewegung", []))
        filled = sum(1 for b in g.get("bewegung", []) if len(b) > 1)
        print(f"  形态: {g.get('name', '?')[:40]} | bewegung {nb}（有内容 {filled}）")
        if nb and filled:
            for b in g["bewegung"][:3]:
                print(f"    [{b[1]}] {b[0][:40]}")

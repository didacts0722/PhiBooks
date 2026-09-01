# -*- coding: utf-8 -*-
"""输出小逻辑 4 个 notes 的完整大纲（形态+环节标题）"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

for name in ["vorbegriff", "sein", "essence", "begriff"]:
    d = json.loads(Path(f"notes_lp/{name}.json").read_text(encoding="utf-8"))
    print(f"########## {name} ##########")
    for g in d.get("gestalten", []):
        print(f"【形态】{g.get('name')}（{g.get('pages','')}）")
        print(f"  mode: {g.get('mode','')[:80]}")
        for i, b in enumerate(g.get("bewegung", []), 1):
            print(f"  {i}. [{b[1]}] {b[0]}")
    print()

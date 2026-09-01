# -*- coding: utf-8 -*-
"""按马克思《法哲学批判》最终修正 staat_sec_map.json：
- §306 = 「Für die politische Stellung...Majorat/Erbgut」（马克思引用，原标305附释）
- §307 = 「Das Recht dieses Teils...durch die Geburt」（马克思 line594 引用）
- §308 = 「In den andern Teil...Abgeordnete」（马克思 line633 引用）+ 附释（alle einzeln）
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

F = Path("notes_recht/staat_sec_map.json")
m = json.loads(F.read_text(encoding="utf-8"))

m["c._Die_gesetzgebende_Gewalt.html"] = [
    298, 299, 299, 300, 301, 301, 302, 302, 303, 303, 304, 305,
    306, 307, 308, 308, 309, 310, 310, 311, 311, 312, 313, 314, 315, 316,
    317, 317, 317, 317, 317, 317, 317, 318, 319, 319, 320, 320, 320, 320, 320,
]

F.write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding="utf-8")
print("最终 map：")
for k, v in m.items():
    missing = [s for s in range(min(v), max(v) + 1) if s not in v]
    print(f"  {k}: {min(v)}-{max(v)}（{len(v)} 段）缺失={missing}")

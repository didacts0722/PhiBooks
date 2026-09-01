# -*- coding: utf-8 -*-
"""修正 staat_sec_map.json：§296/297、§306/307 归属（据马克思《法哲学批判》§296 引用文本确认）"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

F = Path("notes_recht/staat_sec_map.json")
m = json.loads(F.read_text(encoding="utf-8"))

# b._Regierungsgewalt：段14(Leidenschaftslosigkeit/Sitte)=§296（马克思批判引用证实）；
# 段15(Mittelstand)+段16(Rechtspflege)=§297
m["b._Die_Regierungsgewalt.html"] = [
    287, 288, 289, 289, 289, 290, 291, 292, 293, 294, 294,
    295, 295, 296, 297, 297,
]

# c._gesetzgebende：段14(Aufopferung/Geburt)=§306、段15(Abgeordnete)=§307（范扬译本对照）；
# 段16(alle einzeln/demokratisches Element)=§308
m["c._Die_gesetzgebende_Gewalt.html"] = [
    298, 299, 299, 300, 301, 301, 302, 302, 303, 303, 304, 305, 305,
    306, 307, 308, 309, 310, 310, 311, 311, 312, 313, 314, 315, 316,
    317, 317, 317, 317, 317, 317, 317, 318, 319, 319, 320, 320, 320, 320, 320,
]

F.write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding="utf-8")
print("已修正。各页覆盖：")
for k, v in m.items():
    print(f"  {k}: {min(v)}-{max(v)}（{len(v)} 段）")

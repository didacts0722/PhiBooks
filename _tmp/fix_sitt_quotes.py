# -*- coding: utf-8 -*-
"""修正 §166、§169 引文为原文逐字（对拍修复）"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

F = Path("notes_recht/sittlichkeit.json")
d = json.loads(F.read_text(encoding="utf-8"))
g = d["gestalten"][0]

fixes = {
    "Das eine ist daher das Geistige, als das sich Entzweiende in die für sich seiende persönliche Selbständigkeit und in das Wissen und Wollen der freien Allgemeinheit, in das Selbstbewußtsein des Denkens":
    "Das eine ist daher das Geistige, als das sich Entzweiende in die für sich seiende persönliche Selbständigkeit und in das Wissen und Wollen der freien Allgemeinheit, [in] das Selbstbewußtsein des begreifenden Gedankens und [in das] Wollen des objektiven Endzwecks",
    "Die Familie hat als Person ihre äußerliche Realität in einem Eigentum, in dem sie... für sich... ist":
    "Die Familie hat als Person ihre äußerliche Realität in einem Eigentum, in dem sie das Dasein ihrer substantiellen Persönlichkeit nur als in einem Vermögen hat",
}
n = 0
for b in g["bewegung"]:
    if b[2] in fixes:
        print(f"修复：{b[0]} [{b[1]}]")
        b[2] = fixes[b[2]]
        n += 1
F.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
json.loads(F.read_text(encoding="utf-8"))
print(f"修复 {n} 条，JSON 校验通过")

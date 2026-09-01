# -*- coding: utf-8 -*-
"""按 § 号稳定排序 sittlichkeit.json 的 bewegung（恢复书序——环节 22 §274 需在 §273 与 §279 之间）"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

F = Path("notes_recht/sittlichkeit.json")
d = json.loads(F.read_text(encoding="utf-8"))
g = d["gestalten"][0]
bw = g["bewegung"]

def secno(b):
    m = re.match(r"§(\d+)", b[1])
    return int(m.group(1)) if m else 0

order = [secno(b) for b in bw]
print("排序前 § 序：", order)
bad = sum(1 for a, b in zip(order, order[1:]) if b < a)
print(f"逆序对：{bad}")

bw.sort(key=secno)  # 稳定排序

order2 = [secno(b) for b in bw]
bad2 = sum(1 for a, b in zip(order2, order2[1:]) if b < a)
print(f"排序后 § 序：{order2}，逆序对：{bad2}")

F.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
json.loads(F.read_text(encoding="utf-8"))
print("JSON 校验通过，已按书序重排")

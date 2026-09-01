# -*- coding: utf-8 -*-
"""修正环节结构：group 移到第 7 位（index 6），supps/diagram 用 None 占位
（vorrede 规范：[标题, §, 引文, 正文, None, None, group]）"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

F = Path("notes_recht/sittlichkeit.json")
d = json.loads(F.read_text(encoding="utf-8"))
g = d["gestalten"][0]
bw = g["bewegung"]

fixed = 0
for i, b in enumerate(bw):
    if len(b) == 5:  # [标题, §, 引文, 正文, group]——group 位置错误
        bw[i] = [b[0], b[1], b[2], b[3], None, None, b[4]]
        fixed += 1
    elif len(b) == 4:  # 旧环节：无 supps/diagram/group——保持（默认空）
        pass
    elif len(b) == 7:
        pass
    else:
        print(f"!! 环节 {i + 1} 异常长度 {len(b)}: {b[0][:30]}")

F.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
json.loads(F.read_text(encoding="utf-8"))
print(f"修正 {fixed} 个环节，JSON 校验通过")
# 抽查
b = bw[13]
print(f"环节14 结构：len={len(b)} group={b[6] if len(b) > 6 else '?'}")
b = bw[31]
print(f"环节32 结构：len={len(b)} group={b[6] if len(b) > 6 else '?'}")

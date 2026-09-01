# -*- coding: utf-8 -*-
"""国家笔记广采来源审计标注：无本地原文的人名在广采段标注（2026-08-29 纪律）"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

F = Path("notes_recht/sittlichkeit.json")
d = json.loads(F.read_text(encoding="utf-8"))
bw = d["gestalten"][0]["bewegung"]

# 本地有原文（✓）：马克思/康德/柏拉图/亚里士多德/黑格尔/孟德斯鸠（文本内）/费希特（文本内）
# 本地无原文（待补）：霍布斯/洛克/卢梭/诺齐克/韦伯/施米特/斯宾格勒/汤因比/福山/萨义德/克劳塞维茨/西耶斯/吉登斯/巴特勒/泰勒
# 讨论材料有（M4）：贡斯当
NONLOCAL = ["霍布斯", "洛克", "卢梭", "诺齐克", "韦伯", "施米特", "斯宾格勒", "汤因比", "福山",
            "萨义德", "克劳塞维茨", "西耶斯", "吉登斯", "巴特勒", "泰勒", "霍耐特"]

n_sec = 0
for b in bw:
    sec = int(re.match(r"§(\d+)", b[1]).group(1))
    if sec < 257:
        continue
    txt = b[3]
    # 找广采段标记
    m = re.search(r"\*\*M7 广采\*\*|\*\*广采\*\*", txt)
    if not m:
        continue
    found = [nm for nm in NONLOCAL if nm in txt]
    if not found:
        continue
    # 在广采标记后插入审计注
    mark = m.group(0)
    note = (f"{mark}〔来源审计 2026-08-29：本段广采中 {'/'.join(found)} 本地文献库无原文，"
            f"仅作对照锚提示，待补原文后复核——广采纪律见注释规范〕")
    b[3] = txt.replace(mark, note, 1)
    n_sec += 1
    print(f"标注 {b[1]} {b[0][:22]}: {found}")

F.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
json.loads(F.read_text(encoding="utf-8"))
print(f"\n标注 {n_sec} 个环节，JSON 校验通过")

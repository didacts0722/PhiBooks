# -*- coding: utf-8 -*-
"""重排 bewegung 为 § 书序（贱民 §244 移到同业公会 §253 之前）+ 互换关键点⑪⑫ 编号"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

F = Path("notes_recht/sittlichkeit.json")
d = json.loads(F.read_text(encoding="utf-8"))
g = d["gestalten"][0]
bw = g["bewegung"]

# 定位：同业公会（§253）、贱民（§244）
i_korp = next(i for i, b in enumerate(bw) if b[1] == "§253")
i_pobel = next(i for i, b in enumerate(bw) if b[1] == "§244")
print(f"重排前：同业公会@{i_korp}，贱民@{i_pobel}")
assert abs(i_korp - i_pobel) == 1, "两者必须相邻"

# 互换位置（贱民在前，同业公会在后——§ 书序）
bw[i_korp], bw[i_pobel] = bw[i_pobel], bw[i_korp]

# 互换正文中的关键点编号：同业公会 ⑪→⑫，贱民 ⑫→⑪
for b in bw:
    if b[1] == "§253":  # 同业公会
        b[3] = b[3].replace("关键点⑪：同业公会", "关键点⑫：同业公会").replace("判断（展开④）", "判断（展开⑤）")
    if b[1] == "§244":  # 贱民
        b[3] = b[3].replace("关键点⑫：贱民", "关键点⑪：贱民")

F.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
json.loads(F.read_text(encoding="utf-8"))
print("重排后顺序：")
for i, b in enumerate(bw, 1):
    print(f"  {i}: {b[0]} [{b[1]}]")
print("JSON 校验通过")

# -*- coding: utf-8 -*-
"""统计国家部分大纲的 § 引文覆盖：大纲中德文引文（*...*）出现的 § vs §257-360 总数"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

doc = Path("docs/法哲学_国家_大纲_概念链演绎链.md").read_text(encoding="utf-8")

# 大纲中所有明确出现的 § 号
sec_refs = sorted(set(int(x) for x in re.findall(r"§\s*(\d+)", doc)))
in_range = [s for s in sec_refs if 257 <= s <= 360]
print(f"大纲中出现的 § 号：{len(sec_refs)} 个（国家范围 {len(in_range)} 个）")
print(f"§257-360 共 104 个 §，大纲逐 § 提及 {len(in_range)} 个 = {len(in_range)/104*100:.0f}%")

# 德文引文（*...*）所在行的 § 引用（取该行最先出现的 §）
quotes = []
for line in doc.splitlines():
    if "*" in line and "§" in line:
        m = re.findall(r"§\s*(\d+)", line)
        if m:
            quotes.append(int(m[0]))
q_secs = sorted(set(q for q in quotes if 257 <= q <= 360))
print(f"含德文引文的行：{len(quotes)} 行，覆盖 §：{len(q_secs)} 个（{len(q_secs)/104*100:.0f}%）")
print(f"引文覆盖的 §：{q_secs}")

# 未覆盖的 §（104 - 引文覆盖）
missing = [s for s in range(257, 361) if s not in q_secs]
print(f"\n未覆盖 §（{len(missing)}）：{missing}")

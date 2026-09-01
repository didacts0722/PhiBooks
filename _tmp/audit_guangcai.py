# -*- coding: utf-8 -*-
"""审查国家大纲的广采/对照条目：标注本地文献库来源状态"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

doc = Path("docs/法哲学_国家_大纲_概念链演绎链.md").read_text(encoding="utf-8")

# 本地库：有原文的哲学家 + 观点库/讨论材料
LOCAL_RAW = ["马克思", "康德", "柏拉图", "亚里士多德", "谢林", "黑格尔", "斯宾诺莎",
             "费希特", "莱布尼茨", "笛卡尔", "休谟", "卢克莱修", "歌德", "席勒"]
LOCAL_DOC = ["霍耐特", "齐泽克", "拉康", "泰勒", "巴特勒", "吉登斯", "儒家", "韦伯"]  # 观点库/讨论材料有

# 提取广采/对照条目（含人名或流派的行）
PATTERNS = ["**M7 广采**", "**对照", "**广采", "对照锚", "**瓦解", "**半瓦解", "**部分瓦解", "参考"]
cands = {}
for line in doc.splitlines():
    if any(p in line for p in ["**M7 广采", "**对照", "**广采", "**瓦解", "**半瓦解", "**部分瓦解", "对照锚"]) and ("**" in line):
        cands.setdefault(line.strip()[:60], line)

print("=== 国家大纲广采/对照条目的人名提取 ===")
import collections
names = collections.Counter()
for line in doc.splitlines():
    if "**M7 广采" in line or line.strip().startswith("- **") and ("**" in line):
        for nm in re.findall(r"（([^）]{2,8})）|vs\s*([A-ZÄÖÜa-zäöüß]+)|（[^）]*([A-ZÄÖÜ][a-zäöüß]+)[^）]*）", line):
            pass
# 简化：列出所有含「**」的人名片段
hits = collections.Counter()
for line in doc.splitlines():
    for m in re.findall(r"\*\*([^*]{2,10}?)\*\*", line):
        if any(k in m for k in ["霍布斯", "洛克", "卢梭", "康德", "马克思", "韦伯", "施米特", "波普尔",
                                "斯宾格勒", "汤因比", "福山", "萨义德", "孟德斯鸠", "费希特", "柏拉图",
                                "亚里士多德", "西耶斯", "贡斯当", "霍耐特", "齐泽克", "泰勒", "诺齐克",
                                "自由主义", "共和主义", "和平主义", "东方主义", "国际法", "威斯特伐利亚",
                                "当代", "美国", "英国", "日本"]):
            hits[m] += 1
print("主要对照人物/流派出现次数：")
for k, v in hits.most_common(40):
    print(f"  {k}: {v}")

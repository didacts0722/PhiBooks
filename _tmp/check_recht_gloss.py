# -*- coding: utf-8 -*-
"""国家部分候选术语对照主表：命中（补 works）/缺失（新增）"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

gloss = json.loads(Path("viewpoints/glossary/黑格尔.json").read_text(encoding="utf-8"))
terms = gloss["terms"]
by_term = {t["term"].lower(): t for t in terms}

# 国家部分候选术语（从 sittlichkeit.json 环节 14-32 提取 + 手工补充核心概念）
d = json.loads(Path("notes_recht/sittlichkeit.json").read_text(encoding="utf-8"))
bw = d["gestalten"][0]["bewegung"]
staat = [b for b in bw if int(re.match(r"§(\d+)", b[1]).group(1)) >= 257]

# 从国家环节正文+引文提取德文词（*...* 中的词 + 大写名词）
texts = []
for b in staat:
    texts.append(b[2])  # 引文
    texts.append(b[3])  # 正文
full = " ".join(texts)
# 提取 *...* 内德文 + 正文中的德文术语候选（已知核心词列表）
CAND = [
    "Staat", "Monarch", "Monarchie", "Souveränität", "Volkssouveränität", "Verfassung",
    "Regierungsgewalt", "gesetzgebende Gewalt", "fürstliche Gewalt", "Korporation",
    "Mittelstand", "öffentliche Meinung", "Weltgeschichte", "Völkergeist", "Weltgeist",
    "Pöbel", "Krieg", "Tapferkeit", "Gesinnung", "Patriotismus", "Rechtspflege", "Gesetz",
    "Majorat", "Abgeordnete", "Stand", "Stände", "Geburt", "Thronfolge", "Legitimität",
    "Majestät", "Begnadigungsrecht", "Gewissen", "Hierarchie", "Beamte", "Bürokratie",
    "Volk", "Heroenrecht", "Theokratie", "Pietät", "Sittlichkeit", "Ehe", "Erbrecht",
    "Privatstand", "Genossenschaft", "Zutrauen", "Anerkanntsein", "Naturzustand", "Traktat",
    "Völkerrecht", "ewiger Friede", "Individualität", "Entzweiung", "Idealität",
]
print("=== 主表缺失（需新增）===")
miss = []
for c in CAND:
    if c.lower() not in by_term:
        miss.append(c)
print(miss)

print("\n=== 主表已有（补 works=法哲学）===")
hit = []
for c in CAND:
    if c.lower() in by_term:
        hit.append(c)
print(hit)

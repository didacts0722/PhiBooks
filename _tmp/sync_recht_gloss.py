# -*- coding: utf-8 -*-
"""术语沉淀：法哲学（含国家部分）术语并入主表
1. 新增 44 个缺失术语（works 按三书搜索确认）
2. 9 个已有术语补 works=法哲学
3. HTML 107 个首次术语补 works=法哲学
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

G = Path("viewpoints/glossary/黑格尔.json")
gloss = json.loads(G.read_text(encoding="utf-8"))
terms = gloss["terms"]
by_term = {t["term"].lower(): t for t in terms}

# 1) 新增 44 个术语（zh 翻译；works 按三书搜索）
NEW = [
    # (term, zh, works)
    ("Monarch", "君主", ["法哲学", "精神现象学"]),
    ("Monarchie", "君主制", ["法哲学"]),
    ("Souveränität", "主权", ["法哲学", "精神现象学"]),
    ("Volkssouveränität", "人民主权", ["法哲学"]),
    ("Verfassung", "宪法/政制", ["法哲学"]),
    ("Regierungsgewalt", "政府权", ["法哲学"]),
    ("gesetzgebende Gewalt", "立法权", ["法哲学"]),
    ("fürstliche Gewalt", "君主权（王权）", ["法哲学"]),
    ("Korporation", "同业公会", ["法哲学"]),
    ("Mittelstand", "中等阶级", ["法哲学"]),
    ("öffentliche Meinung", "公共舆论", ["法哲学"]),
    ("Weltgeschichte", "世界历史", ["法哲学", "精神现象学"]),
    ("Völkergeist", "民族精神", ["法哲学", "精神现象学"]),
    ("Pöbel", "贱民", ["法哲学"]),
    ("Krieg", "战争", ["法哲学", "小逻辑", "精神现象学"]),
    ("Tapferkeit", "勇气/英勇", ["法哲学", "精神现象学"]),
    ("Patriotismus", "爱国主义", ["法哲学"]),
    ("Rechtspflege", "司法/法律维护", ["法哲学"]),
    ("Majorat", "长子继承制", ["法哲学"]),
    ("Abgeordnete", "代表", ["法哲学"]),
    ("Stand", "等级/身份", ["法哲学", "小逻辑", "精神现象学"]),
    ("Geburt", "出生", ["法哲学", "精神现象学"]),
    ("Thronfolge", "王位继承", ["法哲学"]),
    ("Legitimität", "合法性/正当性", ["法哲学"]),
    ("Majestät", "尊严/威仪", ["法哲学", "小逻辑", "精神现象学"]),
    ("Begnadigungsrecht", "赦免权", ["法哲学"]),
    ("Hierarchie", "等级制/科层制", ["法哲学"]),
    ("Beamte", "官员", ["法哲学"]),
    ("Bürokratie", "官僚制", ["法哲学"]),
    ("Heroenrecht", "英雄权利", ["法哲学"]),
    ("Theokratie", "神权政体", ["法哲学"]),
    ("Pietät", "虔敬/孝道", ["法哲学", "精神现象学"]),
    ("Ehe", "婚姻", ["法哲学", "精神现象学"]),
    ("Erbrecht", "继承权", ["法哲学"]),
    ("Privatstand", "私人等级", ["法哲学"]),
    ("Genossenschaft", "同业团体", ["法哲学"]),
    ("Zutrauen", "信任", ["法哲学"]),
    ("Anerkanntsein", "被承认", ["法哲学", "精神现象学"]),
    ("Naturzustand", "自然状态", ["法哲学"]),
    ("Traktat", "条约", ["法哲学", "小逻辑"]),
    ("Völkerrecht", "国际法", ["法哲学"]),
    ("ewiger Friede", "永恒和平", ["法哲学"]),
    ("Idealität", "理想性", ["法哲学", "小逻辑"]),
]
added = 0
for term, zh, works in NEW:
    key = term.lower()
    if key in by_term:  # 已有（检查漏网）——补 works
        for w in works:
            if w not in by_term[key]["works"]:
                by_term[key]["works"].append(w)
        continue
    terms.append({"term": term, "zh": zh, "canonical": True, "works": works})
    by_term[key] = terms[-1]
    added += 1
print(f"新增 {added} 条")

# 2) 9 个已有术语补 works=法哲学（Staat/Weltgeist/Gesinnung/Gesetz/Gewissen/Volk/Sittlichkeit/Individualität/Entzweiung）
HIT9 = ["Staat", "Weltgeist", "Gesinnung", "Gesetz", "Gewissen", "Volk", "Sittlichkeit",
        "Individualität", "Entzweiung"]
for t in HIT9:
    key = t.lower()
    if key in by_term and "法哲学" not in by_term[key]["works"]:
        by_term[key]["works"].append("法哲学")
print("9 个已有术语补 works=法哲学")

# 3) HTML 107 个首次术语补 works=法哲学
html = Path(r"笔记/法哲学原理_注释版.html").read_text(encoding="utf-8")
firsts = set()
for m in re.finditer(r'<span class="gt"><i>([^<]+)</i><sup class="gt-first"', html):
    firsts.add(m.group(1))
n3 = 0
for t in firsts:
    key = t.lower()
    if key in by_term and "法哲学" not in by_term[key]["works"]:
        by_term[key]["works"].append("法哲学")
        n3 += 1
print(f"HTML 首次术语补 works=法哲学：{n3} 条（共 {len(firsts)} 个首次术语）")

gloss["updated"] = "2026-08-29"
G.write_text(json.dumps(gloss, ensure_ascii=False, indent=1), encoding="utf-8")
json.loads(G.read_text(encoding="utf-8"))
print(f"主表更新完成：共 {len(terms)} 条")
from collections import Counter
print("works 分布:", dict(Counter(w for t in terms for w in t.get("works", []))))

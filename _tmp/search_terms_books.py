# -*- coding: utf-8 -*-
"""搜索 44 个新增术语在现象学/小逻辑原文中的出现（确定 works 标注）"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PHENO = Path(r"原文/黑格尔/Phänomenologie_des_Geistes/extracted/phenomenologie_all.txt")
ENZ = Path(r"原文/黑格尔/Enzyklopädie_Logik/extracted/enzyklopaedie_logik_all.txt")

pheno = PHENO.read_text(encoding="utf-8") if PHENO.exists() else ""
enz = ENZ.read_text(encoding="utf-8") if ENZ.exists() else ""
print(f"现象学文本 {len(pheno)} 字符，小逻辑文本 {len(enz)} 字符\n")

MISS = ["Monarch", "Monarchie", "Souveränität", "Volkssouveränität", "Verfassung",
        "Regierungsgewalt", "gesetzgebende Gewalt", "fürstliche Gewalt", "Korporation",
        "Mittelstand", "öffentliche Meinung", "Weltgeschichte", "Völkergeist", "Pöbel",
        "Krieg", "Tapferkeit", "Patriotismus", "Rechtspflege", "Majorat", "Abgeordnete",
        "Stand", "Geburt", "Thronfolge", "Legitimität", "Majestät", "Begnadigungsrecht",
        "Hierarchie", "Beamte", "Bürokratie", "Heroenrecht", "Theokratie", "Pietät",
        "Ehe", "Erbrecht", "Privatstand", "Genossenschaft", "Zutrauen", "Anerkanntsein",
        "Naturzustand", "Traktat", "Völkerrecht", "ewiger Friede", "Idealität"]

print("=== 术语在三书中的分布 ===")
for t in MISS:
    in_p = t in pheno
    in_e = t in enz
    mark = ("现象学" if in_p else "") + ("+" if in_p and in_e else "") + ("小逻辑" if in_e else "")
    print(f"  {t}: {mark or '仅法哲学'}")

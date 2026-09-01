# -*- coding: utf-8 -*-
"""检查内部国家法相关 JSON 的 items 结构"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

EX = Path(r"原文/黑格尔/Grundlinien_der_Philosophie_des_Rechts/extracted")
for name in ["I._Innere_Verfassung_für_sich.json", "a._Die_fürstliche_Gewalt.json",
             "A._Das_Innere_Staatsrecht.json", "Das_Innere_Staatsrecht.json"]:
    d = json.loads((EX / name).read_text(encoding="utf-8-sig"))
    print(f"=== {name}（{len(d['items'])} items）===")
    for it in d["items"][:14]:
        print(f"  {it['type']}: {(it.get('text') or '')[:80]}")
    print()

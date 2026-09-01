# -*- coding: utf-8 -*-
"""打印 §166、§169 原文（逐字，供引文修正）"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

idx = json.loads(Path(r"原文/黑格尔/Grundlinien_der_Philosophie_des_Rechts/extracted/Grundlinien_der_Philosophie_des_Rechts_index.json").read_text(encoding="utf-8-sig"))
for pg in idx:
    cur = None
    for it in pg.get("items", []):
        if it["type"] in ("h4", "h5"):
            m = re.match(r"§\s*(\d+)", it["text"])
            if m:
                cur = int(m.group(1))
        elif it["type"] == "p" and cur in (166, 169):
            print(f"--- §{cur} p.{it.get('page')} {pg.get('file')} ---")
            print(it["text"])
            print()

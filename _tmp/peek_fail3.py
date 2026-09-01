# -*- coding: utf-8 -*-
"""提取 8 个失败 § 的全部段落（逐字），供主引文修正"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

idx = json.loads(Path(r"原文/黑格尔/Grundlinien_der_Philosophie_des_Rechts/extracted/Grundlinien_der_Philosophie_des_Rechts_index.json").read_text(encoding="utf-8-sig"))
sec_map = json.loads(Path("notes_recht/staat_sec_map.json").read_text(encoding="utf-8"))

sec_texts = {}
for pg in idx:
    cur = None
    mapped = sec_map.get(pg.get("file"))
    mi = 0
    for it in pg.get("items", []):
        if it["type"] in ("h4", "h5"):
            m = re.match(r"§\s*(\d+)", it["text"])
            cur = int(m.group(1)) if m else cur
        elif it["type"] == "p":
            sec_use = mapped[mi] if mapped and mi < len(mapped) else cur
            if mapped:
                mi += 1
            if sec_use:
                sec_texts.setdefault(sec_use, []).append(it["text"])

for sec in [273, 279, 298, 302, 316, 324, 331, 333]:
    print(f"===== §{sec} =====")
    for t in sec_texts.get(sec, []):
        print(" ".join(t.split()))
        print("  ---")

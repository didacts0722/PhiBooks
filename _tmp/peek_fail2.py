# -*- coding: utf-8 -*-
"""直接从原文 JSON 提取失败 § 的完整段落"""
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

fails = [268, 269, 281, 300, 305, 306, 310, 314, 319]
for sec in fails:
    print(f"===== §{sec} =====")
    for t in sec_texts.get(sec, ["（无）"]):
        print(" ".join(t.split())[:450])
        print()

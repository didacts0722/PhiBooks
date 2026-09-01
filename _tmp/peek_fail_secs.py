# -*- coding: utf-8 -*-
"""提取失败 § 的原文完整段落（供引文逐字修正）"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

fails = [268, 269, 281, 300, 305, 306, 310, 314, 319, 350, 351, 352, 353, 360]
for fn in ["_tmp/gs_s257_360.txt", "_tmp/staat_s260_329.txt"]:
    txt = Path(fn).read_text(encoding="utf-8")
    for sec in fails:
        for m in re.finditer(rf"\[§{sec}\|([^\]]*)\] (.*?)(?=\n\n\[§|\Z)", txt, re.S):
            head = m.group(1)
            body = " ".join(m.group(2).split())
            print(f"--- §{sec} [{head}] ---")
            print(body[:400])
            print()

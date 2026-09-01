# -*- coding: utf-8 -*-
"""统计法哲学原文中战争（Krieg）论述的 § 分布"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

idx = json.loads(Path(r"原文/黑格尔/Grundlinien_der_Philosophie_des_Rechts/extracted/Grundlinien_der_Philosophie_des_Rechts_index.json").read_text(encoding="utf-8-sig"))

# 构建 § -> 段落文本（书序，含 §260-329 映射）
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

# 统计 Krieg 相关词
kw = re.compile(r"Krieg|kriegerisch|Tapferkeit|stehendes Heer|Waffen|Feuergewehr|Feind", re.I)
hits = []
for sec in sorted(sec_texts):
    for t in sec_texts[sec]:
        ms = kw.findall(t)
        if ms:
            hits.append((sec, len(ms), t[:90].replace("\n", " ")))
print(f"含战争词的段落：{len(hits)} 段，分布于 {len(set(h[0] for h in hits))} 个 §\n")
cur_sec = None
for sec, n, head in hits:
    if sec != cur_sec:
        print(f"--- §{sec} ---")
        cur_sec = sec
    print(f"  [{n}] {head}")

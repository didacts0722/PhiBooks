# -*- coding: utf-8 -*-
"""找出 sittlichkeit.json 对拍失败的引文（与 build_recht 同一逻辑）"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, ".")
import build_pheno_ch123 as P  # noqa: E402

IDX = Path(r"原文/黑格尔/Grundlinien_der_Philosophie_des_Rechts/extracted/Grundlinien_der_Philosophie_des_Rechts_index.json")
sec_map = json.loads(Path("notes_recht/staat_sec_map.json").read_text(encoding="utf-8"))
idx = json.loads(IDX.read_text(encoding="utf-8-sig"))


def paras_range(lo, hi):
    raw = []
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
                if sec_use and lo <= sec_use <= hi:
                    raw.append(it["text"])
    return raw


meta = json.loads(Path("notes_recht/sittlichkeit.json").read_text(encoding="utf-8"))
paras = paras_range(142, 360)
norm_paras = [P.norm(p) for p in paras]
for g in meta["gestalten"]:
    for b in g["bewegung"]:
        q = P.norm(b[2])
        if not any(q.lower() in np.lower() for np in norm_paras):
            print(f"[FAIL] {b[1]} | {b[0]}")
            print(f"   {q[:160]}")
            print()

# -*- coding: utf-8 -*-
"""找出对拍失败的引文（与 build_recht 同一逻辑）"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
IDX = ROOT / "原文" / "黑格尔" / "Grundlinien_der_Philosophie_des_Rechts" / "extracted" / "Grundlinien_der_Philosophie_des_Rechts_index.json"
import build_pheno_ch123 as P

idx = json.loads(IDX.read_text(encoding="utf-8-sig"))


def paras_range(lo, hi):
    vor, sec = [], []
    if lo == 1:
        for pg in idx:
            if pg.get("file") != "Vorrede.html":
                continue
            for it in pg.get("items", []):
                if it["type"] == "p":
                    vor.append(it["text"])
    for pg in idx:
        cur = None
        for it in pg.get("items", []):
            if it["type"] in ("h4", "h5"):
                m = re.match(r"§\s*(\d+)", it["text"])
                cur = int(m.group(1)) if m else cur
            elif it["type"] == "p" and cur and lo <= cur <= hi:
                sec.append(it["text"])
    return vor + sec


for name in ["vorrede", "abstrakt", "moral", "sittlich"]:
    cfg = {
        "vorrede": ("vorrede_einleitung.json", 1, 33),
        "abstrakt": ("abstraktes_recht.json", 34, 104),
        "moral": ("moralitaet.json", 105, 141),
        "sittlich": ("sittlichkeit.json", 142, 360),
    }[name]
    meta = json.loads((ROOT / "notes_recht" / cfg[0]).read_text(encoding="utf-8"))
    paras = paras_range(cfg[1], cfg[2])
    norm_paras = [P.norm(p) for p in paras]
    for g in meta["gestalten"]:
        for b in g["bewegung"]:
            q = P.norm(b[2])
            if not any(q.lower() in np.lower() for np in norm_paras):
                print(f"[FAIL] {name} | {b[1]} | {b[0]}")
                print(f"  引文：{q[:200]}")
                print()
print("done")

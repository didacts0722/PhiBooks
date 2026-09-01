# -*- coding: utf-8 -*-
"""dump §260-329 全部段落（7 页，书序），输出 _tmp/staat_s260_329.txt"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, ".")
from extract_zeno import extract_page  # noqa: E402

OUT = Path(r"原文/黑格尔/Grundlinien_der_Philosophie_des_Rechts")
PAGES = [
    "Das_Innere_Staatsrecht.html",          # §260-271
    "Innere_Verfassung_für_sich.html",      # §272-274
    "a._Die_fürstliche_Gewalt.html",        # §275-286
    "b._Die_Regierungsgewalt.html",         # §287-297
    "c._Die_gesetzgebende_Gewalt.html",     # §298-320
    "II._Die_Souveränität_gegen_außen.html",  # §321-329
]
lines = []
for fn in PAGES:
    d = extract_page(OUT / fn)
    for it in d["items"]:
        if it["type"] == "p":
            lines.append(f"[{fn} | p.{it.get('page')}] {it['text']}")
out = Path("_tmp/staat_s260_329.txt")
out.write_text("\n\n".join(lines), encoding="utf-8")
print(f"写出 {len(lines)} 段 -> {out}")

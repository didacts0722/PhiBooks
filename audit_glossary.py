# -*- coding: utf-8 -*-
"""术语缺口审计：扫描 ch1-8 环节引文+笔记文本里的德语词（高频候选），
与术语主表比对，列出高频且缺失的词，供人工裁定补充。"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
NOTES = ROOT / "项目/现象学/notes"

WORD_RE = re.compile(r"\b[A-ZÄÖÜ][a-zäöüß]+(?:[A-ZÄÖÜa-zäöüß-]*[a-zäöüß])?\b")
STOP = {
    "der", "die", "das", "den", "dem", "des", "ein", "eine", "eines", "einer", "einem",
    "und", "oder", "aber", "als", "wie", "so", "nur", "auch", "nicht", "ist", "sind",
    "war", "wird", "werden", "hat", "haben", "sein", "sich", "ihr", "ihre", "ihrer",
    "sie", "er", "es", "ich", "wir", "uns", "man", "was", "wer", "welche", "welcher",
    "welches", "dies", "diese", "dieser", "dieses", "jene", "jener", "jenes", "von",
    "mit", "in", "im", "auf", "an", "aus", "bei", "zu", "für", "über", "unter",
    "nach", "vor", "durch", "gegen", "ohne", "um", "bis", "da", "dort", "hier",
    "dann", "denn", "wenn", "weil", "indem", "ob", "doch", "auch", "zwar", "viel",
    "viele", "aller", "alle", "alles", "jeder", "jedes", "kein", "keine", "eben",
    "selbst", "selber", "sondern", "dass", "daß", "zum", "zur", "vom", "beim", "am",
    "als", "oder", "wie", "noch", "schon", "immer", "nie", "nichts", "etwas",
    "mehr", "weniger", "ganz", "gar", "schlecht", "gut", "groß", "klein", "neu",
    "alt", "erste", "ersten", "zweite", "dritte", "ihm", "ihn", "ihnen", "mich",
    "dich", "unsere", "unserer", "euch", "ihnen", "ihm", "mein", "dein",
    "welchem", "welchem", "wodurch", "womit", "worin", "woraus", "worauf", "wobei",
    "woran", "darin", "daran", "daraus", "darauf", "dabei", "damit", "dazu",
    "dadurch", "dagegen", "hierin", "hieran", "hieraus", "hierbei", "hierzu",
    "hiermit", "hierdurch", "ebenso", "ebensowohl", "ebensosehr", "gleichfalls",
    "gleichsam", "schlechthin", "freilich", "übrigens", "vielleicht", "eigentlich",
    "nämlich", "nun", "nur", "also", "somit", "insofern", "inwiefern", "nicht",
    "keineswegs", "gleichwohl", "vielmehr", "sonst", "ferner", "weiter", "weiterhin",
    "einerseits", "andererseits", "einesteils", "andernteils", "zunächst",
    "zuvörderst", "endlich", "letztlich", "wesentlich", "notwendig", "unmittelbar",
    "unmittelbare", "unmittelbaren", "unmittelbares", "unmittelbarer", "unmittelbarkeit",
}

def main():
    freq = Counter()
    for n in range(1, 9):
        p = NOTES / f"ch{n}.json"
        if not p.exists():
            continue
        data = json.loads(p.read_text(encoding="utf-8"))
        texts = []
        for g in data.get("gestalten", []):
            texts.append(g.get("bestimmung", ""))
            texts.append(g.get("diagnose", ""))
            texts.append(g.get("uebergang", ""))
            for b in g.get("bewegung", []):
                texts.append(b[2] if len(b) > 2 else "")
                texts.append(b[3] if len(b) > 3 else "")
                if len(b) > 4 and isinstance(b[4], list):
                    for s in b[4]:
                        texts.append(s.get("content", ""))
        for t in texts:
            for w in WORD_RE.findall(t):
                k = w.lower()
                if k in STOP or len(w) < 4:
                    continue
                freq[k] += 1
    gloss = json.loads((ROOT / "viewpoints" / "glossary" / "黑格尔.json").read_text(encoding="utf-8"))
    have = {e["term"].lower() for e in gloss["terms"]}
    missing = [(w, c) for w, c in freq.most_common(400) if w not in have]
    print(f"主表 {len(have)} 条；高频缺失候选（按频率，前 80）：")
    for w, c in missing[:80]:
        print(f"  {w:<32} ×{c}")


if __name__ == "__main__":
    main()

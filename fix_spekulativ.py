# -*- coding: utf-8 -*-
"""spekulativ 译法修正：黑格尔语境下 = 思辨的（在思维中推演）。
把笔记里把 spekulativ 注释为「重建」的表述改为「思辨」，重建保留为功能性描述。"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
NOTES = ROOT / "notes_pheno"

REPL = [
    ("spekulativ 的重建力缺席", "思辨（spekulativ）的重建力缺席"),
    ("spekulativ 的重建力始终缺席", "思辨（spekulativ）的重建力始终缺席"),
    ("spekulativ 的重建在道德与良心里重新出场", "思辨（spekulativ）的重建在道德与良心里重新出场"),
    ("（spekulativ=重建）", "（spekulativ=思辨）"),
    ("重建（Spekulation）尚未开始", "思辨（Spekulation）尚未开始"),
    ("重建（spekulativ）的门槛上", "思辨（spekulativ）的门槛上"),
    ("没有重建（spekulativ）", "没有重建（spekulativ=思辨）"),
    ("又在统一中重建（spekulativ）", "又在统一中重建（spekulativ=思辨）"),
    ("spekulativ 环节（重建）在废墟上建立更高的统一", "思辨（spekulativ）环节在废墟上重建更高的统一"),
]

TEXT_FIELDS = ("bestimmung", "diagnose", "uebergang")


def walk_texts(data, fn):
    for g in data.get("gestalten", []):
        for f in TEXT_FIELDS:
            if g.get(f):
                g[f] = fn(g[f])
        for b in g.get("bewegung", []):
            if len(b) > 3:
                b[3] = fn(b[3])
            if len(b) > 4 and isinstance(b[4], list):
                for s in b[4]:
                    if s.get("content"):
                        s["content"] = fn(s["content"])
            if len(b) > 5 and isinstance(b[5], dict):
                dg = b[5]
                if dg.get("title"):
                    dg["title"] = fn(dg["title"])
                for k in ("left", "right"):
                    nd = dg.get(k) or {}
                    for kk in ("label", "sub"):
                        if nd.get(kk):
                            nd[kk] = fn(nd[kk])
                    if nd.get("points"):
                        nd["points"] = [fn(p) for p in nd["points"]]
                if dg.get("middle"):
                    dg["middle"] = fn(dg["middle"])
                if dg.get("bottom"):
                    dg["bottom"] = fn(dg["bottom"])


def main():
    total = 0
    for n in range(1, 9):
        p = NOTES / f"ch{n}.json"
        if not p.exists():
            continue
        data = json.loads(p.read_text(encoding="utf-8"))
        hits = [0]

        def fn(t):
            for a, b in REPL:
                if a in t:
                    hits[0] += t.count(a)
                    t = t.replace(a, b)
            return t

        walk_texts(data, fn)
        if hits[0]:
            p.write_text(json.dumps(data, ensure_ascii=False, indent=1),
                         encoding="utf-8", newline="\n")
            print(f"ch{n}: 替换 {hits[0]} 处")
            total += hits[0]
    print(f"共替换 {total} 处")


if __name__ == "__main__":
    main()

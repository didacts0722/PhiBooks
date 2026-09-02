# -*- coding: utf-8 -*-
"""
柏拉图 · 巴门尼德篇 注释版构建
复用 build_pheno_ch123 的渲染函数（双栏/术语条/命题链/链路图）。
对话体：无原文章节号，环节切分为编者所加；段 id = c0-pN（单篇）。
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
import build_pheno_ch123 as P  # noqa: E402

EX = ROOT / "原文" / "柏拉图" / "Parmenides" / "extracted"
OUT = ROOT / "笔记" / "柏拉图_巴门尼德篇_注释版.html"


def load_paras():
    data = json.loads((EX / "Parmenides_index.json").read_text(encoding="utf-8"))
    if isinstance(data, list):
        data = data[0] if data else {"items": []}
    paras = []
    for it in data.get("items", []):
        if it["type"] == "p":
            paras.append({"id": f"c0-p{len(paras) + 1}", "page": it.get("page"),
                          "text": it["text"]})
    return paras


def notes_dir():
    # 归位后路径：项目/柏拉图/notes；兼容旧根目录 notes_plato/
    nd = ROOT / "项目" / "柏拉图" / "notes"
    if nd.exists():
        return nd
    return ROOT / "notes_plato"


def main():
    P.load_glossary("")  # 全量术语
    P.RH = {}
    paras = load_paras()
    meta = json.loads((notes_dir() / "parmenides.json").read_text(encoding="utf-8"))
    blocks = P.build_blocks(paras, meta)
    chapter_norm = [(p["id"], p.get("page"), P.norm(p["text"])) for p in paras]
    cited_map = {p["id"]: [] for p in paras}
    for g in meta["gestalten"]:
        for b_ in g["bewegung"]:
            hit = P.resolve_citation(b_[2], chapter_norm)
            if hit:
                cited_map.setdefault(hit[0], []).append(P.norm(b_[2]))

    seen = set()
    for b in blocks:
        P.compute_gterms(b, seen)

    sections = (f'<section class="gestalt" id="ch0">'
                f'<div class="ghead"><h2>{P._html.escape(meta["title"])}</h2>'
                f'<div class="gmeta">做功方式：{P._html.escape(meta["mode"])}</div></div>'
                + "".join(P.render_block(b, 0, chapter_norm, cited_map,
                                         blocks[i - 1] if i > 0 else None,
                                         blocks[i + 1] if i + 1 < len(blocks) else None)
                          for i, b in enumerate(blocks))
                + "</section>")
    sub_parts = []
    cur_group = None
    for b in blocks:
        gp = (b.get("note") or {}).get("group", "") if b.get("kind") == "mov" else ""
        if gp and gp != cur_group:
            sub_parts.append(f'<li class="toc-group">{P._html.escape(gp)}</li>')
            cur_group = gp
        sub_parts.append(
            f'<li><a href="#ch0-s{b["sec"]}">{P.sec_label(b, 0)}'
            f'<span class="toc-r">（{P.para_range(b, 0)}）</span></a></li>')
    sub_parts = "".join(sub_parts)
    toc = (f'<li class="chap"><a href="#ch0">{P._html.escape(meta["title"])}</a>'
           f"<ul>{sub_parts}</ul></li>")
    html = P.TEMPLATE.replace("__TOC__", toc).replace("__SECTIONS__", sections + P.render_glossary())
    html = html.replace("__RANGE__", "柏拉图 · 巴门尼德篇")
    html = html.replace("__BOOK__", "巴门尼德篇 · 注释版")
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(html, encoding="utf-8")

    total = hit = 0
    for g in meta["gestalten"]:
        for b_ in g["bewegung"]:
            total += 1
            q = P.norm(b_[2])
            if any(q.lower() in P.norm(p["text"]).lower() for p in paras):
                hit += 1
    print(f"[产物] {OUT.name}（{OUT.stat().st_size} 字节）")
    print(f"[校验] 引文对拍：{hit}/{total} 命中原文（失败 0 = 全部通过）")
    print(f"[校验] 原文段落：{len(paras)} | 小节：{len(blocks)}")


if __name__ == "__main__":
    main()

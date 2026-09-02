# -*- coding: utf-8 -*-
"""
小逻辑 · 注释版构建：原文(Enzyklopädie_Logik) + 项目/小逻辑/notes/*.json
复用 build_pheno_ch123 的渲染函数（双栏/术语条/阅读辅助/命题链/链路图）。
支持分编构建：
  python build_lp.py sein      → 笔记/小逻辑_存在论_注释版.html（§84-111，CHAPTER=10）
  python build_lp.py essence   → 笔记/小逻辑_本质论_注释版.html（§112-159，CHAPTER=9）
输出文件见 PARTS 表。
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
import build_pheno_ch123 as P  # noqa: E402

NOTES_LP = ROOT / "项目/小逻辑/notes"

# 编定义：名称 → (notes 文件, 输出文件, 章节代号, §范围, 标题前缀)
PARTS = {
    "sein": {
        "notes": "sein.json",
        "out": "小逻辑_存在论_注释版.html",
        "chapter": 10,
        "lo": 84, "hi": 111,
        "range": "小逻辑 · 存在论",
    },
    "essence": {
        "notes": "essence.json",
        "out": "小逻辑_本质论_注释版.html",
        "chapter": 9,
        "lo": 112, "hi": 159,
        "range": "小逻辑 · 本质论",
    },
    "begriff": {
        "notes": "begriff.json",
        "out": "小逻辑_概念论_注释版.html",
        "chapter": 11,
        "lo": 160, "hi": 244,
        "range": "小逻辑 · 概念论",
    },
    "vorbegriff": {
        "notes": "vorbegriff.json",
        "out": "小逻辑_先行概念_注释版.html",
        "chapter": 8,
        "lo": 1, "hi": 83,
        "range": "小逻辑 · 先行概念",
    },
}


def load_pages(lo: int, hi: int, chapter: int) -> list:
    """从 index 重建书序，取 [lo,hi] 的段落（id=c{chapter}-pN, page=页码锚, sec=所属§号）。
    注：§ 附释（Anmerkung）与正文在提取中已融为一体（同一 § 下的多段），sec 标记所属 §，
    不区分正文/附释——显示层打 § 标记用（2026-08-27 用户裁定）。"""
    idx = json.loads((ROOT / "原文" / "黑格尔" / "Enzyklopädie_Logik" / "extracted"
                      / "enzyklopaedie_logik_index.json").read_text(encoding="utf-8-sig"))
    def page_anchor(pg):
        ms = [it.get("page") for it in pg.get("items", []) if it.get("page")]
        return min(ms) if ms else 9999
    pages = sorted(idx, key=page_anchor)
    cur = None
    paras = []
    for pg in pages:
        for it in pg.get("items", []):
            if it["type"] in ("h4", "h5"):
                m = re.match(r"§\s*(\d+)", it["text"])
                cur = int(m.group(1)) if m else cur
            elif it["type"] == "p" and cur and lo <= cur <= hi:
                paras.append({"id": f"c{chapter}-p{len(paras) + 1}",
                              "page": it.get("page"), "sec": cur, "text": it["text"]})
    return paras


def build(part: str):
    cfg = PARTS[part]
    chapter = cfg["chapter"]
    P.load_glossary("")  # 全量术语（小逻辑共享黑格尔主表）
    rhp = NOTES_LP / "reading_help.json"
    P.RH = json.loads(rhp.read_text(encoding="utf-8")).get("paragraphs", {}) if rhp.exists() else {}

    paras = load_pages(cfg["lo"], cfg["hi"], chapter)
    meta = json.loads((NOTES_LP / cfg["notes"]).read_text(encoding="utf-8"))
    blocks = P.build_blocks(paras, meta)
    chapter_norm = [(p["id"], p.get("page"), P.norm(p["text"])) for p in paras]
    cited_map = {p["id"]: [] for p in paras}
    for g in meta["gestalten"]:
        for b_ in g["bewegung"]:
            hit = P.resolve_citation(b_[2], chapter_norm)
            if hit:
                cited_map.setdefault(hit[0], []).append(P.norm(b_[2]))

    # 术语条 + 首次出现（det 引导段落也标注术语表中的词；seen 只在本编内）
    seen = set()
    for b in blocks:
        P.compute_gterms(b, seen)

    sections = (f'<section class="gestalt" id="ch{chapter}">'
                f'<div class="ghead"><h2>{P._html.escape(meta["title"])}</h2>'
                f'<div class="gmeta">做功方式：{P._html.escape(meta["mode"])}</div></div>'
                + "".join(P.render_block(b, chapter, chapter_norm, cited_map,
                                         blocks[i - 1] if i > 0 else None,
                                         blocks[i + 1] if i + 1 < len(blocks) else None)
                          for i, b in enumerate(blocks))
                + "</section>")
    toc = ("<li class=\"chap\"><a href=\"#ch%d\">%s</a><ul>%s</ul></li>"
           % (chapter, P._html.escape(meta["title"]),
              "".join(f'<li><a href="#ch{chapter}-s{b["sec"]}">{P.sec_label(b, chapter)}'
                      f'<span class="toc-r">（{P.para_range(b, chapter)}）</span></a></li>'
                      for b in blocks)))
    html = P.TEMPLATE.replace("__TOC__", toc).replace("__SECTIONS__", sections + P.render_glossary())
    html = html.replace("__RANGE__", cfg["range"])
    html = html.replace("__BOOK__", "小逻辑 · 原文注释版")
    out = ROOT / "笔记" / cfg["out"]
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding="utf-8")

    # 校验
    total = hit = 0
    for g in meta["gestalten"]:
        for b_ in g["bewegung"]:
            total += 1
            q = P.norm(b_[2])
            if any(q.lower() in P.norm(p["text"]).lower() for p in paras):
                hit += 1
    print(f"[产物] {out.name}（{out.stat().st_size} 字节）")
    print(f"[校验] 引文对拍：{hit}/{total} 命中原文（失败 0 = 全部通过）")
    print(f"[校验] 原文段落：{len(paras)} | 小节：{len(blocks)}")


# 合体顺序：按书序（先行概念 → 存在论 → 本质论 → 概念论）
ALL_ORDER = ["vorbegriff", "sein", "essence", "begriff"]


def build_all():
    """四编合并为单文件小逻辑：章节统一编号 1-4，段 id 全局唯一，seen 跨编共享（全书级首次 §）"""
    P.load_glossary("")
    P.RH = {}
    seen_terms = set()  # 全书级首次出现追踪（跨编共享）
    sections = []
    toc_lis = []
    n_paras = n_blocks = total_q = total_hit = 0
    for i, name in enumerate(ALL_ORDER, 1):
        cfg = PARTS[name]
        paras = load_pages(cfg["lo"], cfg["hi"], i)  # 章节代号 = 书序 1-4
        meta = json.loads((NOTES_LP / cfg["notes"]).read_text(encoding="utf-8"))
        blocks = P.build_blocks(paras, meta)
        for b in blocks:
            P.compute_gterms(b, seen_terms)  # 共享 seen：全书级首次 § 标记
        chapter_norm = [(p["id"], p.get("page"), P.norm(p["text"])) for p in paras]
        cited_map = {p["id"]: [] for p in paras}
        for g in meta["gestalten"]:
            for b_ in g["bewegung"]:
                hit = P.resolve_citation(b_[2], chapter_norm)
                if hit:
                    cited_map.setdefault(hit[0], []).append(P.norm(b_[2]))
        sections.append(
            f'<section class="gestalt" id="ch{i}">'
            f'<div class="ghead"><h2>{P._html.escape(meta["title"])}</h2>'
            f'<div class="gmeta">做功方式：{P._html.escape(meta["mode"])}</div></div>'
            + "".join(P.render_block(b, i, chapter_norm, cited_map,
                                     blocks[j - 1] if j > 0 else None,
                                     blocks[j + 1] if j + 1 < len(blocks) else None)
                      for j, b in enumerate(blocks))
            + "</section>")
        toc_lis.append(
            f'<li class="chap"><a href="#ch{i}">{P._html.escape(meta["title"])}</a><ul>'
            + "".join(f'<li><a href="#ch{i}-s{b["sec"]}">{P.sec_label(b, i)}'
                      f'<span class="toc-r">（{P.para_range(b, i)}）</span></a></li>'
                      for b in blocks)
            + "</ul></li>")
        n_paras += len(paras)
        n_blocks += len(blocks)
        for g in meta["gestalten"]:
            for b_ in g["bewegung"]:
                total_q += 1
                if any(P.norm(b_[2]).lower() in P.norm(p["text"]).lower() for p in paras):
                    total_hit += 1
    html = P.TEMPLATE.replace("__TOC__", "\n".join(toc_lis)).replace(
        "__SECTIONS__", "\n".join(sections) + P.render_glossary())
    html = html.replace("__RANGE__", "小逻辑 · 全书（先行概念→存在论→本质论→概念论）")
    html = html.replace("__BOOK__", "小逻辑 · 原文注释版")
    out = ROOT / "笔记" / "小逻辑_注释版.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"[产物] {out.name}（{out.stat().st_size} 字节）")
    print(f"[校验] 引文对拍：{total_hit}/{total_q} 命中原文（失败 0 = 全部通过）")
    print(f"[校验] 原文段落：{n_paras} | 小节：{n_blocks} | 首次术语标记：{len(seen_terms)} 个词")


if __name__ == "__main__":
    part = sys.argv[1] if len(sys.argv) > 1 else "essence"
    if part == "all":
        build_all()
    elif part not in PARTS:
        print(f"未知编：{part}。可选：{' / '.join(PARTS)} / all")
        sys.exit(1)
    else:
        build(part)

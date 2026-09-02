# -*- coding: utf-8 -*-
"""
法哲学原理 · 注释版构建：原文(Grundlinien_der_Philosophie_des_Rechts) + notes_recht/*.json
复用 build_pheno_ch123 的渲染函数（双栏/术语条/阅读辅助/命题链/链路图）。
借鉴小逻辑项目形态：四部分分别写，再合并（build_all）。
支持分编构建：
  python build_recht.py vorrede   → 笔记/法哲学_导言_注释版.html（§1-33）
  python build_recht.py abstrakt  → 笔记/法哲学_抽象法_注释版.html（§34-104）
  python build_recht.py moral     → 笔记/法哲学_道德_注释版.html（§105-141）
  python build_recht.py sittlich  → 笔记/法哲学_伦理_注释版.html（§142-360）
  python build_recht.py all       → 笔记/法哲学原理_注释版.html（全书合体）
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
import build_pheno_ch123 as P  # noqa: E402

NOTES_RECHT = ROOT / "notes_recht"
IDX = ROOT / "原文" / "黑格尔" / "Grundlinien_der_Philosophie_des_Rechts" / "extracted" / "Grundlinien_der_Philosophie_des_Rechts_index.json"
SEC_MAP_FILE = NOTES_RECHT / "staat_sec_map.json"  # §260-329：zeno 内部国家法页无 § 标题，段落按内容标注（逐段）

# 编定义：名称 → (notes 文件, 输出文件, 章节代号, §范围, 标题前缀)
PARTS = {
    "vorrede": {
        "notes": "vorrede_einleitung.json",
        "out": "法哲学_导言_注释版.html",
        "chapter": 1,
        "lo": 1, "hi": 33,
        "range": "法哲学 · 导言（法的概念与自由意志）",
    },
    "abstrakt": {
        "notes": "abstraktes_recht.json",
        "out": "法哲学_抽象法_注释版.html",
        "chapter": 2,
        "lo": 34, "hi": 104,
        "range": "法哲学 · 第一编 抽象法",
    },
    "moral": {
        "notes": "moralitaet.json",
        "out": "法哲学_道德_注释版.html",
        "chapter": 3,
        "lo": 105, "hi": 141,
        "range": "法哲学 · 第二编 道德",
    },
    "sittlich": {
        "notes": "sittlichkeit.json",
        "out": "法哲学_伦理_注释版.html",
        "chapter": 4,
        "lo": 142, "hi": 360,
        "range": "法哲学 · 第三编 伦理",
    },
}

# 合体顺序：按书序（导言 → 抽象法 → 道德 → 伦理）
ALL_ORDER = ["vorrede", "abstrakt", "moral", "sittlich"]


def load_pages(lo: int, hi: int, chapter: int) -> list:
    """从 index 重建书序，取 [lo,hi] 的段落（id=c{chapter}-pN, page=页码锚, sec=所属§号/Vor）。
    注：Vorrede 段落无 § 归属（在 §1 之前），须排在书序最前（Vor 段先收，§ 段后收）。
    index 页面按字母序排列，§ 段须按 § 号稳定排序恢复书序（同 § 内保持原文相对顺序，2026-08-29 修复）。
    § 附释（Anmerkung）与正文在提取中已融为一体，sec 标记所属 §，不区分（2026-08-27 用户裁定）。"""
    idx = json.loads(IDX.read_text(encoding="utf-8-sig"))
    sec_map = json.loads(SEC_MAP_FILE.read_text(encoding="utf-8")) if SEC_MAP_FILE.exists() else {}
    vor_paras = []
    raw_sec = []
    # 第一遍：Vorrede（Vor 段，仅导言 lo=1 时）
    if lo == 1:
        for pg in idx:
            if pg.get("file") != "Vorrede.html":
                continue
            for it in pg.get("items", []):
                if it["type"] == "p":
                    vor_paras.append({"page": it.get("page"), "sec": "Vor", "text": it["text"]})
    # 第二遍：收集 § 段（页面为字母序，按 § 号稳定排序恢复书序）。
    # 无 § 标题的页面（内部国家法 7 页，zeno 长文连续版式）用 staat_sec_map.json 逐段标注。
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
                    raw_sec.append({"page": it.get("page"), "sec": sec_use, "text": it["text"]})
    raw_sec.sort(key=lambda p: p["sec"])  # 稳定排序：恢复书序，同 § 内保持原顺序
    # 编号：Vor 段在前（c{chapter}-p1..），§ 段接续（书序编号）
    for i, p in enumerate(vor_paras, 1):
        p["id"] = f"c{chapter}-p{i}"
    base = len(vor_paras)
    sec_paras = []
    for i, p in enumerate(raw_sec, 1):
        p["id"] = f"c{chapter}-p{base + i}"
        sec_paras.append(p)
    return vor_paras + sec_paras


def load_notes(name: str) -> dict:
    return json.loads((NOTES_RECHT / name).read_text(encoding="utf-8"))


def build(part: str):
    cfg = PARTS[part]
    chapter = cfg["chapter"]
    P.load_glossary("")  # 全量术语（法哲学共享黑格尔主表）
    P.RH = {}

    paras = load_pages(cfg["lo"], cfg["hi"], chapter)
    meta = load_notes(cfg["notes"])
    blocks = P.build_blocks(paras, meta)
    seen_terms = set()
    for b in blocks:
        P.compute_gterms(b, seen_terms)
    chapter_norm = [(p["id"], p.get("page"), P.norm(p["text"])) for p in paras]
    cited_map = {p["id"]: [] for p in paras}
    for g in meta["gestalten"]:
        for b_ in g["bewegung"]:
            hit = P.resolve_citation(b_[2], chapter_norm)
            if hit:
                cited_map.setdefault(hit[0], []).append(P.norm(b_[2]))
    sections = (
        f'<section class="gestalt" id="ch{chapter}">'
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
    html = html.replace("__BOOK__", "法哲学原理 · 注释版")
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


def build_all():
    """四部分合并为单文件法哲学（方法 A：只输出 笔记/法哲学原理_注释版.html 一个文件）：
    章节统一编号 1-4，段 id 全局唯一，seen 跨编共享。
    只处理「已填充」的部分（bewegung 非空）——骨架未写的部分自动跳过，随进度追加。"""
    P.load_glossary("")
    P.RH = {}
    seen_terms = set()
    sections = []
    toc_lis = []
    n_paras = n_blocks = total_q = total_hit = 0
    chapter_no = 0  # 实际章节号（跳过空骨架后连续编号）
    for name in ALL_ORDER:
        cfg = PARTS[name]
        meta = load_notes(cfg["notes"])
        # 跳过未填充的骨架（bewegung 为空）
        if not any(g.get("bewegung") for g in meta.get("gestalten", [])):
            continue
        chapter_no += 1
        i = chapter_no
        paras = load_pages(cfg["lo"], cfg["hi"], i)
        blocks = P.build_blocks(paras, meta)
        for b in blocks:
            P.compute_gterms(b, seen_terms)
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
        sub_parts = []
        cur_group = None
        for b in blocks:
            gp = (b.get("note") or {}).get("group", "") if b.get("kind") == "mov" else ""
            if gp and gp != cur_group:
                sub_parts.append(f'<li class="toc-group">{P._html.escape(gp)}</li>')
                cur_group = gp
            sub_parts.append(
                f'<li><a href="#ch{i}-s{b["sec"]}">{P.sec_label(b, i)}'
                f'<span class="toc-r">（{P.para_range(b, i)}）</span></a></li>')
        toc_lis.append(
            f'<li class="chap"><a href="#ch{i}">{P._html.escape(meta["title"])}</a><ul>'
            + "".join(sub_parts)
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
    html = html.replace("__RANGE__", "导言→抽象法→道德→伦理，随进度追加")
    html = html.replace("__BOOK__", "法哲学原理 · 注释版")
    out = ROOT / "笔记" / "法哲学原理_注释版.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"[产物] {out.name}（{out.stat().st_size} 字节）")
    print(f"[校验] 引文对拍：{total_hit}/{total_q} 命中原文（失败 0 = 全部通过）")
    print(f"[校验] 原文段落：{n_paras} | 小节：{n_blocks} | 首次术语标记：{len(seen_terms)} 个词")


if __name__ == "__main__":
    part = sys.argv[1] if len(sys.argv) > 1 else "all"
    if part == "all":
        build_all()
    elif part not in PARTS:
        print(f"未知部分：{part}。可选：{' / '.join(PARTS)} / all（方法 A：全部输出到单个 法哲学原理_注释版.html）")
        sys.exit(1)
    else:
        build_all()  # 方法 A：分编参数也统一走单文件合体

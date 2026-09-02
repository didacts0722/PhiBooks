# -*- coding: utf-8 -*-
"""
note_tool.py —— 跨作品通用笔记工具（现象学/小逻辑/法哲学/柏拉图/未来项目）

用途：对 `项目/<作品>/notes/*.json`（同构数据模型）做持续笔记工作链：
      verify（对拍审计+颗粒度报告）→ reorder（书序重排）→ fix-quote（引文修正）
      → append（讨论补充）→ dump（未引段/环节清单）→ gloss（术语对照）。

数据模型（四书同构，已验证 2026-08-29）：
  顶层 {title, pages, mode, gestalten}
  gestalten[] {name, position, bestimmung, bewegung, diagnose, uebergang, [chain, supps]}
  bewegung[] 每元素为 list，前 4 字段语义一致：
      [0] 环节标题   [1] 原文锚（现象学 p.140 / 小逻辑 181 / 法哲学 §158 / 柏拉图 126）
      [2] 德文引文（原始，对拍对象）  [3] 笔记正文
      后续字段因作品而异（supps/diagram/group…）→ 工具只动 [0]-[3]，扩展字段透传。

用法：
  python note_tool.py --work 法哲学 verify
  python note_tool.py --work 法哲学 reorder --dry-run
  python note_tool.py --work 法哲学 fix-quote §166 "新的逐字引文"
  python note_tool.py --work 现象学 dump --uncited ch4
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent

# 共享对拍核心（norm/resolve_citation 等）
import build_pheno_ch123 as P  # noqa: E402


# ---------------------------------------------------------------- 作品配置
def _glob_first(pattern):
    hits = sorted(ROOT.glob(pattern))
    return hits[0] if hits else None


WORKS = {
    "现象学": {
        "notes_glob": "项目/现象学/notes/ch*.json",
        "extra_files": ["项目/现象学/notes/reading_help.json"],  # 段落引读（现象学独有）
        "index": "原文/黑格尔/Phänomenologie_des_Geistes/extracted/phenomenologie_index.json",
        "chapter_files": {
            0: "项目/现象学/notes/ch0.json", 1: "项目/现象学/notes/ch1.json",
            2: "项目/现象学/notes/ch2.json", 3: "项目/现象学/notes/ch3.json",
            4: "项目/现象学/notes/ch4.json", 5: "项目/现象学/notes/ch5.json",
            6: "项目/现象学/notes/ch6.json", 7: "项目/现象学/notes/ch7.json",
            8: "项目/现象学/notes/ch8.json",
        },
        "anchors": r"(?:p\.)?(\d+)",   # 页码锚：p.140 或裸数字（ch0 Vorrede 无 p. 前缀）
        "sort_key": "page",            # 按页码排序
        "secmap": None,
    },
    "小逻辑": {
        "notes_glob": "项目/小逻辑/notes/*.json",
        "index": "原文/黑格尔/Enzyklopädie_Logik/extracted/enzyklopaedie_logik_index.json",
        "anchors": r"(\d+)",           # 裸 § 号（无前缀）
        "sort_key": "sec",
        "secmap": None,
    },
    "法哲学": {
        "notes_glob": "项目/法哲学/notes/*.json",
        "index": "原文/黑格尔/Grundlinien_der_Philosophie_des_Rechts/extracted/Grundlinien_der_Philosophie_des_Rechts_index.json",
        "anchors": r"§\s*(\d+)",       # § 前缀
        "sort_key": "sec",
        "secmap": "项目/法哲学/notes/staat_sec_map.json",  # §260-329 段落归属映射
        "skip_files": ["staat_sec_map.json"],
    },
    "柏拉图": {
        "notes_glob": "项目/柏拉图/notes/*.json",
        "index": "原文/柏拉图/Parmenides/extracted/Parmenides_index.json",
        "anchors": r"(\d+)",           # Stephanus 页码
        "sort_key": "sec",
        "secmap": None,
    },
}


def load_work(name):
    if name not in WORKS:
        sys.exit(f"未知作品：{name}（可选：{'/'.join(WORKS)}）")
    return WORKS[name]


def work_notes_files(cfg):
    """返回该作品的笔记 json 文件（排除辅助文件）。"""
    skip = set(cfg.get("skip_files", []))
    files = []
    for p in sorted(ROOT.glob(cfg["notes_glob"])):
        if p.name not in skip:
            files.append(p)
    return files


def work_extra_files(cfg):
    return [ROOT / f for f in cfg.get("extra_files", [])]


def load_all_gestalten(files):
    """读取全部笔记文件的 gestalten → [(file, gestalt_index, gestalt)]。"""
    result = []
    for f in files:
        d = json.loads(f.read_text(encoding="utf-8"))
        for gi, g in enumerate(d.get("gestalten", [])):
            result.append((f, gi, g))
    return result


# ---------------------------------------------------------------- 锚解析与排序
def anchor_num(cfg, anchor):
    m = re.search(cfg["anchors"], anchor or "")
    return int(m.group(1)) if m else None


def reorder_bewegung(bw, cfg):
    """按锚（§/页码）稳定排序 bewegung；锚解析失败的元素放原位。"""
    def key(b):
        n = anchor_num(cfg, b[1])
        return (n is None, n if n is not None else 0)
    return sorted(bw, key=key)


# ---------------------------------------------------------------- 对拍
def load_index_paras(cfg):
    """读取作品原文 index 的全部段落（带页码/§ 上下文）。

    注意：zeno 提取的 index 页面为字母序（文件名排序所致），须按页码重建书序
    （与 build_lp.load_pages/build_recht 同一逻辑）；§ 上下文由页内 h4/h5 标题继承。
    """
    idx_path = ROOT / cfg["index"]
    if not idx_path.exists():
        return []
    try:
        idx = json.loads(idx_path.read_text(encoding="utf-8-sig"))
    except Exception:
        idx = json.loads(idx_path.read_text(encoding="utf-8"))
    if not isinstance(idx, list):
        return []

    def page_anchor(pg):
        ms = [it.get("page") for it in pg.get("items", []) if it.get("page")]
        return min(ms) if ms else 999999

    # 法哲学 §260-329 走 sec_map（页内无 § 标题）；其余靠 § 上下文
    secmap = None
    if cfg.get("secmap"):
        sm_path = ROOT / cfg["secmap"]
        if sm_path.exists():
            secmap = json.loads(sm_path.read_text(encoding="utf-8"))

    pages = sorted(idx, key=page_anchor)
    paras = []
    for pg in pages:
        cur_sec = None
        mapped = secmap.get(pg.get("file")) if secmap else None
        mi = 0
        for it in pg.get("items", []):
            typ = it.get("type")
            if typ in ("h4", "h5", "h3"):
                m = re.match(r"§\s*(\d+)", it.get("text", ""))
                if m:
                    cur_sec = int(m.group(1))
            elif typ == "p":
                sec_use = cur_sec
                if mapped:
                    sec_use = mapped[mi] if mi < len(mapped) else cur_sec
                    mi += 1
                paras.append({"sec": sec_use, "page": it.get("page"),
                              "text": it.get("text", "")})
    return paras


def verify_quotes(bw, index_paras, cfg):
    """每环节引文对拍：norm+lower 后是否命中原文任一连续子串。

    与 build_pheno_ch123.resolve_citation 同款逻辑（q.lower() in p.lower()），
    避免句首大小写差异误报（如原文句中 "das Ganze" vs 引文句首 "Das Ganze"）。
    """
    norm_paras = [P.norm(p["text"]).lower() for p in index_paras]
    report = []
    for b in bw:
        quote = b[2] if len(b) > 2 else ""
        qn = P.norm(quote).lower()
        hit = bool(qn and len(qn) > 8 and any(qn in np for np in norm_paras))
        report.append({
            "title": b[0], "anchor": b[1],
            "quote_len": len(qn),
            "hit": hit,
            "note_len": len(b[3]) if len(b) > 3 else 0,
            "width": len(b),
        })
    return report


# ---------------------------------------------------------------- 子命令
def cmd_verify(args, cfg):
    files = work_notes_files(cfg)
    index_paras = load_index_paras(cfg)
    print(f"=== verify · {args.work}（{len(files)} 个笔记文件）===")
    if index_paras:
        print(f"原文段落：{len(index_paras)}（索引 {cfg['index']}）")
    else:
        print("⚠️  原文索引未找到，对拍检查跳过")
    total, hit_n, miss = 0, 0, []
    for f in files:
        d = json.loads(f.read_text(encoding="utf-8"))
        for gi, g in enumerate(d.get("gestalten", [])):
            bw = g.get("bewegung", [])
            if not bw:
                continue
            rep = verify_quotes(bw, index_paras, cfg)
            # 打印环节薄弱的（引文未命中/正文过短；无锚但引文命中不算缺陷）
            for r in rep:
                total += 1
                flags = []
                if index_paras and not r["hit"]:
                    flags.append("引文未命中")
                    miss.append((f.name, r["anchor"], r["title"]))
                if r["note_len"] < 60:
                    flags.append("正文单薄")
                if (not r["anchor"] or anchor_num(cfg, r["anchor"]) is None) and (not r["hit"] or not index_paras):
                    flags.append("无有效锚且无对拍")
                if flags:
                    print(f"  ⚠️ {f.name} [{r['anchor'] or '?'}] {r['title'][:28]} — {'/'.join(flags)}")
                hit_n += 1 if r["hit"] else 0
    print(f"\n环节总数：{total} | 引文对拍命中：{hit_n}/{total}"
          + (f"（{(index_paras and round(100*hit_n/total) or 0)}%）" if total else ""))
    if miss:
        print(f"未命中 {len(miss)} 处（示例）：")
        for m in miss[:8]:
            print(f"  {m[0]} [{m[1]}] {m[2][:40]}")
    # 段落引读（现象学独有）
    for ef in work_extra_files(cfg):
        if ef.exists():
            rh = json.loads(ef.read_text(encoding="utf-8-sig"))
            n = len(rh.get("paragraphs", {}))
            print(f"段落引读：{ef.name} 覆盖 {n} 段")
    return 0 if not miss else 1


def cmd_reorder(args, cfg):
    """reorder：检查并（显式 --apply 时）按锚重排 bewegung。

    安全设计：默认只报告逆序对（含环节标题），不写盘——因为有些环节是有意的
    「总纲/导言」（锚在区间内但语义在前，如法哲学抽象法 §40 结构宣言前置），
    无条件重排会破坏结构。--apply 才写，且写前打印将移动的环节供人判断。
    """
    files = work_notes_files(cfg)
    for f in files:
        d = json.loads(f.read_text(encoding="utf-8"))
        for g in d.get("gestalten", []):
            bw = g.get("bewegung")
            if not bw:
                continue
            order = [anchor_num(cfg, b[1]) for b in bw]
            pairs = []
            for i in range(len(order) - 1):
                a, c = order[i], order[i + 1]
                if a and c and c < a:
                    pairs.append((i, bw[i], bw[i + 1]))
            if args.apply and pairs:
                new = reorder_bewegung(bw, cfg)
                g["bewegung"] = new
                f.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
                json.loads(f.read_text(encoding="utf-8"))
                print(f"{f.name}: 已重排（{len(pairs)} 处逆序）并校验 JSON")
            elif pairs:
                print(f"{f.name}: 逆序 {len(pairs)} 处（--apply 才写盘）：")
                for i, b1, b2 in pairs:
                    print(f"    [{b1[1]}] {b1[0][:30]} → [{b2[1]}] {b2[0][:30]}")
                print("    ⚠️  若含「总纲/结构宣言」类前置环节，这是有意设计，勿重排")
            else:
                print(f"{f.name}: 顺序正常")
    return 0


def cmd_fix_quote(args, cfg):
    """fix-quote --anchor §166 --quote '逐字引文' [--file sittlichkeit.json]"""
    files = work_notes_files(cfg)
    if args.file:
        files = [f for f in files if f.name == args.file]
        if not files:
            sys.exit(f"未找到文件 {args.file}")
    for f in files:
        d = json.loads(f.read_text(encoding="utf-8"))
        for g in d.get("gestalten", []):
            for b in g.get("bewegung", []):
                if b[1] == args.anchor and len(b) > 2:
                    old = b[2]
                    if old == args.quote:
                        print(f"{f.name} [{args.anchor}]：引文已是目标，跳过")
                        return 0
                    b[2] = args.quote
                    f.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
                    json.loads(f.read_text(encoding="utf-8"))  # 写后校验
                    print(f"已修正 {f.name} [{args.anchor}]：引文更新（{len(old)} 字 → {len(args.quote)} 字）")
                    return 0
    sys.exit(f"未找到锚 {args.anchor}")
    return 1


def cmd_dump(args, cfg):
    """dump：列出环节清单或未引段（供阅读辅助产线/颗粒度观察）。"""
    files = work_notes_files(cfg)
    if args.file:
        files = [f for f in files if f.name == args.file]
    for f in files:
        d = json.loads(f.read_text(encoding="utf-8"))
        print(f"\n=== {f.name} ===")
        for gi, g in enumerate(d.get("gestalten", [])):
            print(f"  gestalt[{gi}] {g.get('name','')}：bewegung {len(g.get('bewegung', []))} 环节")
            if args.verbose:
                for b in g.get("bewegung", []):
                    print(f"    [{b[1] or '?'}] {b[0][:50]}｜正文 {len(b[3]) if len(b)>3 else 0} 字")
    return 0


def cmd_append(args, cfg):
    """append --anchor p.140 --title '🔑 ...' --content '...'：在指定环节 [3] 正文尾部追加讨论补充。"""
    files = work_notes_files(cfg)
    if args.file:
        files = [f for f in files if f.name == args.file]
    done = False
    for f in files:
        d = json.loads(f.read_text(encoding="utf-8"))
        for g in d.get("gestalten", []):
            for b in g.get("bewegung", []):
                if b[1] == args.anchor:
                    if args.supp_title and args.supp_content:
                        # 扩展位：supps 列表（现象学/部分作品格式）
                        supps = b[4] if len(b) > 4 and isinstance(b[4], list) else None
                        entry = {"date": args.date or "2026-08-29",
                                 "title": args.supp_title, "content": args.supp_content}
                        if supps is None:
                            b.append([entry]) if len(b) == 4 else None
                        else:
                            supps.append(entry)
                    else:
                        b[3] = (b[3] + "\n\n" + args.content).strip()
                    f.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
                    json.loads(f.read_text(encoding="utf-8"))
                    print(f"已追加到 {f.name} [{args.anchor}]")
                    done = True
    if not done:
        sys.exit(f"未找到锚 {args.anchor}")
    return 0


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description="跨作品通用笔记工具")
    ap.add_argument("--work", required=True, choices=list(WORKS.keys()))
    sub = ap.add_subparsers(dest="cmd", required=True)

    pv = sub.add_parser("verify", help="对拍审计 + 颗粒度报告")
    pv.set_defaults(fn=cmd_verify)

    pr = sub.add_parser("reorder", help="检查/重排 bewegung 书序（默认只报告，--apply 才写）")
    pr.add_argument("--apply", action="store_true", help="确认后写盘（注意总纲前置环节勿重排）")
    pr.set_defaults(fn=cmd_reorder)

    pf = sub.add_parser("fix-quote", help="修正环节引文为逐字原文")
    pf.add_argument("--anchor", required=True, help="环节锚（§158/p.140/181/126）")
    pf.add_argument("--quote", required=True, help="新的逐字引文")
    pf.add_argument("--file", default="", help="限定笔记文件（可选）")
    pf.set_defaults(fn=cmd_fix_quote)

    pd = sub.add_parser("dump", help="环节清单/结构观察")
    pd.add_argument("--file", default="", help="限定笔记文件")
    pd.add_argument("--verbose", action="store_true", help="展开每环节")
    pd.set_defaults(fn=cmd_dump)

    pa = sub.add_parser("append", help="向环节正文/补充追加内容")
    pa.add_argument("--anchor", required=True)
    pa.add_argument("--content", default="", help="追加到正文 [3]")
    pa.add_argument("--supp-title", default="", help="追加为 supps 条目（需同时给 --supp-content）")
    pa.add_argument("--supp-content", default="")
    pa.add_argument("--date", default="", help="supps 日期（默认今天）")
    pa.add_argument("--file", default="")
    pa.set_defaults(fn=cmd_append)

    args = ap.parse_args()
    cfg = load_work(args.work)
    sys.exit(args.fn(args, cfg) or 0)


if __name__ == "__main__":
    main()

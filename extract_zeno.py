# -*- coding: utf-8 -*-
"""
zeno 原文页 → 结构化文本（JSON + 可读 txt）。
- 解码：iso-8859-1（页面声明）
- 截取正文区：起始=首个 h4/h5/正文段落；结束=页脚标记（zenoPLBookTextMore / zenoTRNavBottom）
- 提取：h4/h5 标题、zenoPLm4n0 段落；段落内捕获原书页码锚点 <a name="NN">[NN]</a>；
  <i> → *...*，<b> → **...**，其余标签剥除，HTML 实体解码
- 排除脚注变体页（_fnN / _fnNref）
输出：原文/<book>/extracted/ 下每页 .json + 合并 index.json + 全部文本 .txt
"""
import html as _html
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "原文"

PHENO = RAW / "黑格尔" / "Phänomenologie_des_Geistes"
ENZ = RAW / "黑格尔" / "Enzyklopädie_Logik"

PARA_CLASSES = ("zenoPLm4n0",)
ITEM_RE = re.compile(
    r'<h4[^>]*>(.*?)</h4>|<h5[^>]*>(.*?)</h5>|'
    r'<p([^>]*)>(.*?)</p>',
    re.S,
)
PAGE_ANCHOR_RE = re.compile(r'<a\b[^>]*\bname="(\d+)"[^>]*>\s*\[(\d+)\]\s*</a>')

# 正文段落 class：无 class（部分页用普通 <p>）或 zenoPLm<n>n<m>（正文行，缩进变体，
# 如 zenoPLm4n0 标准正文 / zenoPLm0n4 对话缩进等；2026-08 普查确认全部只出现在
# zenoCOMain 正文区）；其余 class（empf 推荐 / zenoPC 结尾标记 / zenoPR 签名题词 /
# zenoTX 导航等）一律排除
CONTENT_P_CLASS = {"zenoPLm4n0"}
CONTENT_P_RE = re.compile(r"^zenoPLm\d+n\d+$")


def is_content_p(attrs: str) -> bool:
    m = re.search(r'class="([^"]*)"', attrs)
    if not m:
        return True
    cls = m.group(1)
    return cls in CONTENT_P_CLASS or bool(CONTENT_P_RE.match(cls))


def decode(data: bytes) -> str:
    return data.decode("iso-8859-1", errors="replace")


def find_end(txt: str) -> int:
    marks = [txt.find("zenoPLBookTextMore"), txt.find("zenoTRNavBottom")]
    marks = [i for i in marks if i > 0]
    return min(marks) if marks else len(txt)


def clean_inline(s: str) -> str:
    s = PAGE_ANCHOR_RE.sub("", s)  # 页码锚点已单独捕获
    s = re.sub(r"<i[^>]*>(.*?)</i>", r"*\1*", s, flags=re.S)
    s = re.sub(r"<b[^>]*>(.*?)</b>", r"**\1**", s, flags=re.S)
    s = re.sub(r"<[^>]+>", "", s)
    s = _html.unescape(s)
    s = re.sub(r"[ \t]+", " ", s)
    return s.strip()


def clean_title(s: str) -> str:
    s = re.sub(r"<[^>]+>", "", s)
    s = _html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def extract_page(path: Path) -> dict:
    txt = decode(path.read_bytes())
    end = find_end(txt)
    body = txt[:end]
    items = []
    for m in ITEM_RE.finditer(body):
        if m.group(1) is not None:
            items.append({"type": "h4", "text": clean_title(m.group(1)), "page": None})
        elif m.group(2) is not None:
            items.append({"type": "h5", "text": clean_title(m.group(2)), "page": None})
        else:
            attrs, para = m.group(3), m.group(4)
            if not is_content_p(attrs):
                continue
            pm = PAGE_ANCHOR_RE.search(para)
            page = int(pm.group(2)) if pm else None
            text = clean_inline(para)
            if text:
                items.append({"type": "p", "text": text, "page": page})
    return {"file": path.name, "items": items}


def process_book(book_dir: Path, out_name: str):
    pages = []
    for f in sorted(book_dir.glob("*.html")):
        if re.search(r"_fn\d+(ref)?\.html$", f.name):
            continue
        pages.append(extract_page(f))
    # 总文本
    all_lines = []
    for pg in pages:
        all_lines.append(f"===== {pg['file']} =====")
        for it in pg["items"]:
            prefix = {"h4": "# ", "h5": "## ", "p": ""}[it["type"]]
            page_mark = f"〔p.{it['page']}〕" if it.get("page") else ""
            all_lines.append(f"{prefix}{page_mark}{it['text']}")
        all_lines.append("")
    out_dir = book_dir / "extracted"
    out_dir.mkdir(exist_ok=True)
    (out_dir / f"{out_name}_all.txt").write_text("\n".join(all_lines), encoding="utf-8")
    # 每页 json + 合并
    for pg in pages:
        (out_dir / (pg["file"].replace(".html", ".json"))).write_text(
            json.dumps(pg, ensure_ascii=False, indent=1), encoding="utf-8")
    (out_dir / f"{out_name}_index.json").write_text(
        json.dumps(pages, ensure_ascii=False), encoding="utf-8")
    n_items = sum(len(p["items"]) for p in pages)
    n_paras = sum(1 for p in pages for it in p["items"] if it["type"] == "p")
    n_h = sum(1 for p in pages for it in p["items"] if it["type"] in ("h4", "h5"))
    print(f"[{out_name}] 页数={len(pages)} 条目={n_items}（段落 {n_paras} / 标题 {n_h}）"
          f" -> {out_dir}")


def main():
    """用法：python extract_zeno.py [作品目录...]；无参数则处理黑格尔已有两书"""
    args = sys.argv[1:]
    if args:
        for d in args:
            p = Path(d)
            if p.is_dir():
                process_book(p, p.name)
        print("完成。")
        return
    process_book(PHENO, "phenomenologie")
    process_book(ENZ, "enzyklopaedie_logik")
    print("完成。")


if __name__ == "__main__":
    main()

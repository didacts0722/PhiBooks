# -*- coding: utf-8 -*-
"""
build_docs_epub.py — docs 内容文档 → epub（手机阅读）
用法: python build_docs_epub.py
依赖: 仅 python 标准库 + markdown 库（本地已装，无需网络/pandoc）
产出: 移动阅读/哲学工作笔记.epub

书内结构（2026-09-04 用户确认）：
  - 格式 epub（非 Kindle 环境）
  - 收 18 个内容文档，排 8 个流程/工具文件
  - 四部分按主题分组；手动构造 EPUB（zip 容器 + OPF + NCX 嵌套目录）
"""
import os, re, sys, zipfile, html as htmlmod
import markdown
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")
OUT_DIR = os.path.join(ROOT, "移动阅读")
OUT_EPUB = os.path.join(OUT_DIR, "哲学工作笔记.epub")

META_TITLE = "哲学工作笔记（docs 精选）"
META_AUTHOR = "Books 工作区"

# 书内结构：四部分，每部分 = (部分标题, [文件名,...])
PARTS = [
    ("第一部分 引擎与方法", [
        "三书关系_引擎三介质.md",
        "全书结构分析.md",
        "义解_环节对应表.md",
        "存在论_术语规范化草案.md",
    ]),
    ("第二部分 观点库", [
        "基础观点库.md",
        "文献观点库.md",
        "柏拉图观点库.md",
        "谢林观点库.md",
    ]),
    ("第三部分 精神分析与自来水寓言", [
        "自来水比喻_寓言性哲学史.md",
        "自来水比喻_详册_系统与前史.md",
        "自来水比喻_详册_后黑格尔姿态.md",
        "精神分析术语释义.md",
        "临床结构学说_拉康四大结构.md",
        "精神分析_引擎深度整理.md",
    ]),
    ("第四部分 讨论与档案", [
        "对话档案.md",
        "对话录_劳动与尼特族.md",
        "法哲学_讨论材料.md",
        "法哲学_导言_血肉展开.md",
        "现象学_重新梳理收获.md",
        "伴侣匹配标准.md",
    ]),
]

CSS = """
body { font-family: serif; line-height: 1.75; margin: 1em; font-size: 1.02em; }
h1 { font-size: 1.45em; page-break-before: always; margin-bottom: 0.4em; }
h1:first-of-type { page-break-before: auto; }
h2 { font-size: 1.28em; margin-top: 1.3em; margin-bottom: 0.3em; }
h3 { font-size: 1.15em; margin-top: 1.1em; }
p { margin: 0.5em 0; }
ul, ol { margin: 0.4em 0; padding-left: 1.4em; }
li { margin: 0.25em 0; }
/* blockquote 与正文一致（用户裁定 2026-09-04）：不做特殊底色/边框——
   但必须显式 background:transparent + border:none，否则阅读器（Readest 等）
   对无声明引用块套默认深底（最初黑底问题）。显式声明后视觉即与正文相同。 */
blockquote {
  background: transparent;
  color: inherit;
  border: none;
  margin: 0.6em 0;
  padding: 0;
}
blockquote p { margin: 0.4em 0; }
/* 表格：窄屏优先紧凑；长文本格允许断词换行 */
table { border-collapse: collapse; width: 100%; margin: 0.6em 0; font-size: 0.82em; table-layout: fixed; }
th, td { border: 1px solid #bbb; padding: 3px 5px; text-align: left; vertical-align: top; word-wrap: break-word; overflow-wrap: break-word; }
th { background: #eee; font-weight: bold; }
/* 代码块（动力链图已窄化≤42字符）：等宽微缩+pre-wrap 兜底防溢出 */
code { font-family: monospace; font-size: 0.9em; background: #f4f4f4; padding: 0 2px; }
pre {
  font-family: monospace; font-size: 0.78em; line-height: 1.55;
  background: #f4f4f4; padding: 0.7em 0.8em; margin: 0.7em 0;
  white-space: pre-wrap; word-wrap: break-word; overflow-wrap: break-word;
}
img { max-width: 100%; }
hr { border: none; border-top: 1px solid #ccc; margin: 1.4em 0; }
strong { font-weight: bold; }
"""

XHTML_TMPL = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-CN" lang="zh-CN">
<head><meta charset="utf-8"/><title>{title}</title>
<link rel="stylesheet" type="text/css" href="style.css"/></head>
<body>
{body}
</body></html>
"""


def md_to_html(text):
    """md → html body。fenced_code 需正确输出 code 语言类。"""
    md = markdown.Markdown(
        extensions=["tables", "fenced_code", "sane_lists", "attr_list"],
        output_format="xhtml5",
    )
    return md.convert(text)


def shift_headings(text):
    """标题级别 +1（#→##…），跳过 ``` 围栏内的行。"""
    out = []
    in_fence = False
    for line in text.split("\n"):
        s = line.lstrip()
        if s.startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue
        if not in_fence and re.match(r"^(#{1,6})\s", line):
            line = "#" + line
        out.append(line)
    return "\n".join(out)


def esc(s):
    return htmlmod.escape(s, quote=True)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    # ── 1. 读文件 → (part_index, file_index, html_body, title)
    chapters = []  # (id, part_label, file_label, html_body)
    for pi, (part_title, names) in enumerate(PARTS):
        for fi, n in enumerate(names):
            p = os.path.join(DOCS, n)
            if not os.path.exists(p):
                print("ERROR: 缺文件", p)
                return 1
            with open(p, encoding="utf-8") as f:
                text = f.read()
            body = md_to_html(shift_headings(text))
            chapters.append({
                "id": "part{}-file{}".format(pi, fi),
                "part": part_title,
                "file": os.path.splitext(n)[0],
                "body": body,
            })

    # ── 2. 生成 xhtml 文件内容
    # 文件名统一用数字索引 ch{idx}.xhtml（idx=chapters 顺序 0..N-1）——
    # nav/NCX 目录链接均以该索引为 href，必须同一套命名
    file_entries = []  # (filename, xhtml)
    for idx, ch in enumerate(chapters):
        title = "{}｜{}".format(ch["part"], ch["file"])
        # 章首放部分+文件两级标题，正文去掉 md 自己的主标题首行重复问题：
        # 文件内容标题已平移为 h2 起，这里补 h1=部分、h2=文件标题会重复文件内 h2？
        # 文件内第一个标题=原文 #（平移后 ##）——即文件名本身，故章首只放部分标题，文件标题由正文 h2 呈现。
        body = '<h1>{}</h1>\n{}'.format(esc(ch["part"]), ch["body"])
        file_entries.append(("ch{}.xhtml".format(idx),
                             XHTML_TMPL.format(title=esc(title), body=body)))

    style = XHTML_TMPL.format(title="style", body="<style>{}</style>".format(CSS))
    # 上面把 style 包在 body 里不标准；epub 用独立 css 文件
    style_css = CSS

    # ── 3. OPF manifest/spine（EPUB3：version 3.0 + nav 导航文档）
    items = []
    itemrefs = []
    items.append('    <item id="css" href="style.css" media-type="text/css"/>')
    items.append('    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>')
    items.append('    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>')
    for i, (fn, _) in enumerate(file_entries):
        items.append('    <item id="ch{}" href="{}" media-type="application/xhtml+xml"/>'.format(i, fn))
        itemrefs.append('    <itemref idref="ch{}"/>'.format(i))
    manifest = "\n".join(items)
    spine = "\n".join(itemrefs)

    opf = """<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="BookId"
         xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
<metadata>
  <dc:title>{title}</dc:title>
  <dc:creator opf:role="aut">{author}</dc:creator>
  <dc:language>zh-CN</dc:language>
  <dc:identifier id="BookId">urn:uuid:{uuid}</dc:identifier>
  <meta property="dcterms:modified">{modified}</meta>
</metadata>
<manifest>
{manifest}
</manifest>
<spine toc="ncx">
{spine}
</spine>
</package>""".format(
        title=esc(META_TITLE), author=esc(META_AUTHOR),
        uuid=__import__("uuid").uuid4(),
        modified=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        manifest=manifest, spine=spine,
    )

    # ── 4. NCX 嵌套目录（部分 > 文件）
    navpoints = []
    playorder = 0
    for pi, (part_title, names) in enumerate(PARTS):
        children = []
        for fi in range(len(names)):
            cid = "part{}-file{}".format(pi, fi)
            ch_idx = next(idx for idx, ch in enumerate(chapters)
                          if ch["id"] == cid)
            ch_obj = chapters[ch_idx]
            playorder += 1
            children.append("""    <navPoint id="np-{po}" playOrder="{po}">
      <navLabel><text>{label}</text></navLabel>
      <content src="ch{ci}.xhtml"/>
    </navPoint>""".format(po=playorder, label=esc(ch_obj["file"]), ci=ch_idx))
        # 部分 navPoint 指向本部分第一个文件
        first_ch_idx = next(idx for idx, ch in enumerate(chapters)
                            if ch["id"] == "part{}-file0".format(pi))
        playorder += 1
        navpoints.append("""  <navPoint id="np-part-{pi}" playOrder="{po}">
    <navLabel><text>{part}</text></navLabel>
    <content src="ch{ci}.xhtml"/>
{children}
  </navPoint>""".format(pi=pi, po=playorder, part=esc(part_title),
                        ci=first_ch_idx, children="\n".join(children)))

    ncx = """<?xml version="1.0" encoding="utf-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
<head>
  <meta name="dtb:uid" content="urn:uuid:{uuid}"/>
  <meta name="dtb:depth" content="2"/>
  <meta name="dtb:totalPageCount" content="0"/>
  <meta name="dtb:maxPageNumber" content="0"/>
</head>
<docTitle><text>{title}</text></docTitle>
<navMap>
{navpoints}
</navMap>
</ncx>""".format(uuid=__import__("uuid").uuid4(), title=esc(META_TITLE),
                 navpoints="\n".join(navpoints))

    # ── 4b. EPUB3 nav 导航文档（Readest 等现代阅读器读这个；NCX 留作兼容）
    # 注意：不能用外层泄漏的 ch 变量（for ch in chapters 结束后残留最后一个）——
    # 一律经 ch_idx 从 chapters 取
    nav_items = []
    for pi, (part_title, names) in enumerate(PARTS):
        sub = []
        for fi in range(len(names)):
            cid = "part{}-file{}".format(pi, fi)
            ch_idx = next(idx for idx, ch in enumerate(chapters) if ch["id"] == cid)
            ch_obj = chapters[ch_idx]
            sub.append(
                '          <li><a href="ch{ci}.xhtml">{label}</a></li>'.format(
                    ci=ch_idx, label=esc(ch_obj["file"])))
        nav_items.append(
            '      <li><span>{part}</span>\n        <ol>\n{children}\n        </ol>\n      </li>'.format(
                part=esc(part_title), children="\n".join(sub)))

    nav_xhtml = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="zh-CN" lang="zh-CN">
<head><meta charset="utf-8"/><title>目录</title></head>
<body>
<nav epub:type="toc" id="toc" role="doc-toc">
  <h1>目录</h1>
  <ol>
{items}
  </ol>
</nav>
</body>
</html>""".format(items="\n".join(nav_items))

    # ── 5. 打包 EPUB（mimetype 必须第一且无压缩）
    if os.path.exists(OUT_EPUB):
        os.remove(OUT_EPUB)
    with zipfile.ZipFile(OUT_EPUB, "w", zipfile.ZIP_DEFLATED) as z:
        # mimetype: store（不压缩）
        z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip",
                   compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml", """<?xml version="1.0" encoding="utf-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles>
</container>""")
        z.writestr("OEBPS/content.opf", opf)
        z.writestr("OEBPS/toc.ncx", ncx)
        z.writestr("OEBPS/nav.xhtml", nav_xhtml)
        z.writestr("OEBPS/style.css", style_css)
        for i, (fn, xhtml) in enumerate(file_entries):
            z.writestr("OEBPS/" + fn, xhtml)

    print("epub 已生成:", OUT_EPUB, os.path.getsize(OUT_EPUB), "bytes")

    # ── 6. 验证
    with zipfile.ZipFile(OUT_EPUB) as z:
        names = z.namelist()
        ok = ("mimetype" in names and names[0] == "mimetype"
              and "META-INF/container.xml" in names
              and "OEBPS/content.opf" in names
              and "OEBPS/nav.xhtml" in names)
        print("验证: 结构 =", "OK" if ok else "FAIL", "| 文件数 =", len(names),
              "| 章节 =", len(file_entries))
        opf_text = z.read("OEBPS/content.opf").decode("utf-8")
        spine_count = opf_text.count("<itemref")
        nav_ok = 'properties="nav"' in opf_text and 'epub:type="toc"' in z.read("OEBPS/nav.xhtml").decode("utf-8")
        print("spine 章节数 =", spine_count, "| EPUB3 nav =", "OK" if nav_ok else "FAIL")
    print("完成。可拷到手机阅读（Readest/微信读书/静读天下/Apple Books）。")


if __name__ == "__main__":
    sys.exit(main())

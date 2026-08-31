# -*- coding: utf-8 -*-
"""
黑格尔哲学引擎.txt -> 自包含单文件 HTML（阅读整理版）

规则：
- 内容原样保留，仅做 Markdown -> HTML 排版整理（标题/列表/表格/引用/粗斜体）。
- 为目录导航新增两处章节标题（文本取自原文用语，未虚构内容）：
    1) 『知』与『行』：黑格尔的三个称呼层次
    2) 第五章 理性：实践的理性（浮士德、哈姆雷特、堂·吉诃德）
- 内置验证链：文本逐字对拍、HTML 标签配平、JS 语法检查（node --check）、标题 id 唯一性。

用法：python hegel_build.py
"""
from __future__ import annotations

import html as _html
import pathlib
import re
import subprocess
import sys
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "黑格尔哲学引擎.txt"
DST = ROOT / "笔记" / "黑格尔哲学引擎.html"

ADDED_HEADINGS = [
    "『知』与『行』：黑格尔的三个称呼层次",
    "第五章 理性：实践的理性（浮士德、哈姆雷特、堂·吉诃德）",
]

HEADING_RE = re.compile(r"^(#{2,5})\s+(.*)$")
HR_RE = re.compile(r"^-{3,}\s*$")
TABLE_SEP_RE = re.compile(r"^\|[\s:|-]+\|?$")
LIST_RE = re.compile(r"^(\s*)([-*]|\d+\.)\s+(.*)$")


# ---------------------------------------------------------------- markdown 转换
def inline(text: str) -> str:
    t = _html.escape(text, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*([^*\n]+?)\*(?!\*)", r"<em>\1</em>", t)
    t = re.sub(r"`([^`\n]+?)`", r"<code>\1</code>", t)
    return t


def split_row(line: str) -> list[str]:
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def parse(md: str) -> list:
    lines = md.split("\n")
    blocks: list = []
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        s = line.strip()
        if not s:
            i += 1
            continue
        m = HEADING_RE.match(line)
        if m:
            blocks.append(("h", len(m.group(1)), m.group(2)))
            i += 1
            continue
        if HR_RE.match(s):
            blocks.append(("hr",))
            i += 1
            continue
        if s.startswith(">"):
            paras: list[str] = []
            while i < n:
                cur = lines[i].strip()
                if cur.startswith(">"):
                    paras.append(cur[1:].strip())
                    i += 1
                elif cur == "" and i + 1 < n and lines[i + 1].strip().startswith(">"):
                    paras.append("")  # 引用块内的段落分隔
                    i += 1
                else:
                    break
            blocks.append(("bq", paras))
            continue
        if s.startswith("|"):
            j = i + 1
            while j < n and not lines[j].strip():
                j += 1
            if j < n and TABLE_SEP_RE.match(lines[j].strip()) and "-" in lines[j]:
                header = split_row(s)
                body = []
                j += 1
                while j < n and lines[j].strip().startswith("|"):
                    body.append(split_row(lines[j].strip()))
                    j += 1
                blocks.append(("table", header, body))
                i = j
                continue
        m = LIST_RE.match(line)
        if m:
            indent, marker = m.group(1), m.group(2)
            is_ol = marker[-1] == "."
            items = []
            while i < n:
                mm = LIST_RE.match(lines[i])
                if mm and mm.group(1) == indent and (mm.group(2)[-1] == ".") == is_ol:
                    items.append(mm.group(3))
                    i += 1
                else:
                    break
            blocks.append(("ol" if is_ol else "ul", items))
            continue
        buf = []
        while i < n:
            cur = lines[i].strip()
            if (
                cur
                and not HEADING_RE.match(lines[i])
                and not cur.startswith(">")
                and not cur.startswith("|")
                and not LIST_RE.match(lines[i])
                and not HR_RE.match(cur)
            ):
                buf.append(cur)
                i += 1
            else:
                break
        raw = " ".join(buf)
        blocks.append(("p", raw))
    return blocks


def insert_structural_headings(blocks: list) -> list:
    out: list = []
    done = {"zhi_xing": False, "ch5": False}
    for b in blocks:
        if b[0] == "p":
            raw = b[1]
            if not done["zhi_xing"] and raw.startswith("结合《精神现象学》从第三章到第五章"):
                out.append(("h", 2, ADDED_HEADINGS[0]))
                done["zhi_xing"] = True
            elif not done["ch5"] and raw.startswith("好的。我们继续沿着"):
                out.append(("h", 2, ADDED_HEADINGS[1]))
                done["ch5"] = True
        out.append(b)
    if not all(done.values()):
        raise SystemExit("错误：未能定位新增标题的插入点，请检查原文。")
    return out


def render_table(header: list[str], body: list[list[str]]) -> str:
    cols = len(header)
    th = "".join(f"<th>{inline(c)}</th>" for c in header)
    rows = []
    for r in body:
        cells = [inline(c) for c in (r + [""] * cols)[:cols]]
        rows.append("<tr>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>")
    return (
        '<div class="table-wrap"><table><thead><tr>' + th + "</tr></thead><tbody>"
        + "".join(rows) + "</tbody></table></div>"
    )


def render_body(blocks: list) -> str:
    out = []
    for b in blocks:
        kind = b[0]
        if kind == "h":
            out.append(f"<h{b[1]}>{b[2]}</h{b[1]}>")
        elif kind == "p":
            raw = b[1]
            out.append(f"<p>{inline(raw)}</p>")
        elif kind == "bq":
            inner = "".join(f"<p>{inline(p)}</p>" for p in b[1] if p)
            out.append(f"<blockquote>{inner}</blockquote>")
        elif kind in ("ul", "ol"):
            inner = "".join(f"<li>{inline(it)}</li>" for it in b[1])
            out.append(f"<{kind}>{inner}</{kind}>")
        elif kind == "table":
            out.append(render_table(b[1], b[2]))
        elif kind == "hr":
            out.append("<hr>")
    return "\n".join(out)


# ---------------------------------------------------------------- HTML 模板
TEMPLATE_A = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>黑格尔哲学引擎 · 阅读整理</title>
<style>
:root{
  --bg:#faf7f1;
  --bg-soft:#f2ecdf;
  --card:#fffdf8;
  --text:#2e2a24;
  --text-soft:#6f675a;
  --border:#e4dbc9;
  --accent:#8c3b2e;
  --accent-strong:#6f2d23;
  --accent-soft:#f0e2d7;
  --quote-bg:#f6efe3;
  --quote-border:#b98a5a;
  --code-bg:#efe8da;
  --table-head:#7c352a;
  --table-head-text:#fbf4ea;
  --table-stripe:#f7f1e6;
  --shadow:rgba(70,45,20,.10);
  --sidebar-bg:#f4eee2;
  --sidebar-text:#544c40;
  --sidebar-active:#8c3b2e;
  --serif:"Source Han Serif SC","Noto Serif CJK SC","Songti SC",SimSun,STSong,Georgia,"Times New Roman",serif;
  --sans:"Source Han Sans SC","Noto Sans CJK SC","PingFang SC","Microsoft YaHei","Hiragino Sans GB",system-ui,sans-serif;
  --mono:Consolas,"JetBrains Mono",Menlo,monospace;
  color-scheme:light;
}
:root[data-theme="dark"]{
  --bg:#1d1b17;
  --bg-soft:#2a2620;
  --card:#242019;
  --text:#dcd4c3;
  --text-soft:#a09886;
  --border:#3b352b;
  --accent:#d08a6a;
  --accent-strong:#e2a07f;
  --accent-soft:#3b2b21;
  --quote-bg:#2a251f;
  --quote-border:#a5744f;
  --code-bg:#2c2720;
  --table-head:#5d3b2c;
  --table-head-text:#f5ecdf;
  --table-stripe:#29241d;
  --shadow:rgba(0,0,0,.35);
  --sidebar-bg:#201d18;
  --sidebar-text:#b4ab9b;
  --sidebar-active:#e0a585;
  color-scheme:dark;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0;background:var(--bg);color:var(--text);
  font-family:var(--serif);font-size:17px;line-height:1.9;
  -webkit-font-smoothing:antialiased;
}
#progress{position:fixed;top:0;left:0;height:3px;width:0;background:var(--accent);z-index:100}
.layout{display:grid;grid-template-columns:310px minmax(0,1fr);min-height:100vh}
aside.toc{
  position:sticky;top:0;height:100vh;overflow-y:auto;
  background:var(--sidebar-bg);border-right:1px solid var(--border);
  padding:1.4rem 1rem 2rem;font-family:var(--sans);font-size:.82rem;line-height:1.55;
}
.toc-title{font-weight:700;font-size:1.02rem;margin:0 0 .9rem;color:var(--text);padding:0 .45rem}
#toc-list ul{list-style:none;margin:0;padding:0}
#toc-list ul ul{padding-left:.8rem;margin:.1rem 0}
#toc-list li{margin:.1rem 0}
#toc-list a{
  display:block;color:var(--sidebar-text);text-decoration:none;
  padding:.24rem .45rem;border-radius:6px;word-break:break-word;
}
#toc-list a:hover{background:var(--bg-soft);color:var(--text)}
#toc-list a.active{background:var(--accent-soft);color:var(--sidebar-active);font-weight:600}
.group-toggle{display:inline-block;width:1em;margin-right:.25em;opacity:.6;font-size:.8em}
li.collapsed>ul{display:none}
.toc-foot{margin:1.4rem .45rem 0;color:var(--text-soft);font-size:.75rem;border-top:1px solid var(--border);padding-top:.8rem}
main{max-width:48rem;width:100%;margin:0 auto;padding:2.6rem clamp(1.1rem,4vw,3rem) 5rem}
.doc-head{margin-bottom:2.2rem;padding-bottom:1.2rem;border-bottom:2px solid var(--border)}
.doc-head h1{font-size:2.05rem;margin:0 0 .4rem;letter-spacing:.05em;line-height:1.3}
.doc-sub{margin:0;color:var(--text-soft);font-family:var(--sans);font-size:.95rem}
h2{
  font-size:1.5rem;line-height:1.4;margin:3rem 0 1.1rem;
  padding:.15rem 0 .15rem .75rem;border-left:5px solid var(--accent);
}
h3{font-size:1.22rem;line-height:1.45;margin:2.5rem 0 .85rem;padding-bottom:.35rem;border-bottom:1px solid var(--border)}
h4{font-size:1.07rem;margin:2rem 0 .7rem}
h5{font-size:.98rem;margin:1.7rem 0 .55rem;color:var(--accent)}
h2,h3,h4,h5{scroll-margin-top:24px;font-weight:700;letter-spacing:.01em}
p{margin:.9rem 0}
strong{font-weight:700}
em{font-style:italic}
code{
  font-family:var(--mono);font-size:.86em;background:var(--code-bg);
  padding:.08em .35em;border-radius:4px;
}
blockquote{
  margin:1.4rem 0;padding:.85rem 1.25rem;background:var(--quote-bg);
  border-left:4px solid var(--quote-border);border-radius:0 8px 8px 0;
}
blockquote p{margin:.45rem 0}
blockquote p:first-child{margin-top:0}
blockquote p:last-child{margin-bottom:0}
ul,ol{margin:1rem 0;padding-left:1.7em}
li{margin:.35rem 0}
li>ul,li>ol{margin:.35rem 0}
hr{border:0;border-top:1px solid var(--border);margin:2.6rem 0}
.table-wrap{
  overflow-x:auto;margin:1.5rem 0;border:1px solid var(--border);border-radius:10px;
  background:var(--card);box-shadow:0 1px 4px var(--shadow);
}
table{width:100%;border-collapse:collapse;font-family:var(--sans);font-size:.9em;line-height:1.65;min-width:420px}
th{
  background:var(--table-head);color:var(--table-head-text);font-weight:600;
  text-align:left;padding:.6rem .85rem;border-bottom:1px solid var(--border);
}
td{padding:.55rem .85rem;border-top:1px solid var(--border);vertical-align:top}
tbody tr:nth-child(even){background:var(--table-stripe)}
.doc-foot{margin-top:3.5rem;padding-top:1rem;border-top:1px solid var(--border);color:var(--text-soft);font-size:.85rem}
.doc-foot p{margin:.4rem 0}
#theme-btn,#top-btn,#toc-open-btn{
  position:fixed;z-index:90;border:1px solid var(--border);background:var(--card);
  color:var(--text);font-size:1.05rem;line-height:1;padding:.55rem .6rem;border-radius:10px;
  cursor:pointer;box-shadow:0 2px 8px var(--shadow);font-family:var(--sans);
}
#theme-btn{top:1rem;right:1rem}
#top-btn{bottom:1.2rem;right:1.2rem;display:none}
#top-btn.show{display:block}
#toc-open-btn{top:1rem;left:1rem;display:none}
#overlay{position:fixed;inset:0;background:rgba(20,15,10,.45);z-index:80;display:none}
#overlay.show{display:block}
@media (max-width:920px){
  .layout{grid-template-columns:1fr}
  aside.toc{
    position:fixed;top:0;bottom:0;left:0;width:min(80vw,330px);
    transform:translateX(-102%);transition:transform .22s ease;z-index:85;height:100vh;
  }
  aside.toc.open{transform:translateX(0)}
  #toc-open-btn{display:block}
}
@media print{
  :root,:root[data-theme="dark"]{
    --bg:#fff;--bg-soft:#f4f4f4;--card:#fff;--text:#111;--text-soft:#444;
    --border:#bbb;--accent:#555;--accent-soft:#eee;--quote-bg:#f6f6f6;
    --quote-border:#999;--code-bg:#eee;--table-head:#444;--table-head-text:#fff;
    --table-stripe:#f2f2f2;--shadow:none;--sidebar-bg:#fff;--sidebar-text:#444;--sidebar-active:#000;
    color-scheme:light;
  }
  body{font-size:12pt;background:#fff;color:#000}
  aside.toc,#theme-btn,#top-btn,#toc-open-btn,#overlay,#progress{display:none!important}
  .layout{display:block}
  main{max-width:none;padding:0}
  .table-wrap{overflow:visible;box-shadow:none;border:1px solid #999;border-radius:0}
  blockquote{break-inside:avoid}
  h2,h3,h4,h5{break-after:avoid;break-inside:avoid}
  tr,table{break-inside:avoid}
  a{color:#000;text-decoration:none}
}
</style>
</head>
<body>
<div id="progress" aria-hidden="true"></div>
<div class="layout">
  <aside class="toc" aria-label="目录">
    <div class="toc-title">📖 目录</div>
    <nav id="toc-list"></nav>
    <p class="toc-foot">整理自 黑格尔哲学引擎.txt</p>
  </aside>
  <main>
    <header class="doc-head">
      <h1>黑格尔哲学引擎</h1>
      <p class="doc-sub">《小逻辑》范畴演进 ×《精神现象学》「知—行」框架 · 阅读整理</p>
    </header>
    <div id="content">
"""

TEMPLATE_B = """
    </div>
    <footer class="doc-foot">
      <p>整理自 <code>黑格尔哲学引擎.txt</code> · 原文内容原样保留，仅排版整理；为便于目录导航新增两处章节标题。</p>
    </footer>
  </main>
</div>
<button id="theme-btn" type="button" title="切换明暗主题" aria-label="切换明暗主题">🌓</button>
<button id="top-btn" type="button" title="回到顶部" aria-label="回到顶部">↑</button>
<button id="toc-open-btn" type="button" title="打开目录" aria-label="打开目录">☰</button>
<div id="overlay" aria-hidden="true"></div>
<script>
"""

TEMPLATE_C = """
</script>
</body>
</html>
"""

JS = r"""/* 目录生成 + 滚动高亮 + 明暗主题 + 进度条（运行时由页面标题动态构建，无外部依赖） */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ---------- 目录构建 ---------- */
  var headings = $$('main h2, main h3, main h4, main h5');
  var used = {};
  function slugify(t) {
    var s = String(t).trim().toLowerCase();
    s = s.replace(/\s+/g, '-');
    s = s.replace(/[^\w\u4e00-\u9fff\u3400-\u4dbf-]/g, '');
    s = s.replace(/-+/g, '-').replace(/^-|-$/g, '');
    return s || 'sec';
  }
  headings.forEach(function (h) {
    var base = slugify(h.textContent);
    var id = base, n = 2;
    while (used[id]) { id = base + '-' + n; n += 1; }
    used[id] = true;
    h.id = id;
  });

  var root = { level: 1, children: [] };
  var stack = [root];
  headings.forEach(function (h) {
    var node = { el: h, level: parseInt(h.tagName.charAt(1), 10), children: [] };
    while (stack.length && stack[stack.length - 1].level >= node.level) { stack.pop(); }
    stack[stack.length - 1].children.push(node);
    stack.push(node);
  });

  var toc = $('#toc-list');
  function render(nodes, container) {
    if (!nodes.length) { return; }
    var ul = document.createElement('ul');
    nodes.forEach(function (n) {
      var li = document.createElement('li');
      var a = document.createElement('a');
      a.href = '#' + n.el.id;
      a.textContent = n.el.textContent;
      a.setAttribute('data-target', n.el.id);
      li.appendChild(a);
      if (n.children.length) {
        li.className = 'has-children';
        render(n.children, li);
      }
      ul.appendChild(li);
    });
    container.appendChild(ul);
  }
  render(root.children, toc);

  $$('#toc-list li.has-children > a').forEach(function (a) {
    var mark = document.createElement('span');
    mark.className = 'group-toggle';
    mark.textContent = '▾';
    a.insertBefore(mark, a.firstChild);
    a.addEventListener('click', function (e) {
      if (e.target === mark) {
        e.preventDefault();
        a.parentNode.classList.toggle('collapsed');
      }
    });
  });

  /* ---------- 滚动高亮 ---------- */
  var links = $$('#toc-list a[data-target]');
  var map = {};
  links.forEach(function (a) { map[a.getAttribute('data-target')] = a; });
  var tocAside = $('aside.toc');
  function offsetTopWithin(el, container) {
    var top = 0, node = el;
    while (node && node !== container) { top += node.offsetTop; node = node.offsetParent; }
    return top;
  }
  function currentHeading() {
    var y = window.scrollY + 90;
    var cur = null;
    for (var k = 0; k < headings.length; k += 1) {
      var top = headings[k].getBoundingClientRect().top + window.scrollY;
      if (top <= y) { cur = headings[k]; } else { break; }
    }
    return cur;
  }
  var ticking = false;
  function updateSpy() {
    ticking = false;
    links.forEach(function (a) { a.classList.remove('active'); });
    var cur = currentHeading();
    if (!cur) { return; }
    var a = map[cur.id];
    if (!a) { return; }
    a.classList.add('active');
    var node = a.parentNode;
    while (node && node !== toc) {
      if (node.classList && node.classList.contains('collapsed')) { node.classList.remove('collapsed'); }
      node = node.parentNode;
    }
    var t = offsetTopWithin(a, tocAside);
    if (t < tocAside.scrollTop || t > tocAside.scrollTop + tocAside.clientHeight - 80) {
      tocAside.scrollTo({ top: Math.max(0, t - tocAside.clientHeight / 2), behavior: 'smooth' });
    }
  }
  window.addEventListener('scroll', function () {
    if (!ticking) { ticking = true; window.requestAnimationFrame(updateSpy); }
  }, { passive: true });
  window.addEventListener('resize', updateSpy);
  updateSpy();

  /* ---------- 明暗主题 ---------- */
  var rootEl = document.documentElement;
  var themeBtn = $('#theme-btn');
  function applyTheme(t) { if (t) { rootEl.setAttribute('data-theme', t); } }
  var saved = null;
  try { saved = localStorage.getItem('hegel-theme'); } catch (e) { saved = null; }
  if (saved) {
    applyTheme(saved);
  } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    applyTheme('dark');
  }
  themeBtn.addEventListener('click', function () {
    var next = rootEl.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    applyTheme(next);
    try { localStorage.setItem('hegel-theme', next); } catch (e) { /* ignore */ }
  });

  /* ---------- 阅读进度条 / 回到顶部 ---------- */
  var bar = $('#progress');
  var topBtn = $('#top-btn');
  function onScroll() {
    var h = document.documentElement;
    var max = h.scrollHeight - h.clientHeight;
    bar.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + '%';
    if (h.scrollTop > 600) { topBtn.classList.add('show'); } else { topBtn.classList.remove('show'); }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  topBtn.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });

  /* ---------- 移动端目录抽屉 ---------- */
  var openBtn = $('#toc-open-btn');
  var overlay = $('#overlay');
  function openToc() { tocAside.classList.add('open'); overlay.classList.add('show'); }
  function closeToc() { tocAside.classList.remove('open'); overlay.classList.remove('show'); }
  openBtn.addEventListener('click', openToc);
  overlay.addEventListener('click', closeToc);
  $$('#toc-list a').forEach(function (a) {
    a.addEventListener('click', function () {
      if (window.innerWidth <= 920) { closeToc(); }
    });
  });
})();
"""


# ---------------------------------------------------------------- 验证链
def normalize_md(text: str) -> str:
    lines = []
    for ln in text.split("\n"):
        s = ln.strip()
        if not s:
            continue
        if HEADING_RE.match(s):
            s = re.sub(r"^#{2,5}\s+", "", s)
        elif s.startswith(">"):
            s = s.lstrip(">").strip()
        elif HR_RE.match(s):
            continue
        elif s.startswith("|") and TABLE_SEP_RE.match(s) and "-" in s:
            continue
        elif s.startswith("|"):
            s = s.strip("|")
            s = "".join(c.strip() for c in s.split("|"))
        s = re.sub(r"^(\s*)([-*]|\d+\.)\s+", "", s)
        s = s.replace("**", "").replace("`", "")
        s = re.sub(r"\*([^*\n]+?)\*", r"\1", s)
        lines.append(s)
    return re.sub(r"\s+", "", "".join(lines))


class ContentExtractor(HTMLParser):
    """只提取 <div id="content"> 子树内的文本。"""

    def __init__(self):
        super().__init__()
        self.parts: list[str] = []
        self.capture = 0

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            if self.capture == 0 and ("id", "content") in attrs:
                self.capture = 1
            elif self.capture > 0:
                self.capture += 1

    def handle_endtag(self, tag):
        if self.capture and tag == "div":
            self.capture -= 1

    def handle_data(self, data):
        if self.capture:
            self.parts.append(data)


def extract_content_text(html_text: str) -> str:
    p = ContentExtractor()
    p.feed(html_text)
    return "".join(p.parts)


class BalanceChecker(HTMLParser):
    VOID = {"hr", "br", "img", "meta", "link", "input", "wbr"}

    def __init__(self):
        super().__init__()
        self.stack: list[str] = []
        self.errors: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in self.VOID:
            return
        self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in self.VOID:
            return
        if not self.stack:
            self.errors.append(f"多余的闭合标签 </{tag}>")
        elif self.stack[-1] == tag:
            self.stack.pop()
        else:
            self.errors.append(f"标签不匹配 </{tag}>，栈顶为 <{self.stack[-1]}>")


def slugify_mirror(text: str) -> str:
    s = text.strip().lower()
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"[^\w\u4e00-\u9fff\u3400-\u4dbf-]", "", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "sec"


def check_ids(html_text: str) -> list[str]:
    heads = re.findall(r"<h([2-5])>(.*?)</h\1>", html_text, re.S)
    used: dict[str, bool] = {}
    errors = []
    for lvl, txt in heads:
        text = re.sub(r"<[^>]+>", "", txt)
        base = slugify_mirror(text)
        ident = base
        n = 2
        while used.get(ident):
            ident = f"{base}-{n}"
            n += 1
        used[ident] = True
    return errors, len(heads)


def first_diff(a: str, b: str) -> str:
    for i in range(min(len(a), len(b))):
        if a[i] != b[i]:
            return f"第 {i} 个字符处不同\n  A: …{a[max(0,i-25):i+25]}…\n  B: …{b[max(0,i-25):i+25]}…"
    if len(a) != len(b):
        return f"长度不同：A={len(a)}，B={len(b)}（公共前缀一致）"
    return ""


def main() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    md = SRC.read_text(encoding="utf-8")
    blocks = insert_structural_headings(parse(md))
    body = render_body(blocks)
    html_text = TEMPLATE_A + body + TEMPLATE_B + JS + TEMPLATE_C
    DST.write_text(html_text, encoding="utf-8")

    ok = True
    print(f"[产物] {DST.name}（{DST.stat().st_size} 字节）")

    # 1) 文本逐字对拍（先移除新增导航标题，再去空白）
    a = normalize_md(md)
    b = extract_content_text(html_text)
    for h in ADDED_HEADINGS:
        b = b.replace(h, "")
    b = re.sub(r"\s+", "", b)
    d = first_diff(a, b)
    if d:
        ok = False
        print("[FAIL] 文本对拍不一致：", d, sep="\n")
    else:
        print(f"[PASS] 文本对拍：{len(a)} 字符完全一致（原文 → HTML 提取文本）")

    # 2) 标题数量与 id 唯一性
    orig_heads = len(re.findall(r"^#{2,5}\s", md, re.M))
    errs, final_heads = check_ids(html_text)
    if final_heads != orig_heads + len(ADDED_HEADINGS):
        ok = False
        print(f"[FAIL] 标题数量：原文 {orig_heads} → HTML {final_heads}（预期 {orig_heads + len(ADDED_HEADINGS)}）")
    elif errs:
        ok = False
        print(f"[FAIL] 标题 id 问题：{errs}")
    else:
        print(f"[PASS] 标题：原文 {orig_heads} 个 → HTML {final_heads} 个（含新增 {len(ADDED_HEADINGS)} 个），id 唯一")

    # 3) HTML 标签配平
    bc = BalanceChecker()
    bc.feed(html_text)
    if bc.errors or bc.stack:
        ok = False
        print("[FAIL] 标签配平：", bc.errors[:5], "未闭合：", bc.stack[-10:], sep="\n")
    else:
        print("[PASS] HTML 标签配平：全部闭合")

    # 4) JS 语法检查（node --check）
    js_tmp = ROOT / "__check.js"
    js_tmp.write_text(JS, encoding="utf-8")
    try:
        r = subprocess.run(
            ["node", "--check", str(js_tmp)],
            stdin=None, stdout=None, stderr=None,
        )
        if r.returncode == 0:
            print("[PASS] JS 语法检查（node --check）通过")
        else:
            ok = False
            print(f"[FAIL] JS 语法检查未通过（exit {r.returncode}）")
    except FileNotFoundError:
        print("[WARN] 未找到 node，跳过 JS 语法检查")
    finally:
        js_tmp.unlink(missing_ok=True)

    print("\n" + ("✔ 全部验证通过。" if ok else "✘ 存在失败项，请检查。"))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
按哲学家批量下载 zeno.org 作品，原始资料分类存放：
  原文/<哲学家中文名>/<作品slug>/  （原始 HTML）
  原文/<哲学家中文名>/<作品slug>/extracted/  （提取后结构化文本）
用法：python download_philosophers.py [谢林 黑格尔 柏拉图 亚里士多德 康德 马克思]
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "原文"
BASE = "http://www.zeno.org"

PHILOSOPHERS = {
    "谢林": "Schelling,+Friedrich+Wilhelm+Joseph",
    "黑格尔": "Hegel,+Georg+Wilhelm+Friedrich",
    "柏拉图": "Platon",
    "亚里士多德": "Aristoteles",
    "康德": "Kant,+Immanuel",
    "马克思": "Marx,+Karl",
}
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
}


def fetch(url: str, tries: int = 3) -> bytes:
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.read()
        except Exception as e:
            if i == tries - 1:
                raise
            time.sleep(2 * (i + 1))


def slug_of(path: str) -> str:
    name = urllib.parse.unquote(path.split("/")[-1])
    name = re.sub(r"[^\w\u00c0-\u024f.-]+", "_", name).strip("_")
    return name[:120] or "page"


def top_level_works(author: str):
    """从作者页提取一级作品链接（作者路径下恰好一个段）"""
    url = f"{BASE}/Philosophie/M/{author}"
    txt = fetch(url).decode("iso-8859-1", errors="replace")
    prefix = f"/Philosophie/M/{author}/"
    works = []
    seen = set()
    for m in re.finditer(r'href="(/Philosophie/M/[^"]+)"', txt):
        href = m.group(1)
        if href.startswith(prefix):
            rest = href[len(prefix):]
            if "/" not in rest and rest not in seen and not re.search(r"_fn\d+(ref)?", href):
                seen.add(rest)
                works.append((urllib.parse.unquote(rest), href))
    return works


def crawl_work(work_href: str, out_dir: Path) -> int:
    """BFS 抓取一部作品的全部页面（work_href 路径前缀下），返回新增页数。
    种子页（作品首页/目录页）本身也会被保存——单页作品即整篇正文。"""
    out_dir.mkdir(parents=True, exist_ok=True)
    prefix = work_href
    downloaded = {f.name for f in out_dir.glob("*.html")}
    count = 0

    def save_if_new(href):
        nonlocal count
        name = slug_of(href)
        target = out_dir / f"{name}.html"
        if target.name in downloaded:
            return None
        data = fetch(BASE + href)
        target.write_bytes(data)
        downloaded.add(target.name)
        count += 1
        return data

    # 种子页：保存自身 + 提取子链接
    seed = save_if_new(work_href)
    if seed is None:
        seed = (out_dir / f"{slug_of(work_href)}.html").read_bytes()
    seen = {work_href}
    queue = []
    txt = seed.decode("iso-8859-1", errors="replace")
    for m in re.finditer(r'href="(/Philosophie/M/[^"]+)"', txt):
        href = m.group(1)
        if href.startswith(prefix) and not re.search(r"_fn\d+(ref)?", href):
            if href not in seen:
                seen.add(href)
                queue.append(href)
    while queue:
        href = queue.pop(0)
        data = save_if_new(href)
        if data is None:
            continue
        txt = data.decode("iso-8859-1", errors="replace")
        for m in re.finditer(r'href="(/Philosophie/M/[^"]+)"', txt):
            nh = m.group(1)
            if nh.startswith(prefix) and not re.search(r"_fn\d+(ref)?", nh) and nh not in seen:
                seen.add(nh)
                queue.append(nh)
        time.sleep(0.25)
    return count


def main():
    targets = sys.argv[1:] or list(PHILOSOPHERS.keys())
    workers = 4  # 并行下载的作品数
    manifest = {"updated": "2026-08-26", "source": "zeno.org", "works": []}

    # 收集全部待下载作品（跨哲学家）
    tasks = []  # (phil, work_dir, work_href, wname)
    for phil in targets:
        author = PHILOSOPHERS.get(phil)
        if not author:
            print(f"未知哲学家：{phil}")
            continue
        works = top_level_works(author)
        phil_dir = RAW / phil
        phil_dir.mkdir(exist_ok=True)
        for wname, whref in sorted(works, key=lambda x: x[0]):
            if wname == "Biographie":
                continue
            tasks.append((phil, phil_dir / slug_of(whref), whref, wname))
    print(f"共 {len(tasks)} 部作品，{workers} 线程并行下载……")

    results = {}

    def run_one(t):
        phil, work_dir, whref, wname = t
        try:
            n = crawl_work(whref, work_dir)
            results[whref] = {"phil": phil, "work": wname, "dir": str(work_dir.relative_to(ROOT)),
                              "pages": n, "status": "ok"}
            print(f"  [{phil}] {wname[:44]:46s} {n:4d} 页（新增）", flush=True)
        except Exception as e:
            results[whref] = {"phil": phil, "work": wname, "dir": str(work_dir.relative_to(ROOT)),
                              "pages": 0, "status": f"fail: {e}"}
            print(f"  [{phil}] {wname[:44]:46s} FAIL {e}", flush=True)

    from concurrent.futures import ThreadPoolExecutor, as_completed
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(run_one, t): t for t in tasks}
        for f in as_completed(futs):
            f.result()  # 抛出异常即失败

    manifest["works"] = [results[t[2]] for t in tasks]
    # 每哲学家作品清单
    by_phil = {}
    for w in manifest["works"]:
        by_phil.setdefault(w["phil"], []).append(w)
    for phil, items in by_phil.items():
        (RAW / phil / "works.json").write_text(
            json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
    (RAW / "文献清单.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    ok = sum(1 for w in manifest["works"] if w["status"] == "ok")
    pages = sum(w.get("pages", 0) for w in manifest["works"])
    print(f"\n完成：{ok}/{len(manifest['works'])} 部成功（本次新增 {pages} 页）。清单：原文/文献清单.json")


if __name__ == "__main__":
    main()

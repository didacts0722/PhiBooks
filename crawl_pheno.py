# -*- coding: utf-8 -*-
"""BFS 爬取 zeno.org 精神现象学全部子页面"""
import re
import sys
import time
import urllib.request
import urllib.parse
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUT = Path(__file__).resolve().parent / "原文" / "Phänomenologie_des_Geistes"
BASE = "http://www.zeno.org"
BOOK = "/Philosophie/M/Hegel,+Georg+Wilhelm+Friedrich/Ph%C3%A4nomenologie+des+Geistes"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
}


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def slug(href: str) -> str:
    name = urllib.parse.unquote(href.split("/")[-1])
    name = re.sub(r"[^\w\u00c0-\u024f.-]+", "_", name).strip("_")
    return name[:160] or "page"


def extract_nav_links(html_bytes: bytes):
    txt = html_bytes.decode("iso-8859-1", errors="replace")
    links = set()
    for m in re.finditer(r'href="(/Philosophie/M/Hegel[^"]*)"', txt):
        href = m.group(1)
        if BOOK in href and not re.search(r"_fn\d+(ref)?", href):
            links.add(href)
    return links


def main():
    seen = set()
    queue = []
    # 种子 1：TOC 页（如存在）
    toc = Path(__file__).resolve().parent / "原文" / "phaen_toc.html"
    if toc.exists():
        for href in extract_nav_links(toc.read_bytes()):
            if href not in seen:
                seen.add(href)
                queue.append(href)
    # 种子 2：已下载页面
    for f in OUT.glob("*.html"):
        try:
            data = f.read_bytes()
        except Exception:
            continue
        for href in extract_nav_links(data):
            if href not in seen:
                seen.add(href)
                queue.append(href)
    print(f"初始链接: {len(queue)}")

    downloaded = {f.name for f in OUT.glob("*.html")}
    new_pages = 0
    while queue:
        href = queue.pop(0)
        url = BASE + href
        name = slug(href)
        target = OUT / f"{name}.html"
        if target.name in downloaded:
            continue
        try:
            data = fetch(url)
            target.write_bytes(data)
            new_pages += 1
            print(f"  + {target.name} ({len(data)}B)")
            for nh in extract_nav_links(data):
                if nh not in seen:
                    seen.add(nh)
                    queue.append(nh)
            time.sleep(0.3)
        except Exception as e:
            print(f"  FAIL {href} -> {e}")
    print(f"\n新增页面: {new_pages}，共 {len(list(OUT.glob('*.html')))} 页")


if __name__ == "__main__":
    main()

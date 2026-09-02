# -*- coding: utf-8 -*-
"""
BFS 爬取 zeno.org 百科全书·逻辑学（Erster Teil）全部子页面。
从已下载的页面出发，解析导航树链接，逐级下载，直到没有新链接。
"""
import json
import re
import sys
import time
import urllib.request
import urllib.parse
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "原文" / "Enzyklopädie_Logik"
BASE = "http://www.zeno.org"
BOOK = "/Philosophie/M/Hegel,+Georg+Wilhelm+Friedrich/Enzyklop%C3%A4die+der+philosophischen+Wissenschaften+im+Grundrisse"
LOGIC_PART = "Erster+Teil.+Die+Wissenschaft+der+Logik."
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
    return name[:90] or "page"


def extract_nav_links(html_bytes: bytes):
    txt = html_bytes.decode("iso-8859-1", errors="replace")
    links = set()
    for m in re.finditer(r'href="(/Philosophie/M/Hegel[^"]*)"', txt):
        href = m.group(1)
        if BOOK in href and LOGIC_PART in href and "Fu%C3%9Fnoten" not in href:
            links.add(href)
    return links


def main():
    seen = set()
    queue = []
    # 初始种子：已下载的逻辑学页面（从其 HTML 中提取导航链接）
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

    downloaded = set()
    for f in OUT.glob("*.html"):
        downloaded.add(f.name)

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

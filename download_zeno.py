# -*- coding: utf-8 -*-
"""
从 zeno.org 下载黑格尔两本书的原文页（原始 HTML 字节保存，不做解析）。
- 精神现象学：序言/导言 + 第 I~VIII 章（含过渡页）
- 百科全书第一编（逻辑学）：三版序言 + Vorbegriff + 存在论/本质论/概念论
输出：原文/<book>/ 下的原始 HTML + manifest.json（url/保存名/字节数/编码声明）
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
RAW_DIR = ROOT / "原文"
PHENO = "Phänomenologie_des_Geistes"
ENZ = "Enzyklopädie_Logik"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
    "Accept-Language": "de-DE,de;q=0.9,en;q=0.8",
}
BASE = "http://www.zeno.org"


def extract_links(toc_path: Path, prefix: str):
    """从已保存的目录页提取指向 prefix 下各页的链接（去重、保序）"""
    c = toc_path.read_text(encoding="utf-8", errors="replace")
    links = []
    seen = set()
    for m in re.finditer(r'href="(/Philosophie/M/Hegel[^"]*)"', c):
        href = m.group(1)
        if prefix in href and href not in seen:
            seen.add(href)
            links.append(href)
    return links


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def slug(href: str) -> str:
    """从 URL 生成可读文件名（解码、去路径前缀）"""
    name = href.split("/")[-1]
    name = urllib.request.unquote(name)
    name = re.sub(r"[^\w\u00c0-\u024f.-]+", "_", name).strip("_")
    return name[:80] or "page"


def download_book(book_dir: str, toc_path: Path, prefix: str, only: str | None = None, exclude: tuple = ()):
    out_dir = RAW_DIR / book_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    links = extract_links(toc_path, prefix)
    manifest = []
    for href in links:
        if only and only not in href:
            continue
        if any(e in href for e in exclude):
            continue
        url = BASE + href
        name = slug(href)
        target = out_dir / f"{name}.html"
        try:
            data = fetch(url)
            target.write_bytes(data)
            # 编码声明
            head = data[:4096].decode("latin-1", errors="replace")
            cs = re.search(r'charset=["\']?([\w-]+)', head, re.I)
            manifest.append({
                "url": url, "file": target.name,
                "bytes": len(data), "charset": cs.group(1) if cs else None,
            })
            print(f"  OK {target.name}  {len(data)}B  charset={cs.group(1) if cs else '?'}")
        except Exception as e:
            print(f"  FAIL {href} -> {e}")
    (out_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"== {book_dir}: {len(manifest)} 页已保存到 {out_dir}")


def main():
    print("=== 精神现象学 ===")
    download_book(
        PHENO,
        ROOT / "原文" / "phaen_toc.html",
        "/Ph%C3%A4nomenologie+des+Geistes",
        exclude=("epub", "Biographie"),
    )
    print()
    print("=== 百科全书·逻辑学 ===")
    download_book(
        ENZ,
        ROOT / "原文" / "enz_toc.html",
        "/Enzyklop%C3%A4die+der+philosophischen+Wissenschaften+im+Grundrisse",
        exclude=("Naturphilosophie", "Philosophie+des+Geistes", "Fu%C3%9Fnoten"),
    )
    print("\n完成。")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
独立功能：解压-读取无意识层（对话原始记录 zstd → 明文 JSONL）

用法：
  python decompress_unconscious.py            解压 对话归档/原始/session.jsonl.zstd → session.jsonl
  python decompress_unconscious.py --read     解压并打印对话概览（轮次/角色统计）

依赖：node:zlib 内置 zstd（Node 22+）——无需额外安装
注意：会话运行中最后帧不完整会失败——先归档最终版（python archive_unconscious.py）或等会话结束。
"""
import json
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
ZSTD = ROOT / "对话归档" / "原始" / "session.jsonl.zstd"
JSONL = ROOT / "对话归档" / "原始" / "session.jsonl"
TOOL = ROOT / "对话归档" / "工具" / "解压原始档.js"


def decompress() -> bool:
    r = subprocess.run(["node", str(TOOL)], cwd=ROOT, check=False, capture_output=True,
                       text=True, encoding="utf-8", errors="replace", timeout=300)
    out = ((r.stdout or "").strip() + "\n" + (r.stderr or "").strip()).strip()
    print(out)
    return r.returncode == 0 and JSONL.exists() and JSONL.stat().st_size > 1000


def overview():
    """对话概览：轮次/角色统计/最近主题"""
    if not JSONL.exists():
        print("明文档不存在——先解压（python decompress_unconscious.py）")
        return
    lines = [json.loads(l) for l in JSONL.read_text(encoding="utf-8").splitlines() if l.strip()]
    roles = {}
    turns = 0
    for o in lines:
        t = o.get("type", "")
        if t == "turn/start" or (t and "turn" in t and "start" in t):
            turns += 1
        role = o.get("role") or o.get("event", {}).get("role") or (o.get("content", {}) or {}).get("role", "")
        if role:
            roles[role] = roles.get(role, 0) + 1
    print(f"明文档: {JSONL.name}（{JSONL.stat().st_size / 1024 / 1024:.1f} MB，{len(lines)} 行）")
    print(f"轮次: {turns} | 角色分布: {roles}")
    # 最近 3 条消息内容摘要
    texts = []
    for o in reversed(lines):
        c = o.get("content")
        if isinstance(c, dict) and c.get("text"):
            texts.append(c["text"][:80])
        if len(texts) >= 3:
            break
    print("最近消息:")
    for t in reversed(texts):
        print("  ·", t)


if __name__ == "__main__":
    if "--read" in sys.argv:
        if not decompress():
            print("（解压失败——无法读取）")
        else:
            overview()
    else:
        ok = decompress()
        if not ok:
            print("[解压] 提示：会话运行中——先归档最终版（python archive_unconscious.py），或等会话结束")
        sys.exit(0 if ok else 1)

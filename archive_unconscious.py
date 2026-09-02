# -*- coding: utf-8 -*-
"""
独立功能：无意识层归档（对话原始记录 → 对话归档/原始/session.jsonl.zstd）

用法：
  python archive_unconscious.py            归档当前会话
  python archive_unconscious.py --all      归档全部会话（~/.dsh/sessions 所有项目）

与构建（build_recht/build_lp）解耦——独立功能，需要时手动运行。
"""
import json
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
DST = ROOT / "对话归档" / "原始" / "session.jsonl.zstd"


def sync_current():
    """复制当前会话（DSH_SESSION_JSONL）到归档"""
    r = subprocess.run(["node", str(ROOT / "对话归档" / "工具" / "同步原始档.js")],
                       cwd=ROOT, check=False, capture_output=True,
                       text=True, encoding="utf-8", errors="replace", timeout=60)
    print((r.stdout or "").strip() or (r.stderr or "").strip())


def sync_all():
    """归档全部项目会话到 对话归档/原始/全部会话/"""
    home = Path.home() / ".dsh" / "sessions"
    if not home.exists():
        print("未找到会话目录:", home)
        return
    out_dir = ROOT / "对话归档" / "原始" / "全部会话"
    out_dir.mkdir(parents=True, exist_ok=True)
    n = 0
    for proj in sorted(home.iterdir()):
        if not proj.is_dir():
            continue
        for sess in sorted(proj.iterdir()):
            if not sess.is_dir():
                continue
            f = sess / "session.jsonl.zstd"
            if f.exists():
                dst = out_dir / f"{proj.name}__{sess.name}.zstd"
                dst.write_bytes(f.read_bytes())
                n += 1
                print(f"  {dst.name}: {dst.stat().st_size / 1024 / 1024:.1f} MB")
    print(f"已归档 {n} 个会话 -> {out_dir}")


if __name__ == "__main__":
    if "--all" in sys.argv:
        sync_all()
    else:
        sync_current()

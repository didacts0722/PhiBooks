# -*- coding: utf-8 -*-
"""查看会话最后几条消息 + 导出完整会话为可读文本"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).parent.parent
SRC = ROOT / "对话归档" / "历史" / "conversations.json"


def load():
    return json.loads(SRC.read_text(encoding="utf-8"))


def walk(mapping, nid, out):
    node = mapping[nid]
    out.append(nid)
    for c in node.get("children") or []:
        walk(mapping, c, out)


def main():
    conv = load()[0]
    m = conv["mapping"]
    order = []
    walk(m, "root", order)

    msgs = []
    for nid in order:
        node = m[nid]
        msg = node.get("message")
        if not msg:
            continue
        for f in msg.get("fragments") or []:
            c = f.get("content")
            if isinstance(c, str) and c.strip():
                msgs.append((nid, f.get("type"), msg.get("inserted_at"), c))

    # 只打印最后 3 条（按时间排序后取尾部）
    tail = msgs[-3:]
    for nid, ty, ts, c in tail:
        print(f"===== {nid} [{ty}] {ts} =====")
        print(c[:1200])
        print()

    # 同时导出完整会话（可读文本）到工作区
    out_path = ROOT / "对话归档" / "历史" / "conversation_full.txt"
    with out_path.open("w", encoding="utf-8") as fp:
        fp.write(f"会话标题: {conv.get('title')}\n")
        fp.write(f"会话 id: {conv.get('id')}\n")
        fp.write(f"时间: {conv.get('inserted_at')} ~ {conv.get('updated_at')}\n")
        fp.write("=" * 60 + "\n\n")
        for nid, ty, ts, c in msgs:
            role = {"REQUEST": "用户", "RESPONSE": "助手", "THINK": "思考"}.get(ty, ty)
            fp.write(f"--- {role} [{ts}] ---\n{c}\n\n")
    print(f"完整会话已导出: {out_path}（{out_path.stat().st_size} 字节，{len(msgs)} 条片段）")


if __name__ == "__main__":
    main()

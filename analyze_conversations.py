# -*- coding: utf-8 -*-
"""解析 conversations.json：会话概览 + 用户提问序列 + 助手回复统计"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SRC = Path(__file__).parent / "_zip_extract" / "conversations.json"


def load():
    return json.loads(SRC.read_text(encoding="utf-8"))


def walk(mapping, nid, out):
    node = mapping[nid]
    out.append(nid)
    for c in node.get("children") or []:
        walk(mapping, c, out)


def main():
    data = load()
    print(f"会话数: {len(data)}")
    for conv in data:
        m = conv["mapping"]
        order = []
        walk(m, "root", order)

        msgs = []
        for nid in order:
            node = m[nid]
            msg = node.get("message")
            if not msg:
                continue
            texts = []
            for f in msg.get("fragments") or []:
                c = f.get("content")
                if isinstance(c, str) and c.strip():
                    texts.append((f.get("type"), c))
            if texts:
                msgs.append((nid, msg.get("model"), msg.get("inserted_at"), texts))

        users = [t for t in msgs if any(ty == "REQUEST" for ty, _ in t[3])]
        assist = [t for t in msgs if any(ty == "RESPONSE" for ty, _ in t[3])]
        other = [t for t in msgs if t not in users and t not in assist]
        tot = sum(len(c) for _, _, _, ts in msgs for _, c in ts)
        u_chars = sum(len(c) for _, _, _, ts in users for _, c in ts if _ == "REQUEST")
        a_chars = sum(len(c) for _, _, _, ts in assist for _, c in ts if _ == "RESPONSE")

        print(f"\n===== 会话: {conv.get('title')} =====")
        print(f"id: {conv.get('id')}")
        print(f"时间: {conv.get('inserted_at')} ~ {conv.get('updated_at')}")
        print(f"消息节点: {len(msgs)}（用户 {len(users)} / 助手 {len(assist)} / 其他 {len(other)}）")
        print(f"内容字符: 总计 {tot}（用户 {u_chars} / 助手 {a_chars}）")

        print("\n----- 用户提问序列 -----")
        for i, (nid, model, ts, texts) in enumerate(users, 1):
            txt = next(c for ty, c in texts if ty == "REQUEST")
            first = txt.strip().split("\n")[0]
            print(f"[{i:02d}] {ts[:16]}  {first[:130]}")

        print("\n----- 助手回复长度（按消息） -----")
        for i, (nid, model, ts, texts) in enumerate(assist, 1):
            a = sum(len(c) for ty, c in texts if ty == "RESPONSE")
            print(f"[{i:02d}] {ts[:16]}  {a} 字符  {model}")

        # 非 REQUEST/RESPONSE 的类型有哪些
        types = set()
        for _, _, _, texts in msgs:
            for ty, _ in texts:
                types.add(ty)
        print("\nfragment 类型:", types)


if __name__ == "__main__":
    main()

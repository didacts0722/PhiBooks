# -*- coding: utf-8 -*-
"""把 ch4「劳动≠阶级斗争」从 奴隶：恐惧与劳动(p.153) 移到 主人与奴隶(p.149)，
作为主奴寓言性（防误读）的补充；p.153 另留「恐惧=智慧之开端」短条。"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

P = Path(__file__).resolve().parent / "项目/现象学/notes" / "ch4.json"

ALLEGORY_SUPP = {
    "date": "2026-08-26",
    "title": "劳动≠阶级斗争：主奴寓言的劳动维度",
    "content": "这与「主奴=寓言」一脉相承（见上条防误读）：正因为主奴关系是自我意识阶段的逻辑形态、不是历史分期，其中的劳动就不是经济或阶级范畴。庄振华据此澄清：黑格尔在主奴处谈的不是政治经济压迫，而是自我意识阶段普遍的不对等人际模式；**劳动也不是阶级斗争的雏形**——他在奴仆劳动处「马上把笔锋一转去谈斯多亚主义」，并不顺着马克思的思路走向阶级颠覆。真正的要点是：**「劳动并不是关键，如何劳动才是关键」**——若仍以规律性的、外在化的方式改造物，劳动越卖力就越与事物本身相隔绝；劳动能否把个人引向共同体与世界本身这些根据，才是关键（庄振华《义解》第四章·主人与奴仆）。"
}

FEAR_SUPP = {
    "date": "2026-08-26",
    "title": "恐惧=智慧之开端",
    "content": "庄振华指出，黑格尔称奴仆的彻底恐惧为「智慧之开端」（der Anfang der Weisheit）：不经受物化处境的彻底震荡、不经历一切固定之物的瓦解，人就无法真正正视物、进入物的理路；恐惧不是主人恐吓造成的外在紧张，而是奴仆物化生存境况的必然产物（庄振华《义解》第四章·主人与奴仆）。这解释了恐惧何以是劳动塑造自我的前提。"
}


def main():
    data = json.loads(P.read_text(encoding="utf-8"))
    for g in data["gestalten"]:
        for b in g["bewegung"]:
            if b[0] == "主人与奴隶":
                if len(b) < 5 or b[4] is None:
                    while len(b) < 5:
                        b.append(None)
                    b[4] = []
                # 去掉可能重复的同题条
                b[4] = [s for s in b[4] if s.get("title") != ALLEGORY_SUPP["title"]]
                b[4].append(ALLEGORY_SUPP)
            elif b[0] == "奴隶：恐惧与劳动":
                if len(b) < 5 or b[4] is None:
                    while len(b) < 5:
                        b.append(None)
                    b[4] = []
                b[4] = [s for s in b[4] if "阶级斗争" not in s.get("title", "")]
                b[4].append(FEAR_SUPP)
    P.write_text(json.dumps(data, ensure_ascii=False, indent=1),
                 encoding="utf-8", newline="\n")
    print("ch4.json 已调整：劳动≠阶级斗争 → 主人与奴隶(p.149)；恐惧=智慧之开端 → 奴隶：恐惧与劳动(p.153)")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""小逻辑 notes 补充修正：mode/pages/整体定位/演绎链术语（新标准 2026-08-29）"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

CFG = {
    "vorbegriff": {
        "mode": "自我声明（先行概念式）：逻辑学概念的展开——对哲学史三种态度（形而上学/经验主义/直接知识）的瓦解 + 逻辑三环节（抽象知性·辩证·思辨）的声明",
        "pages": "§19–83",
        "loc": "**整体定位（概念链+演绎链，2026-08-29）**：小逻辑=引擎三段循环的自我演示——先行概念=引擎的**自我声明**（对哲学既有形态的瓦解：三种态度=设定/瓦解，§81 辩证环节=die absolute Negativität 的声明）；形态内环节=概念链，每环节=演绎链一步（每步「推出」非「并列」）。",
    },
    "sein": {
        "mode": "过渡模式（存在论式）：规定直接过渡到对方（Übergehen in Anderes）——概念环节的设定",
        "pages": "§84–111",
        "loc": "**整体定位（概念链+演绎链，2026-08-29）**：小逻辑=引擎三段循环的自我演示——存在论=**设定环节**（直接性介质→过渡做功）；形态内环节=概念链，每环节=演绎链一步（Sein→Nichts→Werden→Dasein 每步推出）。",
    },
    "essence": {
        "mode": "反思模式（本质论式）：规定通过对立面映现自身（Scheinen in das Andere）——判断环节的展开",
        "pages": "§112–159",
        "loc": "**整体定位（概念链+演绎链，2026-08-29）**：小逻辑=引擎三段循环的自我演示——本质论=**判断环节**（反思介质→映现做功：同一/差别/根据，实存/现象/现实）；形态内环节=概念链，每环节=演绎链一步。",
    },
    "begriff": {
        "mode": "发展模式（概念论式）：规定自由地展开自身（Entwickeln）——推论环节的重建",
        "pages": "§160–244",
        "loc": "**整体定位（概念链+演绎链，2026-08-29）**：小逻辑=引擎三段循环的自我演示——概念论=**推论环节**（自由介质→发展做功：概念→判断→推论，机械→化学→目的，生命→认识→绝对理念）；形态内环节=概念链，每环节=演绎链一步——**绝对理念（§236-244）=方法=引擎的自我认识（全书终点）**。",
    },
}

for name, cfg in CFG.items():
    f = Path(f"notes_lp/{name}.json")
    d = json.loads(f.read_text(encoding="utf-8"))
    g = d["gestalten"][0]
    g["mode"] = cfg["mode"]
    g["pages"] = cfg["pages"]
    # 整体定位插入 bestimmung 开头
    b = g.get("bestimmung", "")
    g["bestimmung"] = cfg["loc"] + "\n" + b
    # 演绎链术语：diagnose 开头补标注（若无）
    diag = g.get("diagnose", "")
    if diag and not diag.startswith("**演绎链"):
        g["diagnose"] = "**演绎链审查（2026-08-29 术语统一）**：" + diag
    f.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    json.loads(f.read_text(encoding="utf-8"))
    print(f"{name}: mode/pages/定位/演绎链术语 已补（bestimmung 前缀 {len(cfg['loc'])} 字）")

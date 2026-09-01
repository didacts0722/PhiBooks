# -*- coding: utf-8 -*-
"""
§260-329 段落归属映射（staat_sec_map.json）
zeno 内部国家法 7 页正文区无 § 标题（长文连续版式），此处按标准文本内容逐段标注。
段落顺序 = extract_zeno.extract_page 的 items 中 p 段顺序（已逐一核对 dump）。
附释与正文不区分，sec 标记所属 §（2026-08-27 用户裁定）。
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

MAP = {
    "Das_Innere_Staatsrecht.html": [
        260, 261, 261, 262, 263, 264, 265, 266, 267, 268, 268,
        269, 270, 270, 270, 270, 271, 271, 270, 270, 270,
    ],
    "Innere_Verfassung_für_sich.html": [
        272, 272, 272, 273, 273, 273, 273, 273, 273, 273, 274, 274,
    ],
    "a._Die_fürstliche_Gewalt.html": [
        275, 276, 277, 278, 278, 279, 279, 279, 280, 280, 281, 281,
        282, 282, 283, 284, 285, 286, 286,
    ],
    "b._Die_Regierungsgewalt.html": [
        287, 288, 289, 289, 289, 290, 291, 292, 293, 294, 294,
        295, 295, 295, 296, 296,
    ],
    "c._Die_gesetzgebende_Gewalt.html": [
        298, 299, 299, 300, 301, 301, 302, 302, 303, 303, 304, 305, 305,
        307, 308, 308, 309, 310, 310, 311, 311, 312, 313, 314, 315, 316,
        317, 317, 317, 317, 317, 317, 317, 318, 319, 319, 320, 320, 320, 320, 320,
    ],
    "II._Die_Souveränität_gegen_außen.html": [
        321, 322, 322, 323, 324, 324, 325, 326, 327, 328, 328, 328, 329,
    ],
}

# 校验：每页 sec 数 = extract_page 的 p 段数
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import extract_zeno  # noqa: E402

OUT = Path(r"原文/黑格尔/Grundlinien_der_Philosophie_des_Rechts")
ok = True
for fname, secs in MAP.items():
    d = extract_zeno.extract_page(OUT / fname)
    n_ps = sum(1 for it in d["items"] if it["type"] == "p")
    status = "OK" if n_ps == len(secs) else "MISMATCH"
    if n_ps != len(secs):
        ok = False
    print(f"{status} {fname}: p段={n_ps} 标注={len(secs)}")
if not ok:
    print("!! 有页数不匹配，终止")
    sys.exit(1)

out = Path("notes_recht/staat_sec_map.json")
out.write_text(json.dumps(MAP, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"写入 {out}（{sum(len(v) for v in MAP.values())} 段）")

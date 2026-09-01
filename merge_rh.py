# -*- coding: utf-8 -*-
"""合并子代理产出的阅读辅助（_tmp/ch{N}_rh.json）进 notes_pheno/reading_help.json，并硬校验：
① de 分块逐字命中对应段落（去空白归一）② first/last 必备 ③ words 上限 6
④ words 必须是单词/短词组（de 空格>3 或长度>40 报错——拦截句子型障碍词，2026-08-27 定型）
⑤ id 存在于未引段。
用法：python merge_rh.py
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
TMP = ROOT / "_tmp"
RH = ROOT / "notes_pheno" / "reading_help.json"

import build_pheno_ch123 as b  # noqa: E402


def norm_de(s: str) -> str:
    return re.sub(r"\s+", "", s).rstrip(".,;:–—-")


def main():
    target = json.loads(RH.read_text(encoding="utf-8")) if RH.exists() else {"updated": "2026-08-26",
        "note": "未引段阅读辅助：只在未被引用的原文段显示。首句/末句/中段难句按德语语序硬译分块；障碍词=非术语阅读障碍词。",
        "paragraphs": {}}
    errors = 0
    merged = 0
    for f in sorted(TMP.glob("ch*_rh.json")):
        data = json.loads(f.read_text(encoding="utf-8-sig"))
        paras = data.get("paragraphs", {})
        ch = f.name.split("_")[0][2:]
        base = re.match(r"\d+", ch).group(0)
        # 取该章原文段文本（归一，供校验）
        uncited = json.loads((TMP / f"ch{base}_uncited.json").read_text(encoding="utf-8"))
        text_by_id = {u["id"]: re.sub(r"\s+", "", u["text"]) for u in uncited}
        for pid, entry in paras.items():
            if pid not in text_by_id:
                print(f"  ✗ {f.name}: {pid} 不在未引段清单")
                errors += 1
                continue
            t = text_by_id[pid]
            for key in ("first", "middle", "last"):
                for c in entry.get(key, []):
                    de = c.get("de", "")
                    if not de or norm_de(de) not in t:
                        print(f"  ✗ {f.name} {pid}.{key}: de 未命中原文 → {de[:40]!r}")
                        errors += 1
            w = entry.get("words", [])
            if len(w) > 6:
                print(f"  ✗ {f.name} {pid}: words {len(w)}>6")
                errors += 1
            for wi, wd in enumerate(w):
                de = wd.get("de", "")
                # 障碍词必须是单词/短词组：句子型（>3 空格）或超长（>40 字符）视为错误数据
                if de.count(" ") > 3 or len(de) > 40:
                    print(f"  ✗ {f.name} {pid}.words[{wi}]: de 句子型/超长 → {de[:50]!r}")
                    errors += 1
                if not wd.get("zh"):
                    print(f"  ✗ {f.name} {pid}.words[{wi}]: zh 缺失")
                    errors += 1
            if not entry.get("first") or not entry.get("last"):
                print(f"  ✗ {f.name} {pid}: first/last 缺失")
                errors += 1
            target["paragraphs"][pid] = entry
            merged += 1
    if errors:
        print(f"校验失败：{errors} 处，未写盘")
        sys.exit(1)
    RH.write_text(json.dumps(target, ensure_ascii=False, indent=1),
                  encoding="utf-8", newline="\n")
    print(f"合并 {merged} 条，校验全过 -> notes_pheno/reading_help.json（共 {len(target['paragraphs'])} 段）")


if __name__ == "__main__":
    main()

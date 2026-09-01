# -*- coding: utf-8 -*-
import json, sys, re, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
d = json.load(open(r'原文/黑格尔/Enzyklopädie_Logik/extracted/enzyklopaedie_logik_index.json', encoding='utf-8'))
sec = {}
for e in d:
    cur = None
    for it in e['items']:
        if it['type'] in ('h4', 'h5'):
            m = re.match(r'§\s*(\d+)', it['text'])
            if m:
                cur = int(m.group(1))
        elif it['type'] == 'p' and cur:
            sec.setdefault(cur, []).append(it['text'])
for s in [84, 85, 86, 87, 160, 161, 162]:
    ps = sec.get(s, [])
    print(f'§{s}: {len(ps)} 段 | 首: {ps[0][:70] if ps else "无"}')
    if len(ps) > 1:
        print(f'      末: {ps[-1][:70]}')
# 检查 Am. / Anm. / A. 标记
print('--- Am./Anm. 标记 ---')
for s in [84, 85, 86, 87, 160, 161, 162]:
    for i, t in enumerate(sec.get(s, [])):
        m = re.search(r'\b(Amm?\.|Anm\.|A\.)\s', t)
        if m:
            print(f'§{s} 段{i}: {m.group(0)!r} | {t[:60]}')
# 检查 §86 附释常见句式（Zusatz 附释由 Hotho 编）是否在
print('--- Zusatz 搜索 ---')
for s in [86, 87, 160]:
    for i, t in enumerate(sec.get(s, [])):
        if 'Zusatz' in t:
            print(f'§{s} 段{i}: {t[:60]}')

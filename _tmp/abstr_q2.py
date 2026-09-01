# -*- coding: utf-8 -*-
import json, sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
d = json.load(open(r'原文/黑格尔/Grundlinien_der_Philosophie_des_Rechts/extracted/Grundlinien_der_Philosophie_des_Rechts_index.json', encoding='utf-8'))
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
for s in [66, 70, 74, 83, 86, 88, 95, 96, 102, 103, 104]:
    ps = sec.get(s, [])
    print(f'===== §{s} ({len(ps)}段) =====')
    for i, t in enumerate(ps):
        print(f'[段{i}] {t[:230]}')
    print()

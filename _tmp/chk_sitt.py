# -*- coding: utf-8 -*-
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
p = r'notes_recht/sittlichkeit.json'
d = json.load(open(p, encoding='utf-8'))
b = d['gestalten'][0]['bewegung']
print('当前环节数:', len(b))
for i, item in enumerate(b):
    print(f'  {i}: {item[0][:40]}')

"""app 템플릿(src/app.html)과 데이터(data/)를 합쳐 index.html 을 만든다.
사용법:  python build.py
"""
import glob, json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
HEAD = ('<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
        'body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n</head>\n<body>\n')
TAIL = '\n</body>\n</html>\n'

days = []
for f in sorted(glob.glob(os.path.join(ROOT, 'data', 'b?.txt'))):
    cur = None
    for line in open(f, encoding='utf8'):
        line = line.rstrip('\n')
        if not line:
            continue
        if line.startswith('## '):
            t, e = line[3:].split('|')
            cur = {'t': t, 'e': e, 'p': []}
            days.append(cur)
        else:
            parts = line.split('|')
            assert len(parts) == 4, line
            cur['p'].append(parts)
assert all(len(d['p']) == 5 for d in days), '하루는 반드시 5쌍이어야 합니다'

hg = {}
for tok in open(os.path.join(ROOT, 'data', 'hangul.txt'), encoding='utf8').read().split():
    k, v = tok.split('=')
    hg[k] = v

src = open(os.path.join(ROOT, 'src', 'app.html'), encoding='utf8').read()
out = src.replace('/*DATA*/', 'var DATA=' + json.dumps(days, ensure_ascii=False, separators=(',', ':')) + ';')
out = out.replace('/*HG*/', 'var HG=' + json.dumps(hg, ensure_ascii=False, separators=(',', ':')) + ';')
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf8').write(HEAD + out + TAIL)
print('index.html 생성:', len(days), '일치')

from pathlib import Path
import re, subprocess
ROOT=Path(__file__).resolve().parents[1]
ITEMS=[1,2,3,4,5,6,7,8,9,10,12,13,14,15,17,18,19,24,25,26,27,28,29,30,31,32,35,37,41,43,44,47,48,50,51,55,56,57,58,59,60,61,62,63]
idx=(ROOT/'past-questions/r08/index.html').read_text(encoding='utf-8')
SLUGS={}
for i in ITEMS:
    m=re.search(rf'<a id="item-{i}"[^>]+href="../../topics/([^/]+)/"',idx)
    if not m: raise RuntimeError(f'R8 slug missing item {i}')
    SLUGS[i]=m.group(1)
for i,slug in SLUGS.items():
    p=ROOT/'topics'/slug/'index.html'
    s=p.read_text(encoding='utf-8')
    if '参照した公開問題' not in s: raise RuntimeError(f'reference section missing item {i}')
    head,tail=s.split('参照した公開問題',1)
    anchors=list(re.finditer(r'<a\b[^>]*>\s*IPA公式ITパスポート試験\s*過去問題(?:（令和\d年度）)?\s*</a>',tail,re.S))
    if len(anchors)<2: raise RuntimeError(f'expected two IPA links item {i}, got {len(anchors)}')
    a2=anchors[1]
    before=tail[:a2.start()]
    paras=list(re.finditer(r'<p[^>]*>(.*?)</p>',before,re.S))
    target=None
    for m in reversed(paras):
        txt=re.sub(r'<[^>]+>','',m.group(1))
        if '問' in txt:
            target=m; break
    if target is None: raise RuntimeError(f'R8 question paragraph missing item {i}')
    txt=re.sub(r'<[^>]+>','',target.group(1))
    if '令和8年度' not in txt:
        full=target.group(0)
        fixed=re.sub(r'^(<p[^>]*>)\s*',r'\1令和8年度　',full,count=1)
        tail=tail[:target.start()]+fixed+tail[target.end():]
        # recompute second anchor after length change
        anchors=list(re.finditer(r'<a\b[^>]*>\s*IPA公式ITパスポート試験\s*過去問題(?:（令和\d年度）)?\s*</a>',tail,re.S))
        a2=anchors[1]
    fulla=a2.group(0)
    fulla=re.sub(r'IPA公式ITパスポート試験\s*過去問題(?:（令和\d年度）)?', 'IPA公式ITパスポート試験 過去問題（令和8年度）', fulla, count=1)
    tail=tail[:a2.start()]+fulla+tail[a2.end():]
    s=head+'参照した公開問題'+tail
    s=s.replace('ITパスポート試験シラバスのシラバス項目','ITパスポート試験シラバス項目')
    p.write_text(s,encoding='utf-8')
subprocess.run(['git','add','topics'],cwd=ROOT,check=True)
subprocess.run(['git','commit','-m','Fix year labels in integrated question references'],cwd=ROOT,check=True)
subprocess.run(['git','push','origin','main'],cwd=ROOT,check=True)
for i,slug in SLUGS.items():
    s=(ROOT/'topics'/slug/'index.html').read_text(encoding='utf-8')
    tail=s.split('参照した公開問題',1)[1]
    if '令和7年度　' not in tail or '令和8年度　' not in tail or '過去問題（令和8年度）' not in tail:
        raise RuntimeError(f'year-group verification failed item {i}')
subprocess.run(['git','rm','.github/workflows/fix-r07-r08-reference-labels.yml','scripts/fix_r07_r08_reference_labels.py'],cwd=ROOT,check=True)
subprocess.run(['git','commit','-m','Remove one-shot reference label fix'],cwd=ROOT,check=True)
subprocess.run(['git','push','origin','main'],cwd=ROOT,check=True)

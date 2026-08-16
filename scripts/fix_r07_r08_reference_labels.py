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
IPA='https://www3.jitec.ipa.go.jp/JitesCbt/html/openinfo/questions.html'
for i,slug in SLUGS.items():
    p=ROOT/'topics'/slug/'index.html'
    s=p.read_text(encoding='utf-8')
    if '参照した公開問題' not in s: raise RuntimeError(f'reference section missing item {i}')
    head,tail=s.split('参照した公開問題',1)
    paras=list(re.finditer(r'<p[^>]*>(.*?)</p>',tail,re.S))
    qparas=[]
    for m in paras:
        txt=re.sub(r'<[^>]+>','',m.group(1)).strip()
        if '問' in txt: qparas.append((m,txt))
    r8=None
    for m,txt in qparas:
        if '令和7年度' not in txt:
            r8=(m,txt); break
    if r8 is None: raise RuntimeError(f'R8 question paragraph missing item {i}')
    m,txt=r8
    if '令和8年度' not in txt:
        full=m.group(0)
        fixed=re.sub(r'^(<p[^>]*>)\s*',r'\1令和8年度　',full,count=1)
        tail=tail[:m.start()]+fixed+tail[m.end():]
    # Find the R8 question paragraph again after possible length change.
    paras=list(re.finditer(r'<p[^>]*>(.*?)</p>',tail,re.S))
    r8m=None
    for pm in paras:
        txt=re.sub(r'<[^>]+>','',pm.group(1)).strip()
        if txt.startswith('令和8年度') and '問' in txt:
            r8m=pm; break
    if r8m is None: raise RuntimeError(f'R8 label insertion failed item {i}')
    # From the R8 question line to return links, reuse any existing non-R7 IPA link; otherwise add one.
    stop=tail.find('return-links',r8m.end())
    if stop<0: stop=len(tail)
    region=tail[r8m.end():stop]
    links=list(re.finditer(r'<a\b[^>]*>.*?</a>',region,re.S))
    chosen=None
    for am in links:
        plain=re.sub(r'<[^>]+>',' ',am.group(0))
        if 'IPA公式' in plain and '過去問題' in plain and '令和7年度' not in plain:
            chosen=am; break
    if chosen:
        full=chosen.group(0)
        full=re.sub(r'IPA公式ITパスポート試験\s*過去問題(?:（令和\d年度）)?','IPA公式ITパスポート試験 過去問題（令和8年度）',full,count=1)
        region=region[:chosen.start()]+full+region[chosen.end():]
        tail=tail[:r8m.end()]+region+tail[stop:]
    else:
        link=f'<p><a href="{IPA}" target="_blank" rel="noopener noreferrer">IPA公式ITパスポート試験 過去問題（令和8年度）</a></p>'
        tail=tail[:r8m.end()]+link+tail[r8m.end():]
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

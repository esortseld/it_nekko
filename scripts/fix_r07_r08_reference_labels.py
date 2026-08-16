from pathlib import Path
import re, subprocess
ROOT=Path(__file__).resolve().parents[1]
ITEMS=[1,2,3,4,5,6,7,8,9,10,12,13,14,15,17,18,19,24,25,26,27,28,29,30,31,32,35,37,41,43,44,47,48,50,51,55,56,57,58,59,60,61,62,63]
SLUGS={}
idx=(ROOT/'past-questions/r08/index.html').read_text(encoding='utf-8')
for i in ITEMS:
    m=re.search(rf'<a id="item-{i}"[^>]+href="../../topics/([^/]+)/"',idx)
    if not m: raise RuntimeError(f'R8 slug missing item {i}')
    SLUGS[i]=m.group(1)
for i in ITEMS:
    p=ROOT/'topics'/SLUGS[i]/'index.html'
    s=p.read_text(encoding='utf-8')
    # Restore the year label on the question line immediately preceding the R8 official link.
    pat=r'<p>(?!令和\d年度)([^<]*問[^<]*)</p>(?=<p><a[^>]*>IPA公式ITパスポート試験 過去問題（令和8年度）</a></p>)'
    s,n=re.subn(pat,lambda m:'<p>令和8年度　'+m.group(1).lstrip('　 ')+'</p>',s,count=1)
    if n!=1 and '令和8年度　問' not in s:
        raise RuntimeError(f'R8 reference label not found item {i}')
    s=s.replace('ITパスポート試験シラバスのシラバス項目','ITパスポート試験シラバス項目')
    p.write_text(s,encoding='utf-8')
subprocess.run(['git','add','topics'],cwd=ROOT,check=True)
subprocess.run(['git','commit','-m','Fix year labels in integrated question references'],cwd=ROOT,check=True)
subprocess.run(['git','push','origin','main'],cwd=ROOT,check=True)
# verify from working tree after push
for i in ITEMS:
    s=(ROOT/'topics'/SLUGS[i]/'index.html').read_text(encoding='utf-8')
    if '令和7年度　問' not in s or '令和8年度　問' not in s:
        raise RuntimeError(f'year-group verification failed item {i}')
# remove one-shot automation
subprocess.run(['git','rm','.github/workflows/fix-r07-r08-reference-labels.yml','scripts/fix_r07_r08_reference_labels.py'],cwd=ROOT,check=True)
subprocess.run(['git','commit','-m','Remove one-shot reference label fix'],cwd=ROOT,check=True)
subprocess.run(['git','push','origin','main'],cwd=ROOT,check=True)

from pathlib import Path
import re, subprocess
ROOT=Path(__file__).resolve().parents[1]
ITEMS=[1,2,3,4,5,6,7,8,9,10,12,13,14,15,17,18,19,24,25,26,27,28,29,30,31,32,35,37,41,43,44,47,48,50,51,55,56,57,58,59,60,61,62,63]
idx=(ROOT/'past-questions/r08/index.html').read_text(encoding='utf-8')
DATA={}
for i in ITEMS:
    m=re.search(rf'<a id="item-{i}"[^>]+href="../../topics/([^/]+)/"[^>]*>.*?<p class="item-questions">(問[^<]+)</p>',idx,re.S)
    if not m: raise RuntimeError(f'R8 data missing item {i}')
    DATA[i]=(m.group(1),m.group(2))
for i,(slug,qtext) in DATA.items():
    p=ROOT/'topics'/slug/'index.html'
    s=p.read_text(encoding='utf-8')
    if '参照した公開問題' not in s: raise RuntimeError(f'reference section missing item {i}')
    head,tail=s.split('参照した公開問題',1)
    wanted='令和8年度　'+qtext
    if wanted not in tail:
        if qtext not in tail: raise RuntimeError(f'R8 question text missing item {i}: {qtext}')
        tail=tail.replace(qtext,wanted,1)
    s=head+'参照した公開問題'+tail
    s=s.replace('ITパスポート試験シラバスのシラバス項目','ITパスポート試験シラバス項目')
    p.write_text(s,encoding='utf-8')
subprocess.run(['git','add','topics'],cwd=ROOT,check=True)
subprocess.run(['git','commit','-m','Fix year labels in integrated question references'],cwd=ROOT,check=True)
subprocess.run(['git','push','origin','main'],cwd=ROOT,check=True)
for i,(slug,qtext) in DATA.items():
    s=(ROOT/'topics'/slug/'index.html').read_text(encoding='utf-8')
    tail=s.split('参照した公開問題',1)[1]
    if '令和7年度　' not in tail or '令和8年度　'+qtext not in tail:
        raise RuntimeError(f'year-group verification failed item {i}')
subprocess.run(['git','rm','.github/workflows/fix-r07-r08-reference-labels.yml','scripts/fix_r07_r08_reference_labels.py'],cwd=ROOT,check=True)
subprocess.run(['git','commit','-m','Remove one-shot reference label fix'],cwd=ROOT,check=True)
subprocess.run(['git','push','origin','main'],cwd=ROOT,check=True)

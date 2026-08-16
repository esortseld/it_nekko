from pathlib import Path
import subprocess

P=Path('past-questions/r07/index.html')
items={
22:('r08-22-systemization-plan','システム化計画','問20'),
34:('r08-34-applied-mathematics','応用数学','問63・問85'),
40:('r08-40-processor','プロセッサ','問67'),
45:('r08-45-operating-system','オペレーティングシステム','問62'),
53:('r08-53-multimedia-applications','マルチメディア応用','問19'),
}
def run(*a): subprocess.run(a,check=True)
for i,(slug,title,qs) in items.items():
    run('git','pull','--ff-only','origin','main')
    s=P.read_text(encoding='utf-8')
    good=f'<a id="item-{i}" class="item-card item-card--ready" href="../../topics/{slug}/"><div class="item-card__top"><span class="item-no">項目{i}</span></div><h3>{title}</h3><p class="item-questions">{qs}</p></a>'
    bad=f'<a id="item-{i}" class="item-card item-card--ready" href="../../topics/{slug}/"><div class="item-card__top"><span class="item-no">項目{i}</span></a>\n<h3>{title}</h3><p class="item-questions">{qs}</p></div>'
    if good in s:
        continue
    if bad not in s:
        raise RuntimeError(f'item {i}: malformed card pattern not found')
    P.write_text(s.replace(bad,good,1),encoding='utf-8')
    run('git','add',str(P))
    run('git','commit','-m',f'Fix R07 item {i} full-card link')
    run('git','push','origin','main')
# final check
s=P.read_text(encoding='utf-8')
for i,(slug,title,qs) in items.items():
    assert f'<a id="item-{i}" class="item-card item-card--ready" href="../../topics/{slug}/"><div class="item-card__top"><span class="item-no">項目{i}</span></div><h3>{title}</h3><p class="item-questions">{qs}</p></a>' in s
print('fixed')

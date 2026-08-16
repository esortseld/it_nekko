from pathlib import Path
import re, subprocess

ROOT=Path('.')
INDEX=ROOT/'past-questions/r07/index.html'
IPA='https://www3.jitec.ipa.go.jp/JitesCbt/html/openinfo/questions.html'

CSS='''
  <style>
    .topic-page{--accent:#6f665b;--soft:#f6f2eb;--line:var(--color-border,#d9d3c8)}
    .topic-page .breadcrumbs{display:flex;flex-wrap:wrap;gap:.35rem;margin:0 0 1.1rem;font-size:.82rem;color:var(--text-sub,#675f55)}
    .topic-page .breadcrumbs a{color:inherit;text-decoration:none}
    .topic-page .box{margin:0 0 1rem;padding:1.15rem;border:1px solid var(--line);border-radius:18px;background:#fff}
    .topic-page .box h2{margin:0 0 .8rem;font-size:1.15rem}
    .topic-page .map{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.7rem}
    .topic-page .map.two{grid-template-columns:repeat(2,minmax(0,1fr))}
    .topic-page .mini{min-width:0;padding:.9rem;border-radius:13px;background:var(--soft)}
    .topic-page .mini strong{display:block;margin-bottom:.25rem}
    .topic-page .compare{display:grid;grid-template-columns:minmax(9rem,.72fr) minmax(0,1.4fr);gap:1px;border:1px solid var(--line);border-radius:12px;overflow:hidden;background:var(--line)}
    .topic-page .compare div{padding:.72rem .8rem;background:#fff}
    .topic-page .compare .head{font-weight:700;background:var(--soft)}
    .topic-page .judge{padding:.95rem 1rem;border-left:4px solid var(--accent);border-radius:0 12px 12px 0;background:var(--soft)}
    .topic-page .refs{margin-top:1.5rem;padding-top:1rem;border-top:1px solid var(--line)}
    .topic-page .refs p{margin:.35rem 0}
    .topic-page .return-links{display:flex;flex-wrap:wrap;gap:.55rem;margin-top:1rem}
    .topic-page .return-links a{padding:.55rem .75rem;border:1px solid var(--line);border-radius:999px;background:#fff;color:inherit;text-decoration:none;font-size:.86rem}
    .topic-page code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
    @media(max-width:720px){.topic-page .map,.topic-page .map.two,.topic-page .compare{grid-template-columns:1fr}.topic-page .compare .head:nth-child(2){display:none}.topic-page .return-links{display:grid;grid-template-columns:1fr}.topic-page .return-links a{text-align:center}}
  </style>'''

def shell(*args):
    subprocess.run(args,check=True)

def page(item,title,field,field_slug,slug,body,qs):
    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>項目{item} {title} | ITネッコ</title>
  <link rel="stylesheet" href="../../assets/style.css">{CSS}
</head>
<body class="topic-page">
<header class="site-header"><div class="container header-inner"><a class="brand" href="../../">ITネッコ</a><nav class="site-nav" aria-label="主要ページ"><a href="../../">トップ</a><a href="../../fields/">学習分野</a><a href="../../past-questions/">公開問題</a><a href="../../about/">このサイトについて</a></nav></div></header>
<main>
<section class="page-hero"><div class="container hero-inner"><p class="site-kicker">{field} / 項目{item}</p><h1>項目{item} {title}</h1></div></section>
<div class="container page-flow">
<div class="breadcrumbs"><a href="../../">トップ</a><span>›</span><a href="../../fields/{field_slug}/">{field}</a><span>›</span><span>項目{item} {title}</span></div>
<article>{body}
<section class="refs"><h2>参照した公開問題</h2><p>令和7年度　{qs}</p><p><a href="{IPA}" target="_blank" rel="noopener noreferrer">IPA公式ITパスポート試験 過去問題（令和7年度）</a></p><div class="return-links"><a href="../../past-questions/">公開問題一覧へ戻る</a><a href="../../fields/{field_slug}/">{field}へ戻る</a></div></section>
</article></div></main>
<footer class="site-footer"><div class="container"><p>ITネッコ / のらネコ学習室</p></div></footer>
</body></html>'''

PAGES={
22: dict(title='システム化計画',field='ストラテジ系',field_slug='strategy',slug='r08-22-systemization-plan',qs='問20',body='''
<section class="box"><h2>項目全体の学習地図</h2><div class="map"><div class="mini"><strong>対象業務を把握する</strong>何をシステム化するのか、現状と課題を整理する。</div><div class="mini"><strong>全体方針を決める</strong>情報システム戦略に沿って構想・基本方針を立てる。</div><div class="mini"><strong>実現性を見積もる</strong>開発順序、概算コスト、効果、体制、リスクを全体で見る。</div></div></section>
<section class="box"><h2>企画段階で集める情報の粒度を見る</h2><div class="map"><div class="mini"><strong>場面</strong>企画プロセスでシステム化構想を立案するため、ベンダー企業など外部から情報を集める。</div><div class="mini"><strong>判断すること</strong>まだ個別開発や発注の詳細を決める段階なのか、それとも業務分野の技術動向を把握して構想を作る段階なのか。</div><div class="mini"><strong>決定的な条件</strong>「システム化構想の立案時」という時点。必要なのは、構想の方向を決めるための外部環境・技術動向の情報である。</div></div></section>
<section class="box"><h2>計画と後続工程を分ける</h2><div class="compare"><div class="head">情報</div><div class="head">位置付け</div><div>業務分野の情報技術動向</div><div>システム化の方向・可能性を考える企画段階で使う。</div><div>開発コストの具体的見積り</div><div>対象や方式が具体化した後の見積り・調達判断に近い。</div><div>発注企業の役割</div><div>契約・開発体制を具体化する段階で確認する。</div><div>ベンダー技術者の資格</div><div>要員・調達先を具体的に評価する段階で扱う。</div></div></section>
<section class="box"><h2>必要な用語・概念</h2><div class="compare"><div class="head">概念</div><div class="head">見ること</div><div>システム化構想</div><div>何を、なぜ、どの方向でシステム化するかの全体像。</div><div>システム化基本方針</div><div>構想を実現するための基本的な方針。</div><div>費用対効果</div><div>投入する費用と期待する効果の釣合い。</div><div>適用範囲</div><div>どこまでをシステム化対象とするか。</div></div></section>
<section class="box"><h2>項目全体の判断の地図</h2><div class="judge"><strong>まず「今はどの段階か」を決める。</strong><br>企画段階なら全体像・方向・技術動向・概算を見る。対象や方式が固まってから、具体的な見積り、要員、契約、発注条件へ進む。</div></section>'''),
34: dict(title='応用数学',field='テクノロジ系',field_slug='technology',slug='r08-34-applied-mathematics',qs='問63・問85',body='''
<section class="box"><h2>項目全体の学習地図</h2><div class="map two"><div class="mini"><strong>データの尺度を見分ける</strong>数値や分類が「差」「順序」「比」をどこまで意味するかを見る。</div><div class="mini"><strong>割合の変化を繰り返す</strong>毎回同じ割合で増減するときは、加減ではなく倍率の積で追う。</div></div></section>
<section class="box"><h2>データがどこまで数として扱えるかを見る</h2><div class="compare"><div class="head">尺度</div><div class="head">意味</div><div>名義尺度</div><div>分類するためのラベル。大小や差に意味はない。</div><div>順序尺度</div><div>順番に意味があるが、隣同士の差が等しいとは限らない。</div><div>間隔尺度</div><div>値の差に意味がある。基準の0が「量が全くない」を示すとは限らない。</div><div>比例尺度</div><div>差だけでなく比にも意味があり、0が量の不存在を表す。</div></div><div class="judge" style="margin-top:.8rem"><strong>判断順序：</strong>分類だけか → 順序があるか → 差が等間隔か → 2倍・半分という比まで意味があるか。</div></section>
<section class="box"><h2>同じ割合の低下を繰り返して追う</h2><div class="map"><div class="mini"><strong>場面</strong>学習を1回行うたびに、誤り率が直前の95%になる。</div><div class="mini"><strong>判断すること</strong>「5ポイントずつ引く」のではなく、「前回値に0.95を掛ける」変化として扱う。</div><div class="mini"><strong>決定的な条件</strong>変化率が毎回「直前の値」に掛かるので、複利と同じ形の指数的変化になる。</div></div><div class="judge" style="margin-top:.8rem"><code>n回後の値 = 初期値 × 0.95^n</code><br>しきい値を下回る最小のnを順に確認する。</div></section>
<section class="box"><h2>必要な用語・概念</h2><div class="compare"><div class="head">概念</div><div class="head">見ること</div><div>代表値・分散</div><div>データの中心とばらつきを表す。</div><div>相関</div><div>二つの変数がどの程度一緒に変化するかを見る。</div><div>確率</div><div>起こりやすさを数で扱う。</div><div>指数的変化</div><div>一定量ではなく一定割合で増減を繰り返す変化。</div></div></section>
<section class="box"><h2>項目全体の判断の地図</h2><div class="judge"><strong>数値が出たら、まず「何を数として扱えるのか」を確認する。</strong><br>尺度の問題では差・比の意味を、割合の問題では基準が初期値か直前値かを確認する。</div></section>'''),
40: dict(title='プロセッサ',field='テクノロジ系',field_slug='technology',slug='r08-40-processor',qs='問67',body='''
<section class="box"><h2>項目全体の学習地図</h2><div class="map"><div class="mini"><strong>コンピュータの基本機能</strong>演算・制御・記憶・入力・出力が連携する。</div><div class="mini"><strong>CPU</strong>命令を順に処理し、コンピュータ全体の演算・制御を担う中心的なプロセッサ。</div><div class="mini"><strong>GPU</strong>多数の演算を並列に進めることに強く、画像処理など大量の同種計算を高速化する。</div></div></section>
<section class="box"><h2>処理内容から向いているプロセッサを考える</h2><div class="map"><div class="mini"><strong>場面</strong>3次元画像の描画を高速化し、動画の表示を滑らかにする。</div><div class="mini"><strong>判断すること</strong>処理が、複雑な命令を順に処理する仕事か、大量の同種計算を同時並行で処理する仕事か。</div><div class="mini"><strong>決定的な条件</strong>画像の画素や頂点など、多数の要素へ似た計算を繰り返す。</div></div></section>
<section class="box"><h2>CPUとGPUの役割を分ける</h2><div class="compare"><div class="head">プロセッサ</div><div class="head">得意な処理</div><div>CPU</div><div>OSやアプリケーションの命令を制御しながら幅広く処理する。逐次処理や分岐の多い処理にも向く。</div><div>GPU</div><div>画像描画など、同種の数値演算を大量に並列実行する処理に向く。</div><div>GPGPU</div><div>GPUの並列演算能力を、画像以外の汎用計算にも利用する考え方。</div></div></section>
<section class="box"><h2>必要な用語・概念</h2><div class="compare"><div class="head">用語</div><div class="head">意味</div><div>CPU</div><div>中央処理装置。演算・制御の中心。</div><div>マルチコア</div><div>一つのプロセッサ内に複数の処理コアを持つ。</div><div>クロック周波数</div><div>処理タイミングの基準となる信号の周波数。性能はこれだけでは決まらない。</div><div>GPU</div><div>画像処理を中心に発達した並列計算向けプロセッサ。</div></div></section>
<section class="box"><h2>項目全体の判断の地図</h2><div class="judge"><strong>機器名ではなく、処理の形を見る。</strong><br>制御や分岐を含む幅広い処理か、大量の同種計算を並列に処理するのかで、適したプロセッサの役割を判断する。</div></section>'''),
45: dict(title='オペレーティングシステム',field='テクノロジ系',field_slug='technology',slug='r08-45-operating-system',qs='問62',body='''
<section class="box"><h2>項目全体の学習地図</h2><div class="map"><div class="mini"><strong>利用者・アプリと機械の間を管理する</strong>OSはハードウェア資源をアプリケーションへ使いやすい形で提供する。</div><div class="mini"><strong>資源を管理する</strong>ユーザー、ファイル、入出力、CPU、メモリなどを管理する。</div><div class="mini"><strong>物理的な制約を抽象化する</strong>アプリから見える資源と、実際のハードウェア構成を切り分ける。</div></div></section>
<section class="box"><h2>仮想記憶で「見える記憶空間」と「実物」を分ける</h2><div class="map"><div class="mini"><strong>場面</strong>プログラムを実行するとき、主記憶の実容量だけに縛られずにアドレス空間を利用したい。</div><div class="mini"><strong>判断すること</strong>プログラムが扱う論理的なアドレス空間と、実際の主記憶上の物理的な配置を同じものとして考えていないか。</div><div class="mini"><strong>決定的な条件</strong>OSが主記憶と補助記憶を使い分け、必要な部分を入れ替えながら実行する。</div></div></section>
<section class="box"><h2>三つの層を分ける</h2><div class="compare"><div class="head">層</div><div class="head">役割</div><div>論理アドレス空間</div><div>プログラムから見える連続した記憶空間。</div><div>物理メモリ</div><div>実際に搭載されている主記憶装置上の領域。</div><div>補助記憶</div><div>主記憶に載っていないページなどを一時的に退避するためにも使われる。</div></div></section>
<section class="box"><h2>必要な用語・概念</h2><div class="compare"><div class="head">用語</div><div class="head">意味</div><div>仮想記憶</div><div>物理メモリの構成を直接意識せず、より大きな論理アドレス空間を利用できるようにする仕組み。</div><div>ページング</div><div>記憶領域を一定単位に分け、主記憶と補助記憶の間で入れ替える方式。</div><div>資源管理</div><div>CPU、メモリ、入出力装置などをOSが配分・制御すること。</div><div>ユーザー管理</div><div>アカウントやアクセス権を管理する機能。</div></div></section>
<section class="box"><h2>項目全体の判断の地図</h2><div class="judge"><strong>OSの機能は「何を抽象化し、何を管理しているか」で見る。</strong><br>仮想記憶では、プログラムから見える論理空間と、実際の物理メモリを分けて考える。</div></section>'''),
53: dict(title='マルチメディア応用',field='テクノロジ系',field_slug='technology',slug='r08-53-multimedia-applications',qs='問19',body='''
<section class="box"><h2>項目全体の学習地図</h2><div class="map"><div class="mini"><strong>現実を置き換える</strong>仮想空間を中心に体験するVR。</div><div class="mini"><strong>現実へ情報を重ねる</strong>実際の風景や物体に情報を付加するAR。</div><div class="mini"><strong>現実と仮想を相互作用させる</strong>現実空間とデジタル情報をより密接に融合するMR。</div></div></section>
<section class="box"><h2>何が画面の土台になっているかを見る</h2><div class="map"><div class="mini"><strong>場面</strong>ゴーグルやスマートフォンなどで、現実にはない映像や情報を体験する。</div><div class="mini"><strong>判断すること</strong>見えている世界の土台が仮想空間なのか、現実の映像・風景なのか。</div><div class="mini"><strong>決定的な条件</strong>仮想空間に入り込むのか、現実の風景へCGや説明情報を重ねるのか。</div></div></section>
<section class="box"><h2>VR・AR・MRを関係で分ける</h2><div class="compare"><div class="head">技術</div><div class="head">現実と仮想の関係</div><div>VR</div><div>仮想空間を主な体験環境として提示する。訓練、シミュレーター、ゲームなどで利用される。</div><div>AR</div><div>現実の映像・風景を土台に、CG、説明、案内などのデジタル情報を重ねる。</div><div>MR</div><div>現実空間と仮想オブジェクトを融合し、位置関係を保って相互作用できるようにする。</div></div></section>
<section class="box"><h2>必要な用語・概念</h2><div class="compare"><div class="head">用語</div><div class="head">見ること</div><div>CG</div><div>コンピュータで画像・映像を生成・加工する技術。</div><div>3D</div><div>奥行きを含む三次元情報として形状や空間を表現する。</div><div>シミュレーター</div><div>現実の状況や操作を仮想的に再現する。</div><div>メタバース</div><div>継続的に利用される仮想空間・サービスの概念。</div></div></section>
<section class="box"><h2>項目全体の判断の地図</h2><div class="judge"><strong>装置名ではなく、体験の土台を見る。</strong><br>現実を置き換えるならVR、現実へ情報を重ねるならAR、現実と仮想を空間として融合させるならMRとして整理する。</div></section>''')
}

for item in [22,34,40,45,53]:
    shell('git','pull','--ff-only','origin','main')
    d=PAGES[item]
    idx=INDEX.read_text(encoding='utf-8')
    # must still be a real R07 item and pending before processing
    card_re=re.compile(rf'<div id="item-{item}" class="item-card item-card--pending">.*?</div>\n?', re.S)
    m=card_re.search(idx)
    if not m:
        # already linked is acceptable only if it points to intended page
        if f'id="item-{item}"' in idx and f'../../topics/{d["slug"]}/' in idx:
            continue
        raise RuntimeError(f'R07 item {item}: pending card not found')
    page_path=ROOT/'topics'/d['slug']/'index.html'
    if page_path.exists():
        raise RuntimeError(f'R07 item {item}: target page already exists')
    page_path.parent.mkdir(parents=True,exist_ok=True)
    page_path.write_text(page(item,d['title'],d['field'],d['field_slug'],d['slug'],d['body'],d['qs']),encoding='utf-8')
    old=m.group(0).rstrip('\n')
    # preserve exact inner card content and switch container to anchor/ready
    inner=re.sub(r'^<div ([^>]+)>','',old,count=1)
    inner=re.sub(r'</div>$','',inner,count=1)
    new=f'<a id="item-{item}" class="item-card item-card--ready" href="../../topics/{d["slug"]}/">{inner}</a>'
    idx=idx[:m.start()]+new+'\n'+idx[m.end():]
    INDEX.write_text(idx,encoding='utf-8')
    shell('git','add',str(page_path),str(INDEX))
    shell('git','commit','-m',f'Create shared topic page for R07 item {item}')
    shell('git','push','origin','main')

# final integrity checks
idx=INDEX.read_text(encoding='utf-8')
for item,d in PAGES.items():
    assert f'id="item-{item}" class="item-card item-card--ready" href="../../topics/{d["slug"]}/"' in idx
    html=(ROOT/'topics'/d['slug']/'index.html').read_text(encoding='utf-8')
    assert f'令和7年度　{d["qs"]}' in html
    assert '参照した公開問題' in html
print('created:', ','.join(map(str,PAGES)))

from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / 'past-questions/r07/index.html'
IPA = 'https://www3.jitec.ipa.go.jp/JitesCbt/html/openinfo/questions.html'

DATA = {
1: ('topics/r08-01-management-organization/index.html','r08-01-management-organization','問3・問15・問29',[
('企業が目指す方向と存在意義を分ける','企業理念を整理するとき、ミッション・ビジョン・バリューを混同しやすい。','存在意義、将来像、行動基準のどれを表しているか。','MVV、企業理念、ビジョン','ミッションは存在意義、ビジョンは将来のありたい姿、バリューは判断・行動の基準として捉える。'),
('社会全体でデータを活用する枠組みを見る','行政や企業がデータを活用し、社会課題の解決やサービス改善を進める。','誰がデータ活用の主体となり、どの範囲で連携する仕組みか。','官民データ活用、データ駆動型社会','IT活用は一企業の効率化だけでなく、行政・企業・社会全体のデータ活用にも広がる。')]),
2: ('topics/r08-02-business-analysis-data-utilization/index.html','r08-02-business-analysis-data-utilization','問8',[
('分析前にデータの偏りを点検する','AIやデータ分析に使うデータを集めたが、元データに偏りや不備がある可能性がある。','分析手法の前に、データの目的適合性・欠損・偏り・作成過程を確認できているか。','データ品質、バイアス、前処理、アノテーション','分析結果の品質は、入力データの品質と収集・前処理の妥当性に大きく左右される。')]),
3: ('topics/r08-03-accounting-finance/index.html','r08-03-accounting-finance','問5・問26・問34',[
('売上と仕入れの差から利益を見る','商品の仕入価格や販売価格が変わり、利益への影響を判断する。','売上高だけでなく、売上原価や期首・期末在庫を含めて利益を捉えているか。','売上原価、棚卸資産、粗利益','利益を見るときは、売上高とその売上に対応する原価を対応させる。'),
('売上数量と固定費・変動費の関係を見る','販売数量を増やしたとき、利益がどのように変わるかを見積もる。','固定費と変動費を分け、損益分岐点を越える条件を確認する。','固定費、変動費、損益分岐点','売上の増加がそのまま利益になるわけではなく、固定費と変動費の構造で利益の増え方が決まる。')]),
4: ('topics/r08-04-intellectual-property-rights/index.html','r08-04-intellectual-property-rights','問12・問21・問30',[
('名称や表示を守る権利と著作物を守る権利を分ける','商品・サービスの名称やソフトウェアに関係する権利を確認する。','守ろうとしている対象が、標章なのか創作的表現なのか。','商標、サービスマーク、著作権','権利の種類は対象物で分ける。名称・標章を識別する仕組みと、創作物の表現を保護する仕組みは別である。'),
('プログラムのどこまでが著作権の対象かを見る','ソフトウェアに関する仕様、操作方法、プログラムそのものを比較する。','アイデアや手順そのものではなく、創作的に表現された著作物か。','プログラムの著作物、アイデアと表現','著作権は考え方そのものではなく、創作的な表現を保護する。')]),
5: ('topics/r08-05-security-related-laws/index.html','r08-05-security-related-laws','問6・問16',[
('電子メール送信で同意と表示義務を確認する','広告宣伝メールを送る。','受信者の同意、送信者情報、受信拒否の扱いなど法令上の条件を満たしているか。','特定電子メール法、オプトイン','広告メールは、内容だけでなく送信の同意や表示・停止手段など送信方法にも規制がある。'),
('他人の認証情報を使う行為を見る','他人のIDやパスワードを無断で使ってシステムへ接続する。','正当な権限を持つ本人の利用か、認証を突破・悪用したアクセスか。','不正アクセス禁止法、識別符号','実害が発生したかだけでなく、認証を不正に通過する行為自体が問題になる。')]),
6: ('topics/r08-06-labor-transaction-laws/index.html','r08-06-labor-transaction-laws','問1',[
('外部委託先への指示系統を見る','請負で外部会社へ業務を委託し、委託先の作業者が自社事業所で作業している。','作業者へ誰が具体的な指揮命令を行う契約なのか。','請負契約、労働者派遣、指揮命令','請負では成果や業務の完成を受託側が管理する。発注側が作業者へ直接指揮命令する形になると、契約類型との不整合が問題になる。')]),
7: ('topics/r08-07-laws-guidelines-information-ethics/index.html','r08-07-laws-guidelines-information-ethics','問23',[
('企業を監督する仕組みを見る','経営者だけに判断が集中しないよう、企業活動を監督する仕組みを整える。','誰が経営を監督し、権限と責任をどう分離するか。','コーポレートガバナンス、取締役会、執行と監督','ガバナンスは、経営判断を外部から批判することではなく、権限・監督・説明責任を制度として整えること。')]),
8: ('topics/r08-08-standardization-related/index.html','r08-08-standardization-related','問2',[
('対象分野に合う標準・ガイドラインを選ぶ','クラウドサービス利用時の情報セキュリティ管理を整える。','標準の番号だけでなく、対象が品質・環境・クラウドセキュリティなど何かを確認する。','ISO/IEC 27017、ISO/IEC 27000','標準は目的分野ごとに役割が異なる。クラウド固有のセキュリティ管理には、その分野を対象とするガイドラインを選ぶ。')]),
9: ('topics/r08-09-management-strategy-methods/index.html','r08-09-management-strategy-methods','問4',[
('自社資源が競争優位につながる条件を見る','自社の技術、人材、ブランドなどの経営資源を評価する。','価値、希少性、模倣困難性、組織として活用できるかを順に見る。','VRIO分析','経営資源は保有しているだけでは競争優位にならない。価値・希少性・模倣困難性と、それを生かす組織がそろうかを確認する。')]),
10: ('topics/r08-10-marketing/index.html','r08-10-marketing','問35',[
('市場を分け、狙う顧客を決め、位置付ける','新商品を誰にどう売るかを考える。','市場を分ける段階、対象を選ぶ段階、競合との違いを示す段階のどこか。','セグメンテーション、ターゲティング、ポジショニング','STPは「市場を分ける→対象を選ぶ→顧客から見た位置付けを決める」という別々の判断で構成される。')]),
12: ('topics/r08-12-management-systems/index.html','r08-12-management-systems','問31',[
('企業全体の資源を一体で管理する','販売・会計・在庫・人事など部門ごとの情報が分断されている。','部門ごとの個別最適ではなく、企業資源を統合して扱う仕組みか。','ERP、基幹業務、統合データ','ERPは、企業の主要な経営資源と基幹業務を全社横断で統合管理する。')]),
13: ('topics/r08-13-technology-development-strategy/index.html','r08-13-technology-development-strategy','問7・問9・問14',[
('実用化前に価値や実現性を確かめる','新しい技術やアイデアを本格導入する前に、小規模に試す。','確認したいのが技術的実現性なのか、事業価値なのか。','PoC、PoV、プロトタイプ','本格投資の前に、検証目的を明確にして小さく試す。'),
('新しい発想を短期間で形にする','限られた時間で参加者がアイデアを出し、試作品や成果を作る。','通常業務の開発工程ではなく、集中型の共創イベントか。','ハッカソン、オープンイノベーション','技術開発では、外部知識や多様な参加者を取り込む方法もある。'),
('競合の知財動向から技術戦略を読む','特許情報などを分析し、技術・競合の動向を把握する。','知財情報を地図化・分析し、研究開発や事業戦略へ結び付けているか。','IPランドスケープ、特許戦略','知財情報は権利保護だけでなく、技術戦略や競争環境の分析材料になる。')]),
14: ('topics/r08-14-business-systems/index.html','r08-14-business-systems','問10・問25・問28',[
('生成AIの出力をそのまま事実と扱わない','生成AIがもっともらしい文章を出力する。','内容の自然さではなく、根拠・出典・事実確認ができているか。','生成AI、ハルシネーション、ヒューマンインザループ','生成AIは自然な誤情報を出すことがあるため、人が検証する前提で利用する。'),
('取引履歴を分散して保持する仕組みを見る','複数主体で取引情報を共有し、改ざん耐性や追跡性を高める。','中央の一主体だけでなく、複数の参加者が同じ履歴を共有する構造か。','ブロックチェーン、分散台帳、トレーサビリティ','ブロックチェーンは履歴共有・追跡・改ざん耐性を生かす用途で使われる。'),
('生成AIと従来の機械学習の違いを見る','入力データから新しい文章・画像などを作るAIを扱う。','分類や予測だけでなく、新しいコンテンツを生成しているか。','生成AI、基盤モデル','AIの用途は予測・分類だけでなく、コンテンツ生成へ広がっている。')]),
15: ('topics/r08-15-engineering-systems/index.html','r08-15-engineering-systems','問11',[
('生産設備を柔軟に組み替える','製品種類や生産量の変化に合わせて、生産設備の構成を変えたい。','専用ラインではなく、複数工程・製品へ柔軟に対応する生産システムか。','FMS、柔軟生産','FMSは設備や工程を柔軟に組み替え、多品種・変動する生産へ対応する。')]),
17: ('topics/r08-17-iot-embedded-systems/index.html','r08-17-iot-embedded-systems','問33',[
('自動運転レベルで人とシステムの役割を分ける','車両が自動で走行するが、条件によって人の対応が必要になる。','システムが運転主体か、人が常時監視するのか、作動継続困難時に誰が対応するか。','自動運転レベル、運転主体、フォールバック','自動運転は「自動化されているか」だけでなく、誰が運転主体で、どの条件で人へ戻るかで区別する。')]),
18: ('topics/r08-18-information-systems-strategy/index.html','r08-18-information-systems-strategy','問27',[
('業務と情報システムの全体像を設計する','現状と理想像を整理し、業務・データ・アプリケーション・技術の関係を整える。','個別システムの設計ではなく、企業全体の構造と移行を扱っているか。','EA、現状モデル、目標モデル','EAは経営戦略と情報システムを結び、現状から目標像への全体的な構造を整理する。')]),
19: ('topics/r08-19-business-process/index.html','r08-19-business-process','問17・問24・問32',[
('実際の処理記録から業務の流れを把握する','システムの操作ログなど、業務で実際に発生した記録がある。','想定した手順ではなく、実行履歴から業務プロセスを再構成・分析しているか。','プロセスマイニング、イベントログ','プロセスマイニングは実データから実際の業務の流れや滞留を可視化する。'),
('定型作業をソフトウェアで自動化する','画面操作や転記など、ルールが明確な定型作業が繰り返される。','人の判断が中心か、決まった操作手順を自動実行できるか。','RPA、業務自動化','RPAは定型的な事務操作をソフトウェアロボットで自動化する。'),
('人の行動履歴をデータとして扱う','移動履歴やWeb利用履歴など、個人の行動記録を業務やサービスに活用する。','記録しているのが人の生活・行動履歴か。','ライフログ','業務改善で使うデータには、機械ログだけでなく人の行動ログも含まれる。')]),
24: ('topics/r08-24-procurement-planning-execution/index.html','r08-24-procurement-planning-execution','問13',[
('提案を求める前に情報を集める','新しいITソリューションの候補や技術動向を知りたい。','具体提案や価格を求める段階か、その前に選択肢や市場情報を集める段階か。','RFI、RFP','RFIは提案依頼の前段で情報収集を行い、RFPは要件・条件を示して具体的な提案を求める。')]),
25: ('topics/r08-25-system-development-technology/index.html','r08-25-system-development-technology','問46',[
('開発後のソフトウェアを本番環境へ移す','開発が完了したソフトウェアを利用環境へ導入する。','開発・テストではなく、利用者が使う環境へ展開し運用を始める段階か。','導入、移行、受入れ、利用者教育','開発プロセスは作って終わりではなく、受入れ・移行・教育を経て実運用へつながる。')]),
26: ('topics/r08-26-development-process-methods/index.html','r08-26-development-process-methods','問39・問44',[
('変更へ早く対応する開発と順序を固定する開発を分ける','要件変更が多い開発と、工程を順番に進める開発を比べる。','反復しながら変更へ適応するのか、工程完了後に次へ進むのか。','アジャイル、ウォーターフォール','開発モデルは変更頻度や要件の確定度によって向き不向きがある。'),
('早い段階で動くものを見せる','利用者の要求が十分に固まっていない。','試作品を作り、利用者の確認を通して要求を明確化するか。','プロトタイピングモデル','要求が曖昧なときは、試作品による確認を通じて認識差を減らす方法がある。')]),
27: ('topics/r08-27-project-management/index.html','r08-27-project-management','問40・問41・問45・問48・問52・問55',[
('変更要求を正式な手続で評価する','プロジェクト中に範囲・コスト・納期へ影響する変更要求が出た。','誰が影響を評価し、承認・却下を決めるか。','変更管理、変更管理委員会、CCB','変更は担当者の判断だけで反映せず、影響を評価して正式に管理する。'),
('進捗を作業量だけでなく価値とコストで見る','予定と実績のずれを数量的に把握したい。','完成した作業の価値、計画価値、実コストを分けているか。','EVM、スケジュール差異、コスト差異','進捗率だけではなく、予定・成果・費用を同じ基準で比較すると遅延とコスト超過を分けられる。'),
('スコープと品質・要員を管理対象として分ける','成果物、品質評価、人員配置など複数の管理課題がある。','何を作るか、品質をどう保証するか、誰を配置するかを別の管理対象として整理できるか。','スコープ管理、品質管理、人的資源管理','プロジェクト管理では、範囲・品質・要員などを分けて管理し、相互影響を調整する。')]),
28: ('topics/r08-28-service-management/index.html','r08-28-service-management','問37',[
('合意したサービス水準を継続的に管理する','顧客とサービス品質を合意し、実績を測定して改善する。','合意文書そのものか、その水準を維持・改善する管理活動か。','SLA、SLM','SLAは合意内容、SLMは合意したサービス水準を測定・管理・改善する活動として分ける。')]),
29: ('topics/r08-29-service-management-system/index.html','r08-29-service-management-system','問36・問49・問50・問54',[
('使えた時間でサービス品質を見る','サービス提供時間のうち、実際に利用できた時間を評価する。','機能の豊富さではなく、必要な時間に利用可能だったか。','可用性、サービス可用性管理','可用性は、サービスを必要な時間に利用できる度合いとして見る。'),
('問い合わせを人だけで処理しない','同じ問い合わせが繰り返され、担当者の負荷が高い。','FAQによる自己解決、チャットボット、自動応答などで窓口負荷を下げられるか。','サービスデスク、FAQ、チャットボット、AIOps','サービスデスクは単一窓口を提供し、自己解決支援や自動化を組み合わせて効率と品質を高める。')]),
30: ('topics/r08-30-facility-management/index.html','r08-30-facility-management','問42',[
('配線変更しやすい床下空間を確保する','オフィスや機械室で、配線を床下へ収め、変更や増設に対応したい。','床面の下に一定の空間を作り、ケーブル経路として使う構造か。','フリーアクセスフロア','ファシリティでは、設備の配置だけでなく保守・変更のしやすさも設計対象になる。')]),
31: ('topics/r08-31-system-audit/index.html','r08-31-system-audit','問38・問51',[
('監査の目的と独立性を見る','情報システムの管理・統制が適切かを第三者的に評価する。','助言・保証を行う立場が、監査対象の実務責任から独立しているか。','システム監査、監査人の独立性','監査はシステムを運用することではなく、基準に照らして客観的に評価し、改善へつなげる活動。')]),
32: ('topics/r08-32-internal-control/index.html','r08-32-internal-control','問43・問53',[
('承認と実行を分けて不正・誤りを防ぐ','経費精算や支払処理などで、申請・承認・実行を同じ人が行える。','相互牽制が働くよう、権限や役割を分けているか。','職務分掌、承認、内部統制','内部統制では、誤りや不正を起こしにくく発見しやすい業務手続を設計する。'),
('ITへの対応を内部統制の一部として捉える','業務が情報システムへ依存している。','IT統制が業務目標・財務報告・法令遵守などの目的を支える構造になっているか。','ITへの対応、全般統制、業務処理統制','IT統制はIT部門だけの問題ではなく、組織の内部統制目的を支える仕組みとして位置付ける。')]),
35: ('topics/r08-35-information-theory/index.html','r08-35-information-theory','問80・問81・問86',[
('広いデータで学習したモデルを用途へ展開する','大量・多様なデータで事前学習したモデルを、複数用途へ利用する。','特定用途専用モデルか、幅広い用途の基盤として再利用されるモデルか。','基盤モデル、ファインチューニング','基盤モデルは大規模な事前学習を基に、追加学習や指示で多様な用途へ展開できる。'),
('画像の文字をデータへ変換する','紙文書や画像内の文字を読み取り、検索・編集できるデータにしたい。','画像処理の目的が文字認識か。','OCR','OCRは画像として存在する文字を認識し、文字データへ変換する。'),
('特徴を自動抽出する多層学習を見る','大量の画像や音声から特徴を自動的に学習する。','人が特徴量を細かく設計するのではなく、多層ネットワークが特徴を学ぶか。','ディープラーニング、ニューラルネットワーク','深層学習は多層のニューラルネットワークによって特徴表現を学習する。')]),
37: ('topics/r08-37-algorithms-programming/index.html','r08-37-algorithms-programming','問78・問98・問99',[
('余りを条件判定に使う','繰返しの中で一定の倍数だけを加算・処理する。','除算の商ではなく余りを使って条件を判定しているか。','剰余、mod、条件分岐','剰余演算は倍数判定や周期的な処理に使える。'),
('並べ替えの操作単位を追う','配列から最小値を探して先頭から確定していく。','比較・交換がどの順番で行われ、何回繰り返すか。','選択ソート、配列、反復','ソートは最終結果だけでなく、1回の反復で何が確定するかを追うと理解しやすい。'),
('条件の組合せで処理を分ける','複数条件に応じて金額などを切り替える関数を読む。','if/elseの条件がどの順に評価されるか。','条件分岐、関数、比較演算','条件分岐は上から評価されるため、条件の範囲と順序を確認する。')]),
41: ('topics/r08-41-memory/index.html','r08-41-memory','問75',[
('主記憶と補助記憶を区別する','RAM、ROM、SSD、光ディスクなどを比較する。','CPUが直接使う主記憶か、長期保存用の補助記憶か。','RAM、ROM、SSD、CD-ROM、DVD-RAM','記憶装置は、揮発性・書換え可否・用途・記憶階層で整理する。')]),
43: ('topics/r08-43-system-configuration/index.html','r08-43-system-configuration','問82',[
('同じデータを複数場所へ複製する','一つのデータベース内容を別のコンピュータにも保持する。','バックアップ保管か、複数拠点で同じデータを同期して使う仕組みか。','レプリケーション、冗長化','レプリケーションはデータを複製・同期し、可用性や性能を高める構成で使われる。')]),
44: ('topics/r08-44-system-evaluation-indicators/index.html','r08-44-system-evaluation-indicators','問94',[
('並列構成で全体の稼働率を高める','同じ装置を複数並列に置き、一部故障でもサービスを継続したい。','全台正常が必要な直列構成か、どれか一台でも動けばよい並列構成か。','稼働率、並列システム、冗長化','システム全体の稼働率は、構成要素の稼働率だけでなく直列・並列など接続構成で変わる。')]),
47: ('topics/r08-47-office-tools/index.html','r08-47-office-tools','問22・問76',[
('表計算で参照位置を固定する','数式をコピーして複数セルへ適用する。','コピー先に応じて変わる参照と、行・列を固定する参照を使い分けられているか。','相対参照、絶対参照、複合参照','表計算では、コピー時に変化させたい行・列だけを相対参照にする。'),
('データ処理に合うツールを選ぶ','多数のデータを集計・可視化・分析する。','文書作成、表計算、データ分析など目的に合うツールか。','オフィスツール、データ分析','ツールは名称ではなく、処理したいデータと作業目的に合わせて選ぶ。')]),
48: ('topics/r08-48-open-source-software/index.html','r08-48-open-source-software','問96',[]),
50: ('topics/r08-50-information-design/index.html','r08-50-information-design','問18・問72',[
('誰でも使いやすい情報設計にする','年齢や障害の有無などにかかわらず情報へアクセスできるようにする。','特定利用者だけに合わせず、利用上の障壁を減らせているか。','アクセシビリティ、ユニバーサルデザイン','情報デザインでは見た目だけでなく、利用できる人の範囲と障壁の少なさも考える。'),
('配置の原則で情報の関係を見せる','画面や資料の要素を見やすく配置する。','近接・整列・反復・対比のどの原則で関係や階層を示しているか。','近接、整列、反復、対比','同じ情報でも配置と強弱によって、まとまり・順序・重要度の伝わり方が変わる。')]),
51: ('topics/r08-51-interface-design/index.html','r08-51-interface-design','問47・問79',[
('利用者が直接触れる境界を見る','ATMなどで利用者が画面や操作部を使って処理する。','利用者とシステムの接点として、操作の分かりやすさを設計しているか。','ユーザインタフェース、使用性','インタフェースは機器内部の接続だけでなく、人とシステムの接点も含む。'),
('一覧を小さな画像で見渡せるようにする','多くの画像やページを一覧から選びたい。','内容全体を開く前に、小さな代表画像で識別できるか。','サムネイル','サムネイルは複数候補を一覧で比較・選択しやすくする表示方法。')]),
55: ('topics/r08-55-database-design/index.html','r08-55-database-design','問65・問95',[
('検索を速くするための索引を持つ','大量データから条件に合う行を繰り返し検索する。','表そのものの並び替えではなく、検索用の索引を使うか。','インデックス','インデックスは検索を高速化するための補助構造で、更新コストとのトレードオフがある。'),
('必要なデータ項目と関係を整理する','業務で使うデータをデータベース化する前に構造を決める。','個々の値ではなく、必要なデータ項目と相互関係をモデル化しているか。','データモデリング、E-R図、正規化','データベース設計では、業務で必要なデータと関係を先に整理して構造化する。')]),
56: ('topics/r08-56-data-operations/index.html','r08-56-data-operations','問66',[
('複数表を関連付けて条件検索する','ログ表と部署表など、別々の表に必要情報が分かれている。','共通キーで表を結び、期間・結果などの条件で絞り込めるか。','結合、選択、検索条件','データ操作では、必要な列を持つ表を結合し、条件に合う行を選択して目的の情報を取り出す。')]),
57: ('topics/r08-57-transaction-processing/index.html','r08-57-transaction-processing','問61',[
('処理の途中失敗を一まとまりとして戻す','複数更新からなる処理の途中で障害が起きた。','一部だけ反映せず、処理開始前の整合した状態へ戻せるか。','トランザクション、ロールバック、ACID','トランザクションは一連の処理を一単位として扱い、失敗時は途中状態を残さない。')]),
58: ('topics/r08-58-network-methods/index.html','r08-58-network-methods','問56・問57・問71',[
('無線方式を到達距離・消費電力で比べる','IoT機器などを無線接続したい。','通信距離、データ量、消費電力のどれを重視するか。','BLE、無線LAN、LPWA','無線方式は速度だけでなく、距離・消費電力・用途の組合せで選ぶ。'),
('周波数と電波の性質を見る','異なる周波数帯の無線通信を比べる。','周波数が高い・低いことで、回り込みや直進性などの特性がどう変わるか。','周波数、電波伝搬','無線通信では周波数帯によって伝わり方や用途が変わる。'),
('通信を中継する役割を見る','端末からWebサーバへ接続する間に中継サーバを置く。','名前解決やIP割当てではなく、通信要求を代理して中継する仕組みか。','プロキシサーバ','プロキシはクライアントの代理として外部サーバへ接続し、制御・キャッシュなどにも使われる。')]),
59: ('topics/r08-59-communication-protocols/index.html','r08-59-communication-protocols','問60',[
('ファイル転送用プロトコルを識別する','ネットワークを介してファイルを送受信する。','メール送受信や名前解決ではなく、ファイル転送のための通信規約か。','FTP','プロトコルは「何を運ぶか・何を解決するか」という役割で区別する。')]),
60: ('topics/r08-60-network-applications/index.html','r08-60-network-applications','問58・問64',[
('名前とIPアドレスを対応付ける','利用者はドメイン名を入力するが、通信にはIPアドレスが必要になる。','ドメイン名をIPアドレスへ変換する仕組みか。','DNS','DNSは人が扱いやすい名前とネットワーク上のIPアドレスを対応付ける。'),
('Web更新情報を定型形式で配信する','Webサイトの新着情報をまとめて受け取りたい。','ページの見た目を定義するのではなく、更新情報を配信・購読する仕組みか。','RSS','RSSはWebサイトの更新情報を定型形式で配信し、購読側でまとめて取得できる。')]),
61: ('topics/r08-61-information-security/index.html','r08-61-information-security','問73・問93・問97',[
('攻撃手口を侵入経路と狙いで分ける','Webサービスやネットワークが攻撃を受ける。','脆弱性悪用、総当たり、サービス妨害など、攻撃の成立条件と目的を分けられるか。','DDoS、ゼロデイ、ブルートフォース、脆弱性','攻撃名を覚えるだけでなく、何を悪用し何を起こす攻撃かで整理する。'),
('機密性・完全性・可用性で影響を分ける','情報漏えい、改ざん、サービス停止などの事故を評価する。','秘密が漏れたのか、内容が変えられたのか、使えなくなったのか。','機密性、完全性、可用性','情報セキュリティの影響はCIAのどの性質が損なわれたかで整理する。')]),
62: ('topics/r08-62-information-security-management/index.html','r08-62-information-security-management','問59・問68・問83・問84・問91',[
('インシデント対応組織の役割を見る','組織内外でセキュリティ事故が発生する。','検知・連絡・分析・復旧支援・再発防止を組織的に調整する役割か。','CSIRT、インシデント管理','CSIRTは事故対応を技術対応だけで終わらせず、連絡・分析・調整を含めて組織的に進める。'),
('ISMSを方針・リスク・監査・改善の循環で見る','情報セキュリティ管理を継続的に運用する。','方針を決め、リスクを評価し、実施状況を監査し、改善へ戻す流れになっているか。','ISMS、PDCA、内部監査、リスク対応','ISMSは単発の対策ではなく、管理の仕組みを継続的に改善する。')]),
63: ('topics/r08-63-security-measures-implementation/index.html','r08-63-security-measures-implementation','問69・問70・問74・問77・問87・問88・問89・問90・問92・問100',[
('認証の使いやすさと誤判定を調整する','生体認証で本人拒否と他人受入れの両方を減らしたい。','本人拒否率と他人受入率のどちらを厳しくする設定か。','FAR、FRR、生体認証、多要素認証','認証強度を高めると利便性とのトレードオフが生じる。生体認証では誤受入れと誤拒否を分けて評価する。'),
('脆弱性をふさぐ対策と攻撃を検知する対策を分ける','既知・未知の脆弱性や不正通信に備える。','修正プログラムで弱点を減らすのか、IDSなどで不審な通信を検知するのか。','セキュリティパッチ、ゼロデイ、IDS','予防・検知・対応は別の役割であり、単一対策だけでは十分でない。'),
('暗号と証明書で通信相手と内容を守る','公開鍵、証明書、暗号化通信、無線LANを扱う。','相手の正当性確認と通信内容の秘匿をどの仕組みで実現するか。','PKI、デジタル証明書、公開鍵暗号、WPA','暗号化だけでなく、鍵や証明書を誰が信頼できる形で管理するかが重要になる。'),
('感染後の復旧と証拠保全まで考える','ランサムウェア感染や不正アクセスが発生した。','バックアップで復旧できるか、原因調査に必要な証拠を適切に保全できるか。','バックアップ、ランサムウェア、デジタルフォレンジックス','セキュリティ対策は侵入防止だけでなく、復旧と事後調査まで含めて設計する。'),
('人的・物理的な対策も組み合わせる','退職者のアカウント、入退室、情報持出しなど技術以外のリスクがある。','技術対策だけでなく、人・ルール・設備の管理ができているか。','人的対策、物理的対策、アカウント管理','情報セキュリティは技術・人・物理環境を組み合わせて守る。')]),
}

HELD = {22:'既存の統合項目ページがなく、新規URL命名規則を安全に確定できない',34:'既存の統合項目ページがなく、新規URL命名規則を安全に確定できない',40:'既存の統合項目ページがなく、新規URL命名規則を安全に確定できない',45:'既存の統合項目ページがなく、新規URL命名規則を安全に確定できない',53:'既存の統合項目ページがなく、新規URL命名規則を安全に確定できない'}
FIELD = {**{i:('strategy','ストラテジ系') for i in range(1,25)}, **{i:('management','マネジメント系') for i in range(25,33)}, **{i:('technology','テクノロジ系') for i in range(33,64)}}

STYLE = '''\n    .integrated-scenes{margin:1.2rem 0 1.6rem;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.8rem}\n    .integrated-scene{min-width:0;padding:1rem;border:1px solid var(--color-border,#d9d3c8);border-radius:16px;background:#fff}\n    .integrated-scene h2{margin:0 0 .7rem;font-size:1.05rem;line-height:1.45}\n    .integrated-scene dl{display:grid;grid-template-columns:7rem minmax(0,1fr);gap:.38rem .7rem;margin:0}\n    .integrated-scene dt{font-size:.78rem;font-weight:700;color:var(--text-sub,#675f55)}\n    .integrated-scene dd{margin:0;line-height:1.55}\n    @media(max-width:700px){.integrated-scenes{grid-template-columns:1fr}.integrated-scene dl{grid-template-columns:1fr;gap:.1rem}.integrated-scene dd{margin-bottom:.45rem}}\n'''

def sh(*args, check=True):
    return subprocess.run(args, cwd=ROOT, text=True, check=check, capture_output=True)

def neutralize(html, item):
    field, label = FIELD[item]
    html = re.sub(r'令和8年度｜(?=項目\s*%d\b)' % item, '', html)
    html = html.replace('令和8年度ITパスポート公開問題のうち、', 'ITパスポート試験シラバスの')
    html = html.replace('令和8年度の公開問題をもとに', '公開問題をもとに')
    html = html.replace('令和8年度', '')
    html = html.replace('<a href="../../past-questions/r08/">公開問題</a>', f'<a href="../../fields/{field}/">{label}</a>')
    html = html.replace('<a href="../../past-questions/r08/">公開問題へ戻る</a>', '<a href="../../past-questions/">公開問題一覧へ戻る</a>')
    html = html.replace('<a href="../../past-questions/r08/">R8公開問題へ戻る</a>', '<a href="../../past-questions/">公開問題一覧へ戻る</a>')
    html = html.replace('<a href="../../past-questions/r08/">R08公開問題へ戻る</a>', '<a href="../../past-questions/">公開問題一覧へ戻る</a>')
    html = html.replace('<a href="../../past-questions/r08/">公開問題一覧へ戻る</a>', '<a href="../../past-questions/">公開問題一覧へ戻る</a>')
    html = html.replace('../../past-questions/r08/">公開問題', f'../../fields/{field}/">{label}')
    if '<a href="../../fields/">学習分野</a>' not in html:
        html = html.replace('<a href="../../">トップ</a>', '<a href="../../">トップ</a>\n      <a href="../../fields/">学習分野</a>', 1)
    return html

def integrated_block(scenes):
    if not scenes:
        return ''
    cards=[]
    for title,scene,judge,knowledge,point in scenes:
        cards.append(f'''<article class="integrated-scene"><h2>{title}</h2><dl><dt>場面</dt><dd>{scene}</dd><dt>判断すること</dt><dd>{judge}</dd><dt>関係する知識</dt><dd>{knowledge}</dd><dt>学習要点</dt><dd>{point}</dd></dl></article>''')
    return '\n<section class="integrated-scenes" data-integrated-source="r07" aria-label="項目の判断場面">' + ''.join(cards) + '</section>\n'

def update_page(item, path, refs, scenes):
    p=ROOT/path
    if not p.exists():
        raise RuntimeError(f'missing page {path}')
    html=p.read_text(encoding='utf-8')
    html=neutralize(html,item)
    if 'integrated-scenes{' not in html:
        html=html.replace('</style>', STYLE+'  </style>',1)
    if scenes and 'data-integrated-source="r07"' not in html:
        h=html.find('<h2>参照した公開問題</h2>')
        if h<0:
            h=html.find('参照した公開問題')
        if h<0:
            raise RuntimeError(f'reference heading not found: {path}')
        sec=html.rfind('<section',0,h)
        if sec<0:
            raise RuntimeError(f'reference section not found: {path}')
        html=html[:sec]+integrated_block(scenes)+html[sec:]
    if f'令和7年度　{refs}' not in html:
        pat=r'(<h2>\s*参照した公開問題\s*</h2>)'
        ins=(r'\1'+f'<p>令和7年度　{refs}</p><p><a href="{IPA}" target="_blank" rel="noopener noreferrer">IPA公式ITパスポート試験 過去問題（令和7年度）</a></p>')
        html,n=re.subn(pat,ins,html,count=1)
        if n!=1:
            raise RuntimeError(f'could not insert references: {path}')
    html=html.replace('>IPA公式ITパスポート試験 過去問題</a>', '>IPA公式ITパスポート試験 過去問題（令和8年度）</a>')
    p.write_text(html,encoding='utf-8')

def link_index(item, slug):
    html=INDEX.read_text(encoding='utf-8')
    href=f'../../topics/{slug}/'
    if re.search(rf'<a id="item-{item}"[^>]*href="{re.escape(href)}"',html):
        return
    line_pat=rf'(?m)^(\s*)<div id="item-{item}" class="item-card item-card--pending">(.*)</div>$'
    repl=rf'\1<a id="item-{item}" class="item-card item-card--ready" href="{href}">\2</a>'
    html,n=re.subn(line_pat,repl,html,count=1)
    if n==0:
        a_pat=rf'(<a id="item-{item}" class="item-card )item-card--[^\"]+(" href=")[^"]+(\")'
        html,n=re.subn(a_pat,rf'\1item-card--ready\2{href}\3',html,count=1)
    if n!=1:
        raise RuntimeError(f'index card not found for item {item}')
    INDEX.write_text(html,encoding='utf-8')

def commit_item(item,path):
    sh('git','add',str(path),str(INDEX.relative_to(ROOT)))
    diff=sh('git','diff','--cached','--quiet',check=False)
    if diff.returncode==0:
        return
    sh('git','commit','-m',f'Integrate R07 item {item} into shared topic page')
    sh('git','push','origin','main')

def verify():
    html=INDEX.read_text(encoding='utf-8')
    problems=[]
    for item,(path,slug,refs,scenes) in DATA.items():
        if not re.search(rf'<a id="item-{item}" class="item-card item-card--ready" href="../../topics/{re.escape(slug)}/"',html):
            problems.append(f'item {item}: index link')
        text=(ROOT/path).read_text(encoding='utf-8')
        if f'令和7年度　{refs}' not in text:
            problems.append(f'item {item}: R07 refs')
    if problems:
        raise RuntimeError('verification failed: '+', '.join(problems))
    print('Verified integrated items:', ','.join(map(str,DATA)))
    print('Held items:', HELD)

def cleanup():
    wf=ROOT/'.github/workflows/integrate-r07-items.yml'
    me=ROOT/'scripts/integrate_r07_items.py'
    sh('git','pull','--rebase','origin','main')
    sh('git','rm','--ignore-unmatch',str(wf.relative_to(ROOT)),str(me.relative_to(ROOT)))
    diff=sh('git','diff','--cached','--quiet',check=False)
    if diff.returncode!=0:
        sh('git','commit','-m','Remove one-shot R07 integration automation')
        sh('git','push','origin','main')

def main():
    for item in sorted(DATA):
        path,slug,refs,scenes=DATA[item]
        sh('git','pull','--rebase','origin','main')
        update_page(item,Path(path),refs,scenes)
        link_index(item,slug)
        commit_item(item,Path(path))
        print(f'completed item {item}')
    verify()
    cleanup()

if __name__=='__main__':
    try:
        main()
    except Exception as e:
        print(e,file=sys.stderr)
        raise

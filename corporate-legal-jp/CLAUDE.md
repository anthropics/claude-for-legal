<!--
CONFIGURATION LOCATION

User-specific configuration for this plugin lives at a version-independent path that survives plugin updates:

  ~/.claude/plugins/config/claude-for-legal/corporate-legal-jp/CLAUDE.md

Rules for every skill, command, and agent in this plugin:
1. READ configuration from that path. Not from this file.
2. If that file does not exist or still contains [PLACEHOLDER] markers, STOP before doing substantive work. Say: "このプラグインは設定が必要です。`/corporate-legal-jp:cold-start-interview` を実行してください（所要時間約10〜15分）。すべてのスキルがこの設定に依存しています。設定なしでは汎用的な出力となり、実務に合わない可能性があります。" Do NOT proceed with placeholder or default configuration. The only skills that run without setup are /corporate-legal-jp:cold-start-interview itself and any --check-integrations flag.
3. Setup and cold-start-interview WRITE to that path, creating parent directories as needed.
4. On first run after a plugin update, if a populated CLAUDE.md exists at the old cache path
   (~/.claude/plugins/cache/claude-for-legal/corporate-legal-jp/<version>/CLAUDE.md for any version)
   but not at the config path, copy it forward to the config path before proceeding.
5. This file (the one you are reading) is the TEMPLATE. It ships with the plugin and shows the
   structure the config should have. It is replaced on every plugin update. Never write user data here.

**Shared company profile.** Company-level facts (who you are, what you do, where you operate, your risk posture, key people) live in `~/.claude/plugins/config/claude-for-legal/company-profile.md` — one level above this file, shared by all plugins. Read it before this plugin's practice profile. If it doesn't exist, this plugin's setup will create it.
-->

# 会社法務プラクティスプロファイル
*cold-start-interview により [DATE] に作成。有効モジュール: [M&A | 取締役会・株主総会 | 上場会社 | 登記・エンティティ管理]*
*`[PLACEHOLDER]` が残っている場合は `/corporate-legal-jp:cold-start-interview` を実行してください。*

---

## 組織情報

**法人名:** [PLACEHOLDER] *（company-profile.md から参照 — 全プラグイン共通で変更する場合はそちらを編集）*
**業種:** [PLACEHOLDER] *（company-profile.md から参照）*
**法人形態:** [PLACEHOLDER — 株式会社 / 合同会社 / 持分会社 / その他]
**資本金:** [PLACEHOLDER — 例: 1億円]
**上場/非上場:** [PLACEHOLDER — 東証プライム / 東証スタンダード / 東証グロース / 非上場]
**本店所在地:** [PLACEHOLDER]
**事業年度:** [PLACEHOLDER — 例: 4月1日〜3月31日]
**ガバナンスモデル:** [PLACEHOLDER — 監査役設置会社 / 監査等委員会設置会社 / 指名委員会等設置会社]
**従業員数:** [PLACEHOLDER]
**法務部門の規模:** [PLACEHOLDER] *（company-profile.md から参照）*
**エスカレーション先:** [PLACEHOLDER — 顧問弁護士事務所名、法務部長名、取締役会エスカレーション経路]

**利用環境:** [PLACEHOLDER — 企業法務部（インハウス） | 法律事務所 | スタートアップ（兼務）] *（company-profile.md から参照）*

---

## 利用者情報

**役割:** [PLACEHOLDER — 弁護士・法務専門職 | 弁護士アクセスのある非法務担当者 | 弁護士アクセスのない非法務担当者]
**弁護士連絡先:** [PLACEHOLDER — 氏名 / チーム / 顧問弁護士事務所 / N/A（法務担当者でない場合に記入）]

*スキルはこのセクションを読んで、成果物のヘッダー選択と重要アクションのゲート判定を行います（下記`## 出力設定`および各スキルのゲートを参照）。*

---

**クライアント向け・役員向け成果物のクワイエットモード。** 法務外部または社外の読者が読む成果物 — 取締役会メモ、書面決議、株主総会招集通知、稟議書、クライアントレター — では内部ナレーションを抑制する:
- 成果物ヘッダー: 維持
- 注意事項メモ: 維持
- 出典タグ: インラインで維持（脚注・巻末注に集約可）
- スキル説明（「Xスキルを使用しています...」）: 削除
- プラグインハンドオフ（「次に/plugin:other-commandを実行...」）: 成果物から削除、別途注記に記載
- 「以下のファイルを読みました...」: 削除

成果物はパートナー弁護士が書いたように読めること。メタコメントは成果物の上の注記欄か別メッセージに記載し、本文中には入れない。

## 連携ツール

| 連携先 | ステータス | 未接続時のフォールバック |
|---|---|---|
| 登記情報提供サービス | [○ / ×] | 登記情報はユーザーが手動で貼り付け |
| EDINET | [○ / ×] | 有価証券報告書等はユーザーがアップロード |
| クラウドサイン | [○ / ×] | 電子署名はユーザーが手動で管理 |
| Box / Google Drive / SharePoint | [○ / ×] | ローカルパスから読取り、クロスシステム検索なし |
| iManage | [○ / ×] | ドキュメント管理はローカルフォルダベース |
| Slack | [○ / ×] | ファイル出力のみ、チャネルサマリーなし |

*再確認: `/corporate-legal-jp:cold-start-interview --check-integrations`*

---

## 出力設定

**成果物ヘッダー**（本プラグインが生成するすべての分析、メモ、レビュー、ドラフトに付記）:

- 役割が **弁護士** の場合: `秘密 — 弁護士業務成果物 — 弁護士の指示に基づき作成`
- 役割が **法務部員** の場合: `調査ノート — 法的助言ではありません — 行動する前に弁護士に相談してください`
- 役割が **その他** の場合: `調査ノート — 法的助言ではありません — 行動する前に資格を有する弁護士に相談してください`

**日本法における秘匿特権の留意点。** 日本には米国のattorney-client privilegeやwork product doctrineに直接対応する制度はない。弁護士・依頼者間の秘密交通権（刑訴法第105条）は刑事手続における押収拒絶権であり、民事ディスカバリーにおける広範な秘匿特権とは異なる。独占禁止法における立入検査での弁護士・依頼者間通信の保護（判審査手続における秘匿特権）は2020年に公正取引委員会の運用として導入されたが、その範囲は限定的である。ヘッダーは「秘密保持」の意思表示として有用だが、米国法上の保護を自動的に付与するものではないことに留意すること。

---

**注意事項メモ — 成果物の直上に1ブロック。** レビュアーが成果物を信頼する前に知るべきことすべてをここに集約する:

> **注意事項メモ**
> - **出典:** [リサーチツール: 接続済み○ / 未接続 — 訓練データからの引用、信頼前に要確認]
> - **読取範囲:** [全N頁中1-50頁 / 全3文書 / N/A]
> - **要判断事項:** [インラインで`[要確認]`マークN件 / なし]
> - **最新性:** [[日付]以降の動向を検索 — 該当なし / N件の更新あり / 検索不可、[特定の規則]を確認のこと]
> - **信頼前に:** [レビュアーが実際に行うべき1-2項目 — または問題なければ「確認済み」]

---

**次のステップの決定木。** 分析・レビュー・トリアージ・評価の後、選択肢のツリーで締める — 決定ではなくオプションのドラフト:

> **次のアクションを選んでください:**
> 1. **[Xをドラフト]** — [メモ / 修正案 / 回答書 / エスカレーション / 方針変更]のドラフトを作成します。
> 2. **エスカレーション** — [プラクティスプロファイルの承認者]宛のエスカレーションドラフトを作成します。
> 3. **追加情報の収集** — 助言の前に確認すべき[2-3の未解決事項]があります。
> 4. **経過観察** — [トラッカー / 監視リスト]に追加し、見直し時期を記録します。
> 5. **その他** — ご希望の対応をお知らせください。

---

## 取締役会・株主総会

**取締役の構成:**
- 取締役数: [PLACEHOLDER — N名]
- 社外取締役数: [PLACEHOLDER — N名]
- 代表取締役: [PLACEHOLDER]
- 取締役会議長: [PLACEHOLDER — 代表取締役 / 会長 / 社外取締役]

**監査役・監査委員の構成:**
- ガバナンスモデル: [PLACEHOLDER — 監査役設置会社 / 監査等委員会設置会社 / 指名委員会等設置会社]
- 監査役数（監査役設置会社の場合）: [PLACEHOLDER — N名（うち社外監査役N名）]
- 監査等委員数（監査等委員会設置会社の場合）: [PLACEHOLDER — N名]
- 指名委員会等設置会社の場合の各委員会構成: [PLACEHOLDER]

**取締役会:**
- 開催頻度: [PLACEHOLDER — 月1回 / 隔月 / 四半期]
- 議事録フォーマット: [PLACEHOLDER — 長文記述型 / 要点記録型]
- 議事録タイミング: [PLACEHOLDER — 開催後N日以内に回覧]
- 書面決議（みなし決議）の定款条項: [PLACEHOLDER — あり / なし]
- 議事録署名方式: [PLACEHOLDER — 出席取締役・出席監査役の記名押印 / 電子署名]
- テレビ会議・電話会議の利用: [PLACEHOLDER — 定款で許容 / 取締役会規則で許容 / 不可]

**株主総会:**
- 定時株主総会の時期: [PLACEHOLDER — 例: 毎年6月（基準日から3ヶ月以内）]
- 基準日: [PLACEHOLDER — 例: 3月31日]
- 招集通知の発送時期: [PLACEHOLDER — 2週間前 / 上場会社は3週間前（電子提供措置の場合は3週間前に電子提供+1週間前に書面送付）]
- 株主構成: [PLACEHOLDER — 支配株主の有無、外国株主比率、主要株主]
- 書面投票・電子投票の採用: [PLACEHOLDER — あり / なし]

**議決権行使:**
- 書面投票制度（会社法第311条）: [PLACEHOLDER — 採用 / 非採用]
- 電子投票制度（会社法第312条）: [PLACEHOLDER — 採用 / 非採用]
- 議決権行使プラットフォーム: [PLACEHOLDER — ICJ / なし]

**種類株式・種類株主総会:**
- 種類株式の発行: [PLACEHOLDER — なし / あり（種類を記載）]
- 種類株主総会の要否: [PLACEHOLDER]

### シードドキュメント（取締役会・株主総会）

| ドキュメント | ソース | 日付 | 備考 |
|---|---|---|---|
| 取締役会議事録（先例） | [PLACEHOLDER] | | |
| 書面決議（先例） | [PLACEHOLDER] | | |
| 株主総会議事録（先例） | [PLACEHOLDER] | | |
| 定款 | [PLACEHOLDER] | | |

---

## M&A・組織再編

**典型的な立場:** [PLACEHOLDER — 買収側 / 売却側 / 両方]
**ディール頻度:** [PLACEHOLDER — 年N件のシリアルアクワイアラー / 案件ごと]
**ディールリード:** [PLACEHOLDER — 経営企画 / 法務 / 外部弁護士]

### デューディリジェンス

**DD項目カテゴリ:**
1. [PLACEHOLDER — DDチェックリストから抽出]

**重要性の基準:**
- 契約: [PLACEHOLDER — 全件 / 年間X万円超 / 上位N件]
- 訴訟: [PLACEHOLDER — 全件 / X万円超 / 重要なもののみ]

### イシューメモフォーマット

**構成:** [PLACEHOLDER]
**重要度スキーム:** [PLACEHOLDER — 赤/黄/緑 | 重大/高/中/低]
**対象読者:** [PLACEHOLDER — ディールリードのみ / ディールチーム / 取締役会]

### クロージングチェックリスト

**管理場所:** [PLACEHOLDER — Excel / プロジェクト管理ツール]
**オーナー:** [PLACEHOLDER]

### 組織再編

**経験のある手法:**
- [PLACEHOLDER — 株式譲渡 / 事業譲渡 / 合併（吸収合併・新設合併） / 会社分割（吸収分割・新設分割） / 株式交換 / 株式移転 / 第三者割当増資]

---

## エスカレーション（稟議制度）

**稟議制度:** [PLACEHOLDER — あり / なし]
**決裁権限基準:**
- 部長決裁: [PLACEHOLDER — X万円未満]
- 本部長決裁: [PLACEHOLDER — X万円以上Y万円未満]
- 取締役会決議: [PLACEHOLDER — Y万円以上]
- 株主総会決議: [PLACEHOLDER — 会社法上の要件に基づく]

**法務部門の関与基準:**
- [PLACEHOLDER — 契約金額X万円以上 / 訴訟リスクあり / 新規取引先 / 反社チェック要]

**外部弁護士への相談基準:**
- [PLACEHOLDER — 訴訟案件 / M&A / 規制対応 / X万円以上の契約]

---

## 上場会社（該当する場合のみ）

**上場市場:** [PLACEHOLDER — 東証プライム / 東証スタンダード / 東証グロース / 非上場]
**証券コード:** [PLACEHOLDER]
**事業年度末:** [PLACEHOLDER]

**適時開示体制:**
- 開示担当部門: [PLACEHOLDER — IR / 法務 / 総務]
- 開示委員会: [PLACEHOLDER — あり / なし]
- 適時開示の承認フロー: [PLACEHOLDER]

**インサイダー取引規制管理:**
- 内部者登録管理: [PLACEHOLDER — 法務 / 総務 / 人事]
- 売買制限期間: [PLACEHOLDER — 決算期末からN日間]
- 事前承認制度: [PLACEHOLDER — あり / なし]

**コーポレートガバナンス・コード対応:**
- 対応状況: [PLACEHOLDER — フルコンプライ / エクスプレイン項目あり]
- スキル・マトリックス: [PLACEHOLDER — 開示済み / 未開示]

---

## 登記・エンティティ管理

**管理法人数:** [PLACEHOLDER — N法人]
**主要管轄:** [PLACEHOLDER — 法務局管轄]
**司法書士:** [PLACEHOLDER — 事務所名 / 自社対応]

**登記管理システム:** [PLACEHOLDER — 手動（Excel） / 専用システム]

**定期届出の管理者:** [PLACEHOLDER — 法務 / 総務 / 司法書士]
**登記期限の追跡方法:** [PLACEHOLDER]

**関連法人テーブル:**
*組織図または面談回答から抽出。*

| 法人名 | 法人形態 | 管轄法務局 | 親会社 | 出資比率 | ステータス |
|---|---|---|---|---|---|
| [PLACEHOLDER] | [株式会社/合同会社/その他] | [PLACEHOLDER] | [PLACEHOLDER] | [PLACEHOLDER] | [活動中/休眠中] |

---

## 共通ガードレール

本プラグインのすべてのスキルに適用される。スキルが独自の指示で繰り返す場合があるが、このセクションが正本 — スキルの記述と矛盾する場合はこのセクションが優先する。

**暗黙の補完禁止 — 3つの値。** スキルが持っていない情報（条文の全文、判例の立場、現行の施行日等）が必要な場合、有効な応答は3つ:

1. **フラグ付きで補完。** ウェブ検索、モデル知識等から引用し、タグ付け（`[ウェブ検索 — 要確認]`、`[モデル知識 — 要確認]`）して続行。
2. **何も言わず停止。** ユーザーにソースの貼り付けまたは指定を求め、提供されるまで続行しない。
3. **フラグのみ使用せず。** 規則の適用や効力に影響しうる情報（係属中の訴訟、改正案、施行日の延期等）を認識している場合、`[モデル知識 — 要確認]`タグ付きの注記として表面化させる。

**条文引用の正確性。** 会社法、会社法施行規則、金融商品取引法等の条文番号を引用する際は、正確な条項番号を確認すること。条文番号の誤りは分析全体の信頼性を損なう。確認できない場合は`[条文番号要確認]`とタグ付けする。

**出典タグのルール:**
- `[登記情報提供サービス]` / `[EDINET]` — 当該ツールからこのセッションで取得した場合のみ
- `[ユーザー提供]` — ユーザーが貼り付けまたはリンクした場合
- `[モデル知識 — 要確認]` — 上記以外すべて。デフォルト
- `[確定 — 最終確認 YYYY-MM-DD]` — 一次情報源で確認済みの安定的な法令参照

タグは出典を示すものであり、確信度を示すものではない。

**検証ログ。** フラグ付き事項が確認された場合、`~/.claude/plugins/config/claude-for-legal/corporate-legal-jp/verification-log.md`に記録:

`[YYYY-MM-DD] [引用または事実] [確認者]による[出典]での確認 — [結果: 確認 / Xに訂正 / 確認不可]`

---

## スカフォールディング（足場であって制約ではない）

プラグインの役割はClaudeの法務作業を改善することであり、既知の法理から遠ざけることではない。スキルにチェックリストやワークフローがある場合、それはフロア（最低基準）であり、シーリング（上限）ではない。チェックリストにない関連する法的分析がある場合は、「通常のチェックリスト外ですが関連します」と注記して回答する。

## 管轄の認識

本プラグインのデフォルトフレームワークは日本法に基づく。ただし、クロスボーダーM&A、外国子会社の管理等で日本法以外の管轄が関係する場合は、適用法の違いを認識し、適切に対応する。

---

*フルインタビュー再実行: `/corporate-legal-jp:cold-start-interview --redo`*
*モジュール追加: `/corporate-legal-jp:cold-start-interview --module [m&a | board | public | entities]`*
*新規ディール: `/corporate-legal-jp:cold-start-interview --new-deal`*

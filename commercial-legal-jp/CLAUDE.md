<!--
CONFIGURATION LOCATION

User-specific configuration for this plugin lives at a version-independent path that survives plugin updates:

  ~/.claude/plugins/config/claude-for-legal/commercial-legal-jp/CLAUDE.md

Rules for every skill, command, and agent in this plugin:
1. READ configuration from that path. Not from this file.
2. If that file does not exist or still contains [PLACEHOLDER] markers, STOP before doing substantive work. Say: "このプラグインを使用する前にセットアップが必要です。/commercial-legal-jp:cold-start-interview を実行してください。10〜15分で完了し、すべてのコマンドがこの設定に依存しています。セットアップなしでは、出力は汎用的なものになり、実務に合わない可能性があります。" Do NOT proceed with placeholder or default configuration. The only skills that run without setup are /commercial-legal-jp:cold-start-interview itself and any --check-integrations flag.
3. Setup and cold-start-interview WRITE to that path, creating parent directories as needed.
4. On first run after a plugin update, if a populated CLAUDE.md exists at the old cache path
   (~/.claude/plugins/cache/claude-for-legal/commercial-legal-jp/<version>/CLAUDE.md for any version)
   but not at the config path, copy it forward to the config path before proceeding.
5. This file (the one you are reading) is the TEMPLATE. It ships with the plugin and shows the
   structure the config should have. It is replaced on every plugin update. Never write user data here.

**Shared company profile.** Company-level facts (who you are, what you do, where you operate, your risk posture, key people) live in `~/.claude/plugins/config/claude-for-legal/company-profile.md` --- one level above this file, shared by all plugins. Read it before this plugin's practice profile. If it doesn't exist, this plugin's setup will create it.
-->

# 商事契約プラクティスプロファイル

*このファイルはコールドスタートインタビューの初回実行時に作成されます。それまではテンプレートです。
下記に `[PLACEHOLDER]` が表示されている場合は、`/commercial-legal-jp:cold-start-interview` を実行して
インタビューを受けてください。*

*設定完了後はこのファイルを直接編集してください。このプラグインのすべてのスキルが実行前にこのファイルを
読み込みます。ここを修正すれば、すべてに反映されます。*

---

## 組織情報

[PLACEHOLDER — 会社名]は[PLACEHOLDER — 法人形態（株式会社/合同会社/有限会社/その他）]です。
法務チームは[PLACEHOLDER — N]名で構成されています。[PLACEHOLDER — 法務責任者名]が最終エスカレーション先です。
月間約[PLACEHOLDER — N]件の契約書を処理しており、主に[PLACEHOLDER — 購買/販売/両方]側の契約を扱っています。

**業種:** [PLACEHOLDER — 業種（IT/製造/小売/金融/サービス等）]

**資本金:** [PLACEHOLDER — 金額（下請法の適用判定に使用）]

**従業員数:** [PLACEHOLDER — N名]

**CLMシステム:** [PLACEHOLDER — LegalForce/MNTSQ/ContractS/Holmes/その他/なし]

*(会社名、法人形態、業種、規模は company-profile.md から取得 --- そちらを編集すると全プラグインに反映されます。チーム規模、CLMシステム、エスカレーション先はプラグイン固有です。)*

**一番困っていること:** [PLACEHOLDER --- チームが言った困りごとを、そのままの言葉で]

**プラクティス設定:** [PLACEHOLDER --- 企業内法務 | 法律事務所 | その他] *(company-profile.md から --- そちらを編集すると全プラグインに反映)*

---

## 利用者情報

**役割:** [PLACEHOLDER --- 弁護士（企業内弁護士含む） / 法務部員（弁護士資格なし、顧問弁護士あり） / その他（弁護士資格なし、顧問弁護士なし）]

**顧問弁護士連絡先:** [PLACEHOLDER --- 弁護士名 / 事務所名 / 該当なし]

---

## 連携ツール

| 連携先 | 状態 | 未接続時のフォールバック |
|---|---|---|
| CLM（LegalForce / MNTSQ / ContractS / Holmes等） | [PLACEHOLDER --- 接続済/未接続] | 手動管理。renewal-trackerはローカルの更新台帳に対して実行 |
| 電子署名（クラウドサイン / DocuSign / GMOサイン等） | [PLACEHOLDER --- 接続済/未接続] | ユーザーがプラグイン外で署名手続きを実施 |
| 文書管理（Google Drive / SharePoint / Box） | [PLACEHOLDER --- 接続済/未接続] | レビューごとにユーザーが契約書をアップロード |
| コミュニケーション（Slack / Chatwork / LINE WORKS） | [PLACEHOLDER --- 接続済/未接続] | アラートやステークホルダーサマリーはインラインで表示 |

*再確認: `/commercial-legal-jp:cold-start-interview --check-integrations`*

---

## プレイブック

**アクティブサイド:** [PLACEHOLDER --- 購買側/販売側/両方 --- コールドスタート時に設定]

*販売側 = 自社が製品・サービスを販売する立場。自社ひな形を使用することが多い。購買側 = 外部ベンダーから購入する立場。相手方ひな形を使用することが多い。この区分によってすべてのプレイブックポジションが変わります --- リスク許容度、標準条件とフォールバック、承認閾値、責任制限、損害賠償の方向性、知的財産権の帰属、解除権。*

> スキルがこのプレイブックに基づいて契約書をレビューまたは評価する際、まず自社がどちら側かを判定します（通常、どちらのひな形かで明らかです）。不明な場合は確認します。該当するプレイブックセクションを読みます。販売側のポジションを購買側の契約に適用したり、その逆を行うことはありません。

### 購買側プレイブック

*自社が購入者（発注者）の場合に適用。通常、相手方のひな形。*

*[未設定 --- `/commercial-legal-jp:cold-start-interview --side purchasing` を実行して構築]*

#### 責任制限

**直接損害の上限（対価との倍率）:** [PLACEHOLDER --- 例：「過去12ヶ月の委託料相当額」]

**間接損害・特別損害（民法第416条第2項）:** [PLACEHOLDER --- 排除/上限あり/上限なし/直接損害と同額]

**上限の例外とする事由:** [PLACEHOLDER --- 例：「故意・重過失、秘密保持義務違反、知的財産権侵害、個人情報漏洩」]

**上限の算定基礎:** [PLACEHOLDER --- 例：「請求原因発生前12ヶ月間に支払済みの委託料」]

**許容可能なフォールバック:**
- [PLACEHOLDER]

**絶対に受け入れない:**
- [PLACEHOLDER]

#### 損害賠償

**標準ポジション:** [PLACEHOLDER --- 債務不履行に基づく損害賠償の範囲、不法行為との関係]

**許容可能なフォールバック:**
- [PLACEHOLDER]

**絶対に受け入れない:**
- [PLACEHOLDER]

#### 契約不適合責任

**標準ポジション:** [PLACEHOLDER --- 修補請求、代金減額請求、損害賠償請求、解除の範囲]

**通知期間:** [PLACEHOLDER --- 例：「検収後1年以内」]

**許容可能なフォールバック:**
- [PLACEHOLDER]

#### 秘密保持

**標準ポジション:** [PLACEHOLDER --- 秘密情報の定義、開示範囲、期間]

**存続期間:** [PLACEHOLDER --- 例：「契約終了後3年間」]

**許容可能なフォールバック:**
- [PLACEHOLDER]

#### 解除

**標準ポジション:** [PLACEHOLDER --- 例：「催告解除（相当期間経過後）、無催告解除事由の列挙」]

**許容可能なフォールバック:**
- [PLACEHOLDER]

**絶対に受け入れない:**
- [PLACEHOLDER]

#### 準拠法・管轄

**希望:** [PLACEHOLDER --- 例：「日本法、東京地方裁判所」]
**許容:** [PLACEHOLDER --- 例：「大阪地方裁判所」]
**エスカレーション:** [PLACEHOLDER --- 例：「仲裁条項（JCAA）」]
**不可:** [PLACEHOLDER --- 例：「外国法準拠、外国裁判所の専属管轄」]

#### 反社会的勢力排除条項

**標準ポジション:** [PLACEHOLDER --- 自社ひな形の有無、三要素（表明保証・誓約・解除）の充足]

#### 下請法コンプライアンス

**適用有無:** [PLACEHOLDER --- 資本金区分に基づく判定結果]
**体制:** [PLACEHOLDER --- 3条書面の発行体制、60日ルールの管理方法、5条書類の保存]

#### 絶対に譲れない条項

[PLACEHOLDER --- 購買側で絶対に譲れない一つの条項。すべての購買側レビューで最初にチェックされます。]

---

### 販売側プレイブック

*自社が販売者（受注者）の場合に適用。通常、自社のひな形。*

*[未設定 --- `/commercial-legal-jp:cold-start-interview --side sales` を実行して構築]*

#### 責任制限

**直接損害の上限（対価との倍率）:** [PLACEHOLDER --- 例：「当該契約に基づき受領した委託料の総額」]

**間接損害・特別損害（民法第416条第2項）:** [PLACEHOLDER --- 排除/上限あり/上限なし]

**上限の例外とする事由:** [PLACEHOLDER]

**上限の算定基礎:** [PLACEHOLDER]

**許容可能なフォールバック:**
- [PLACEHOLDER]

**絶対に受け入れない:**
- [PLACEHOLDER]

#### 損害賠償

**標準ポジション:** [PLACEHOLDER]

**許容可能なフォールバック:**
- [PLACEHOLDER]

**絶対に受け入れない:**
- [PLACEHOLDER]

#### 契約不適合責任

**標準ポジション:** [PLACEHOLDER]

**通知期間:** [PLACEHOLDER]

**許容可能なフォールバック:**
- [PLACEHOLDER]

#### 秘密保持

**標準ポジション:** [PLACEHOLDER]

**存続期間:** [PLACEHOLDER]

**許容可能なフォールバック:**
- [PLACEHOLDER]

#### 解除

**標準ポジション:** [PLACEHOLDER]

**許容可能なフォールバック:**
- [PLACEHOLDER]

**絶対に受け入れない:**
- [PLACEHOLDER]

#### 準拠法・管轄

**希望:** [PLACEHOLDER]
**許容:** [PLACEHOLDER]
**エスカレーション:** [PLACEHOLDER]
**不可:** [PLACEHOLDER]

#### 反社会的勢力排除条項

**標準ポジション:** [PLACEHOLDER]

#### 下請法コンプライアンス

**適用有無:** [PLACEHOLDER]
**体制:** [PLACEHOLDER]

#### 絶対に譲れない条項

[PLACEHOLDER --- 販売側で絶対に譲れない一つの条項。すべての販売側レビューで最初にチェックされます。]

---

## エスカレーション

| 承認者 | 単独決裁可能範囲 | エスカレーション先 | 方法 |
|---|---|---|---|
| 法務担当者 | [PLACEHOLDER --- 閾値] | 法務部長 | [PLACEHOLDER --- Slack/メール/稟議システム] |
| 法務部長 | [PLACEHOLDER --- 閾値] | 取締役 | [PLACEHOLDER] |
| 取締役 | [PLACEHOLDER --- 閾値] | 代表取締役 | [PLACEHOLDER] |

**金額基準（稟議制度）:** [PLACEHOLDER --- 決裁権限規程に基づく金額基準]

**金額にかかわらず自動エスカレーションとなる事項:**
- [PLACEHOLDER --- 例：「責任制限の上限撤廃、知的財産権の譲渡、反社排除条項の削除、外国法準拠」]

**印鑑管理:**
- 代表者印使用基準: [PLACEHOLDER]
- 角印使用基準: [PLACEHOLDER]

---

## 出力設定

**秘密保持マーキング**（本プラグインが生成するすべての分析、メモ、レビュー、評価の冒頭に付記）：

- 役割が弁護士の場合: `秘密 — 弁護士業務成果物 — 弁護士の指示に基づき作成`
- 役割が法務部員（弁護士資格なし）の場合: `調査ノート — 法的助言ではありません — 行動する前に弁護士に相談してください`
- 役割がその他の場合: `調査ノート — 法的助言ではありません — 行動する前に資格を有する弁護士に相談してください`

**日本法における注意事項:** 日本には米国のattorney work product doctrineに直接対応する制度はありません。弁護士・依頼者間秘匿特権（attorney-client privilege）も日本法上は限定的です。秘密保持マーキングは契約上の秘密保持義務および社内情報管理規程に基づく保護を目的としています。

**出力言語:** [PLACEHOLDER --- 日本語/英語/状況に応じて切替]

**NDA簡易レビューのクロージングアクション:** [PLACEHOLDER --- 例：「この出力とNDAを法務部長に転送する」]

---

## レビュー設定

confirm_routing: true   # falseに設定するとルーティング確認をスキップして自動的に進行

---

## 種子文書レビュー履歴

*コールドスタートインタビューで入力されます。上記プレイブックの学習元となった契約書です。*

| 契約書 | 相手方 | 締結日 | 特記事項 |
|---|---|---|---|
| [PLACEHOLDER] | | | |

---

*インタビューを再実行するには: `/commercial-legal-jp:cold-start-interview --redo`*

<!--
CONFIGURATION LOCATION

User-specific configuration for this plugin lives at a version-independent path that survives plugin updates:

  ~/.claude/plugins/config/claude-for-legal/employment-legal-jp/CLAUDE.md

Rules for every skill, command, and agent in this plugin:
1. READ configuration from that path. Not from this file.
2. If that file does not exist or still contains [PLACEHOLDER] markers, STOP before doing substantive work. Say: "このプラグインは利用前にセットアップが必要です。`/employment-legal-jp:cold-start-interview` を実行してください（10〜15分程度）。セットアップなしでは汎用的な出力しかできず、貴社の実務に合わない可能性があります。" Do NOT proceed with placeholder or default configuration. The only skills that run without setup are /employment-legal-jp:cold-start-interview itself and any --check-integrations flag.
3. Setup and cold-start-interview WRITE to that path, creating parent directories as needed.
4. On first run after a plugin update, if a populated CLAUDE.md exists at the old cache path
   (~/.claude/plugins/cache/claude-for-legal/employment-legal-jp/<version>/CLAUDE.md for any version)
   but not at the config path, copy it forward to the config path before proceeding.
5. This file (the one you are reading) is the TEMPLATE. It ships with the plugin and shows the
   structure the config should have. It is replaced on every plugin update. Never write user data here.

**Shared company profile.** Company-level facts (who you are, what you do, where you operate, your risk posture, key people) live in `~/.claude/plugins/config/claude-for-legal/company-profile.md` — one level above this file, shared by all plugins. Read it before this plugin's practice profile. If it doesn't exist, this plugin's setup will create it.
-->

# 労働法務プラクティスプロファイル
*cold-start-interviewにより [DATE] に作成。`[PLACEHOLDER]` が残っている場合は `/employment-legal-jp:cold-start-interview` を実行してください。*

---

## 組織情報

**会社名:** [PLACEHOLDER]
**業種:** [PLACEHOLDER]
**従業員数:** [PLACEHOLDER — 10人以上の場合は就業規則の作成・届出義務あり（労基法第89条）]
**事業場数:** [PLACEHOLDER — 事業場ごとに就業規則の届出が必要]
**本社所在地:** [PLACEHOLDER]
**主たる事業場の管轄労基署:** [PLACEHOLDER]

*(会社名・業種は company-profile.md から読み込み — 全プラグイン共通。従業員数・事業場数はプラグイン固有。)*

---

## 利用者情報

**役割:** [PLACEHOLDER — 弁護士 / 社会保険労務士 / 法務部員 / 人事部員 / その他]
**顧問弁護士:** [PLACEHOLDER — 事務所名 / 担当者名 / なし]
**顧問社労士:** [PLACEHOLDER — 事務所名 / 担当者名 / なし]

*スキルはこのセクションを読み、出力ヘッダーの選択と弁護士確認ゲートの判定を行う。*

---

**クライアント向け・経営向け成果物のクワイエットモード。** 外部または非法務の読者が読む成果物（取締役会報告書、従業員向け通知、官公署への届出書類、ステークホルダー向け要約）では内部的な説明を抑制する:
- 業務成果物ヘッダー: 維持
- レビュアーノート: 維持
- 出典タグ: 維持（脚注または巻末注としてまとめてよい）
- スキル説明（「このスキルは...」）: 削除
- プラグインコマンドへの誘導（「次に /plugin:other-command を...」）: 成果物から削除し、別のレビュアーノートへ
- 「以下のファイルを読みました...」: 削除

成果物はパートナーが書いたように読めるべきである。メタコメントはヘッダー上のレビュアーノートまたは別メッセージに記載する。

## 連携ツール

| 連携先 | ステータス | 未接続時のフォールバック |
|---|---|---|
| HRIS (SmartHR / freee人事労務 / KING OF TIME / ジョブカン / その他) | [✓ / ✗] | 休暇データは `~/.claude/plugins/config/claude-for-legal/employment-legal-jp/leave-register.yaml` で手動管理; `/employment-legal-jp:log-leave` で入力 |
| 勤怠管理 (KING OF TIME / ジョブカン / freee / Touch On Time) | [✓ / ✗] | 労働時間データは手動入力 |
| 給与計算 (freee / マネーフォワード / 弥生 / PCA) | [✓ / ✗] | 給与情報は手動入力 |
| ドキュメントストレージ (Google Drive / SharePoint / Box) | [✓ / ✗] | ローカルパスから就業規則等を読み込み |
| Slack | [✓ / ✗] | レビュー結果はファイル出力のみ |

*再チェック: `/employment-legal-jp:cold-start-interview --check-integrations`*

---

## 出力設定

**業務成果物ヘッダー**（本プラグインが生成するすべての分析、メモ、レビュー、ドラフトに付与）:

- 役割が**弁護士**の場合: `秘密特権 — 弁護士業務成果物 — 弁護士の指示に基づき作成`
- 役割が**社会保険労務士**の場合: `秘密 — 社労士業務成果物 — 社会保険労務士の指示に基づき作成`
- 役割が**法務部員・人事部員・その他**の場合: `調査ノート — 法的助言ではありません — 行動する前に弁護士または社会保険労務士にご確認ください`

---

**レビュアーノート — 成果物の直上に1ブロック。** レビュアーが出力を信頼する前に知るべきことをすべてここにまとめる:

> **レビュアーノート**
> - **出典:** [リサーチツール接続済 / 未接続 — トレーニング知識からの引用、利用前に確認必要]
> - **読み込み範囲:** [全文 / ページ1-50/200 / N件 / N/A]
> - **要判断フラグ:** [N件 `[要確認]` インライン / なし]
> - **最新性:** [date以降の動向を検索 — 該当なし / N件の更新あり / 検索不可、要確認]
> - **利用前に:** [レビュアーが行うべき1-2点 — または問題なければ「確認可」]

---

**次のステップ決定ツリー。** 分析後に選択肢を提示する:

> **次のステップを選んでください:**
> 1. **[ドラフトを作成]** — [メモ / 通知書 / 合意書 / エスカレーションノート] の初稿を作成
> 2. **エスカレーション** — [エスカレーション先] への報告書を作成
> 3. **追加情報の取得** — 助言前に確認したい [2-3の論点] を質問として作成
> 4. **経過観察** — [トラッカー / 監視リスト] に追加し、再確認時期を記録
> 5. **その他** — ご希望をお知らせください

---

## 労務管理体制

### 就業規則の整備状況

**就業規則の有無:** [PLACEHOLDER — あり / なし / 作成中]
**最終更新日:** [PLACEHOLDER]
**届出先労基署:** [PLACEHOLDER]
**意見聴取の実施:** [PLACEHOLDER — 労働組合 / 過半数代表者]
**主な記載事項の充足度:** [PLACEHOLDER — 未監査 / 監査済み(日付)]

### 36協定の締結・届出状況

**36協定の有無:** [PLACEHOLDER — 締結済み / 未締結]
**有効期間:** [PLACEHOLDER]
**特別条項の有無:** [PLACEHOLDER — あり(上限時間) / なし]
**届出状況:** [PLACEHOLDER — 届出済み / 未届出]
**時間外労働の上限規制対応:** [PLACEHOLDER — 対応済み / 未対応 / 適用猶予業種]

### 労働組合・過半数代表者

**労働組合の有無:** [PLACEHOLDER — あり(組合名・組織率) / なし]
**過半数代表者の選出:** [PLACEHOLDER — 選出済み(選出方法) / 未選出]

### ハラスメント相談窓口

**相談窓口の設置:** [PLACEHOLDER — 設置済み(内部 / 外部 / 両方) / 未設置]
**担当者:** [PLACEHOLDER]
**研修の実施状況:** [PLACEHOLDER — 定期実施(頻度) / 未実施]

### 公益通報窓口

**内部通報窓口の設置:** [PLACEHOLDER — 設置済み / 未設置 — 従業員300人超は義務]
**外部通報窓口の設置:** [PLACEHOLDER — 設置済み / 未設置]
**公益通報者保護規程の整備:** [PLACEHOLDER — 整備済み / 未整備]

---

## エスカレーション

| 事案 | 一次対応 | エスカレーション先 | タイミング |
|---|---|---|---|
| 日常的な労務相談 | 人事担当者 | 人事部長 | 判断に迷う場合 |
| 解雇・退職勧奨 | 人事部長 | 法務部 / 顧問弁護士 | 高リスクフラグがある場合 |
| 整理解雇 | — | 法務部 + 顧問弁護士 | 常に |
| 労働審判・訴訟 | — | 取締役 + 顧問弁護士 | 常に |
| ハラスメント申告 | 相談窓口 | 人事部長 → 法務部 | 重大案件 |
| 労基署の調査・是正勧告 | — | 代表取締役 + 顧問社労士 | 常に |
| 労災事故 | 人事担当者 | 人事部長 → 顧問社労士 | 休業を伴う場合 |

---

## 雇用形態

**正社員:** [PLACEHOLDER — 人数]
**契約社員（有期雇用）:** [PLACEHOLDER — 人数、更新回数の上限]
**パートタイマー・アルバイト:** [PLACEHOLDER — 人数]
**派遣社員:** [PLACEHOLDER — 人数、派遣元]
**業務委託:** [PLACEHOLDER — 人数、偽装請負リスクの有無]

---

## 変形労働時間制・裁量労働制

**採用している制度:** [PLACEHOLDER — 1ヶ月単位変形 / 1年単位変形 / フレックスタイム / 専門業務型裁量労働 / 企画業務型裁量労働 / 高度プロフェッショナル / なし]
**労使協定の届出状況:** [PLACEHOLDER]
**対象労働者:** [PLACEHOLDER]

---

## 外国人労働者

**外国人労働者の有無:** [PLACEHOLDER — あり(人数・在留資格の種類) / なし]
**在留資格管理:** [PLACEHOLDER — 管理体制の有無]
**届出状況:** [PLACEHOLDER — 外国人雇用状況届出の実施有無]

---

## 社会保険・労働保険

**社会保険の適用状況:** [PLACEHOLDER — 適用事業所 / 任意適用]
**労働保険の加入状況:** [PLACEHOLDER — 加入済み / 一部未加入]
**特別加入の有無:** [PLACEHOLDER — 労災保険特別加入の有無]

---

## シード文書

| 文書 | 場所 | 日付 | 備考 |
|---|---|---|---|
| 就業規則 | [PLACEHOLDER] | | |
| 賃金規程 | [PLACEHOLDER] | | |
| 36協定 | [PLACEHOLDER] | | |
| 退職金規程 | [PLACEHOLDER] | | |
| ハラスメント防止規程 | [PLACEHOLDER] | | |
| 育児介護休業規程 | [PLACEHOLDER] | | |

---

## 判断基準

主観的な法的判断 — 解雇が有効か、退職勧奨が違法か、懲戒処分が相当か — で判断が不確実な場合、スキルは**回復可能なエラーを優先する**: 該当行に `[要確認]` をインラインでフラグし、不確実性を記載する。フラグ不足は片道切符、フラグ過多は弁護士が30秒で閉じる両道切符。両道切符をデフォルトとする。

---

## ソース帰属

- `[判例検索]` — 判例データベースから取得した場合のみ
- `[法令]` — e-Gov法令検索等の公的情報源から取得した場合のみ
- `[ユーザー提供]` — ユーザーが提示した情報
- `[モデル知識 — 要確認]` — 上記以外すべて（デフォルト）
- `[確認済み — 最終確認日 YYYY-MM-DD]` — 一次情報源で確認済みの安定した法令参照

---

## 管轄の認識

本プラグインは日本の労働法を前提とする。労働基準法、労働契約法、労働安全衛生法、男女雇用機会均等法、育児介護休業法、パートタイム・有期雇用労働法、労働者派遣法等の日本の法令に基づいて分析を行う。海外拠点の労働法は対象外 — `/employment-legal-jp:expansion-kickoff` を利用すること。

---

*再実行: `/employment-legal-jp:cold-start-interview --redo`*

---
name: session
description: >
  科目別のN問学習セッション — 短答式、論文式、またはフラッシュカード。
  成績を追跡し学習計画を更新。「民法10問やって」「セッション」
  「5問ドリル」等で起動。
argument-hint: "<科目> <n> [--短答 | --論文 | --flashcards]"
---

# /session

1. `$ARGUMENTS` を解析する — 科目とN。不足している場合は確認する：
   > 科目と問題数を指定してください（例：`民法 10` または `刑法 5 --論文`）。
2. `~/.claude/plugins/config/claude-for-legal/law-student-jp/CLAUDE.md` を読み込む → 受験予定試験（司法試験/予備試験）、苦手科目、学習スタイル。
3. `~/.claude/plugins/config/claude-for-legal/law-student-jp/study-plan.yaml` が存在すれば読み込む。`session_history` からこの科目の過去成績を取得し、弱い論点に重み付けする。
4. 方式フラグによりルーティングする：
   - `--短答`（試験科目のデフォルト）：`bar-prep-questions` スキルを読み込み、N問の短答式問題を実施する。試験種別（司法試験/予備試験）に応じた科目・形式を適用する。
   - `--論文`：`bar-prep-questions` の論文式モードを読み込み、N問の論文式問題を実施する。採点実感に基づくフィードバックを適用する。
   - `--flashcards`：`flashcards` スキルを読み込み、N枚のカードを `--drill` モードで実施する。
5. N問を一問ずつ出題する。各問の解答後、正解・不正解の理由を解説する。不確実なルールには `[要確認]` をインラインで付記する。
6. セッション終了時に結果を書き込む：
   - `study-plan.yaml` が存在する場合：`session_history` に追記する（`study-plan` スキルのスキーマに従う）。
   - 存在しない場合：`~/.claude/plugins/config/claude-for-legal/law-student-jp/session-history.yaml` に書き込む。
7. 報告：
   - 得点：X/N（正答率%）
   - 誤答：論点タグ付きリスト
   - 今回のセッションの弱点論点
   - 過去セッションとのパターン比較（同科目の履歴が2回以上ある場合）
   - 学習計画が次に推奨する内容

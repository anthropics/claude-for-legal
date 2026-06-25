---
name: matter-intake
description: >
  案件受付 — 新規案件の統一的なインテーク。識別情報、利益相反チェック、リスクトリアージ、
  外部弁護士、証拠保全、主要期日を収集し、matter.mdとhistory.mdを作成、_log.yamlに行を追加。
  「新しい案件」「案件を受け付けたい」と言われたときに使用。
argument-hint: "[案件名]"
---

# /matter-intake

1. `~/.claude/plugins/config/claude-for-legal/litigation-legal-jp/CLAUDE.md` → リスク評価、実務環境を読み込み。
2. 以下のワークフローに従う。
3. 統一インテークを実行。
4. スラグを生成（案件名のローマ字表記 + 年）。
5. `~/.claude/plugins/config/claude-for-legal/litigation-legal-jp/matters/[slug]/matter.md` を作成。
6. `~/.claude/plugins/config/claude-for-legal/litigation-legal-jp/matters/[slug]/history.md` を作成。
7. `~/.claude/plugins/config/claude-for-legal/litigation-legal-jp/matters/_log.yaml` に行を追加。

---

# 案件受付

## インテーク項目

### 1. 識別情報
- 案件名
- 相手方
- 案件類型: `契約 | 労働 | 知的財産 | 不法行為 | 行政 | その他`
- 当社の立場: `原告 | 被告 | 申立人 | 相手方 | 被調査者`
- 管轄裁判所

### 2. 利益相反チェック
- 相手方との既存の取引関係の確認
- 反社会的勢力に該当しないことの確認

### 3. リスクトリアージ
- 請求額 / 被害額
- 重大度 × 可能性マトリクスでの位置づけ
- 非金銭的リスク（差止め、レピュテーション等）

### 4. 外部弁護士
- 外部弁護士の要否
- 推奨事務所（常用外部弁護士リストから）
- 報酬体系の確認

### 5. 証拠保全
- 証拠保全の要否
- 対象文書・データの特定

### 6. 主要期日
- 訴状送達日 / 催告書受領日
- 答弁書提出期限
- 第1回口頭弁論期日
- 時効期限

## 免責事項

> **免責事項:** 本出力はAIによる分析支援であり、法的助言ではありません。

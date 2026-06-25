---
name: portfolio-status
description: >
  ポートフォリオ管理 — _log.yamlからポートフォリオをロールアップし、リスク分布、
  直近の期日、停滞案件、ステージ分布を表示する。「案件の状況は」「ポートフォリオを確認」
  と言われたときに使用。
argument-hint: "[--all | --risk=high | --stale]"
---

# /portfolio-status

1. `~/.claude/plugins/config/claude-for-legal/litigation-legal-jp/CLAUDE.md` → リスク評価を読み込み。
2. `~/.claude/plugins/config/claude-for-legal/litigation-legal-jp/matters/_log.yaml` を読み込み。
3. ロールアップを生成。

---

# ポートフォリオ管理

## 目的

「今何を抱えていて、何に注意が必要で、何が停滞しているか」を1回の読み取りで把握する。

## ロールアップ項目

- リスク分布（対応必須/重要/要確認/低リスクの件数）
- 直近14/30/60日の期日
- 30日以上更新のない案件
- ステージ分布（訴訟前/係属中/和解交渉中/控訴審/終結）
- 外部弁護士未アサインの重要案件

## 免責事項

> **免責事項:** 本出力はAIによる分析支援であり、法的助言ではありません。

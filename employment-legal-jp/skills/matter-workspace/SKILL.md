---
name: matter-workspace
description: >
  案件ワークスペースの管理 — 新規作成、一覧表示、切替、クローズ、解除。
  複数クライアントの案件コンテキストを分離し、情報の漏洩を防止する。
  社労士事務所・法律事務所向け。企業内人事部門ではオフ。
argument-hint: "<new | list | switch | close | none> [slug]"
---

# /matter-workspace

1. Load `~/.claude/plugins/config/claude-for-legal/employment-legal-jp/CLAUDE.md` → Matter workspaces の設定確認。
2. Dispatch on subcommand.

---

## 目的

社労士事務所や法律事務所など、複数のクライアントの案件を扱う場合に、案件ごとのコンテキストを分離する。企業内の人事部門（単一クライアント）ではこの機能はオフとなり、プラクティスレベルのコンテキストが自動的に使用される。

## ワークフロー

### ステップ1: 設定確認

`~/.claude/plugins/config/claude-for-legal/employment-legal-jp/CLAUDE.md` の `## Matter workspaces` セクションを確認する。`Enabled` が `✗` の場合:

> 案件ワークスペースはオフです — 企業内利用（単一クライアント）として設定されているため、プラクティスレベルのコンテキストが自動的に使用されます。複数のクライアントを扱う場合は `/employment-legal-jp:cold-start-interview --redo` を実行して設定を変更してください。

### ステップ2: サブコマンドの実行

#### `new <slug>` — 新規案件ワークスペースの作成

以下のインテークを1つのプロンプトで実施する:

> 案件ワークスペースを作成します:
>
> - **クライアント名** — 代理するクライアント
> - **案件の種類** — 解雇 / 調査 / 休職 / 採用 / 労働者性判断 / 就業規則 / 海外展開 / その他
> - **案件の概要** — 2〜5文で案件の内容
> - **秘密保持レベル** — 通常 / 厳格（他案件との情報共有を制限）
> - **案件固有の事情** — プラクティスレベルの設定と異なる点

作成後、`~/.claude/plugins/config/claude-for-legal/employment-legal-jp/matters/<slug>/` に以下を作成:
- `matter.md` — 案件情報
- `history.md` — 経過記録
- `notes.md` — 作業メモ

#### `list` — 案件一覧の表示

```markdown
| Slug | クライアント | 種類 | ステータス | 作成日 | アクティブ |
|---|---|---|---|---|---|
| [slug] | [名前] | [種類] | [active/archived] | [日付] | [* / ] |
```

#### `switch <slug>` — アクティブ案件の切替

1. `matters/<slug>/matter.md` の存在を確認
2. プラクティスレベルCLAUDE.mdの `Active matter:` を更新
3. 案件概要を表示して確認

#### `close <slug>` — 案件のアーカイブ

1. `matters/<slug>/history.md` にクローズの記録を追加
2. `matters/<slug>/` → `matters/_archived/<slug>/` に移動
3. アクティブ案件だった場合は解除

#### `none` — 案件の解除

`Active matter:` を `none — プラクティスレベルのコンテキストのみ` に設定。

---

## 出力

サブコマンドの実行結果を表示し、変更内容を確認する。

---

## このスキルがやらないこと

- コンフリクトチェックを行うこと。利益相反の確認は利用者の責任。
- 案件データを削除すること。クローズはアーカイブであり、削除ではない。
- 案件間の情報共有を自動的に行うこと。クロスマターコンテキストがオフの場合は厳格に分離。

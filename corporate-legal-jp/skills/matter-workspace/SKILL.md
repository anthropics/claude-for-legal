---
name: matter-workspace
description: >
  案件ワークスペースの管理。案件の作成・一覧・切替・クローズを行い、
  法律事務所等の複数クライアント環境で案件ごとのコンテキストを分離する。
  「新規案件」「案件切替」「案件一覧」「案件クローズ」等で起動。
argument-hint: "<new | list | switch | close | none> [slug]"
---

# /matter-workspace（案件ワークスペース）

複数クライアント・複数案件を扱う実務者向け。案件ワークスペースにより、あるクライアント・案件のコンテキストを他のすべてから分離する。

インハウス法務（一社のみ）の場合、この機能はオフであり、すべてのスキルはプラクティスレベルのコンテキストを使用する。

---

## コンテキストの読み込み

- `~/.claude/plugins/config/claude-for-legal/corporate-legal-jp/CLAUDE.md` → 案件ワークスペースの設定

---

## サブコマンド

### `/corporate-legal-jp:matter-workspace new <slug>`

新規案件ワークスペースを作成。

> 以下の情報をお知らせください:
> 1. **案件名/コード:** [例: project-falcon]
> 2. **クライアント名:**
> 3. **案件の種類:** [M&A / 組織再編 / 取締役会案件 / エンティティ管理 / その他]
> 4. **主担当弁護士:**

案件フォルダを `~/.claude/plugins/config/claude-for-legal/corporate-legal-jp/matters/<slug>/` に作成。
`matter.md` にメタデータを記録。

### `/corporate-legal-jp:matter-workspace list`

案件一覧をステータスとアクティブフラグ付きで表示。

```
案件ワークスペース一覧:

  * project-falcon  [アクティブ]  M&A — [クライアント名]
    project-eagle   [進行中]      組織再編 — [クライアント名]
    project-hawk    [アーカイブ]  M&A — [クライアント名]
```

### `/corporate-legal-jp:matter-workspace switch <slug>`

アクティブ案件を切替。以降のスキルはこの案件のコンテキストで動作。

### `/corporate-legal-jp:matter-workspace close <slug>`

案件をアーカイブ。案件フォルダは残るが、アクティブ案件として選択されなくなる。

### `/corporate-legal-jp:matter-workspace none`

アクティブ案件を解除し、プラクティスレベルで作業。

---

## クロスマター制約

クロスマターコンテキストがオフ（デフォルト）の場合、案件Aで作業中に案件Bのファイルは読み込まない。案件をまたぐ知見はプラクティスレベルの`CLAUDE.md`に記録。

---

## このスキルが行わないこと

- 案件の利益相反チェック — コンフリクトチェックシステムの領域
- タイムエントリの管理 — 時間管理システムの領域
- 案件の請求管理 — 経理・ビリングシステムの領域

---
name: matter-workspace
description: 案件ワークスペースの管理 — 作成、一覧、切替、クローズ、またはアクティブ案件の解除（プラクティスレベル）。複数のクライアントや案件を扱い、ある案件のコンテキストを他の案件から分離する必要がある場合に使用。
argument-hint: "<new | list | switch | close | none> [slug]"
---

# /matter-workspace

複数のクライアントと案件にわたって業務を行う実務者向けです。案件ワークスペースは、あるクライアント・案件のコンテキストを他のすべてから分離します。

## サブコマンド

- `/regulatory-legal-jp:matter-workspace new <slug>` — 新しい案件ワークスペースを作成、短いインテークを実施、`matter.md` を書き込み
- `/regulatory-legal-jp:matter-workspace list` — 案件をステータスとアクティブフラグ付きでリスト表示
- `/regulatory-legal-jp:matter-workspace switch <slug>` — アクティブ案件を設定
- `/regulatory-legal-jp:matter-workspace close <slug>` — 案件をアーカイブ（`_archived/` に移動、削除しない）
- `/regulatory-legal-jp:matter-workspace none` — アクティブ案件を解除、プラクティスレベルのみで作業

## 手順

1. `~/.claude/plugins/config/claude-for-legal/regulatory-legal-jp/CLAUDE.md` → `## 案件ワークスペース` セクションを確認。`有効` が `✗` の場合：「案件ワークスペースはオフです — 企業内法務として1社のクライアントに設定されているため、プラクティスレベルのコンテキストを自動的に使用します。複数のクライアントにわたって業務を行う場合は、`/regulatory-legal-jp:cold-start-interview --redo` を再実行し、法律事務所の設定を選択してください。」
2. `$ARGUMENTS` の最初のトークンでディスパッチ：
   - `new` → インテークインタビューを実施、`~/.claude/plugins/config/claude-for-legal/regulatory-legal-jp/matters/<slug>/matter.md` を書き込み、`history.md` と `notes.md` を初期化。
   - `list` → `~/.claude/plugins/config/claude-for-legal/regulatory-legal-jp/matters/*/matter.md` を列挙、テーブルで表示、アクティブ案件をマーク。
   - `switch` → プラクティスレベルCLAUDE.mdの `アクティブ案件:` 行を更新。
   - `close` → `~/.claude/plugins/config/claude-for-legal/regulatory-legal-jp/matters/<slug>/` を `_archived/<slug>/` に移動、`history.md` にクローズ日を記録。
   - `none` → `アクティブ案件:` を `なし — プラクティスレベルコンテキストのみ` に設定。
3. 変更内容をユーザーに表示し、書き込み前に確認。

## 注意事項

- `案件間コンテキスト` がオフ（デフォルト）の場合、案件Aで作業中にスキルが案件Bのファイルを読むことはない。
- アーカイブは削除ではない — クローズされた案件は保存目的で読み取り可能。
- slugは小文字、ハイフン区切り。

## 弁護士確認ゲート

案件ワークスペースの管理自体には弁護士確認ゲートは不要です。

## 免責事項

案件管理は組織のツールであり、法的助言ではありません。

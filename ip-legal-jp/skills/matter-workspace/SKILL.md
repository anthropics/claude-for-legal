---
name: matter-workspace
description: >
  案件ワークスペースの管理 — 作成、一覧、切替、クローズ、切断。
  複数クライアントの法律事務所・特許事務所で、クライアント間のコンテキストを
  分離するために使用する。企業内知財部では通常不要。
argument-hint: "<new | list | switch | close | none> [slug]"
---

# /matter-workspace

法律事務所・特許事務所では複数のクライアント・案件を扱う。案件ワークスペースは、各クライアントのコンテキストを分離する。

## サブコマンド

- `/ip-legal-jp:matter-workspace new <slug>` — 新規案件ワークスペースを作成
- `/ip-legal-jp:matter-workspace list` — 案件一覧を表示
- `/ip-legal-jp:matter-workspace switch <slug>` — アクティブ案件を切替
- `/ip-legal-jp:matter-workspace close <slug>` — 案件をアーカイブ（削除ではない）
- `/ip-legal-jp:matter-workspace none` — 案件から切断、プラクティスレベルで作業

## 手順

1. `~/.claude/plugins/config/claude-for-legal/ip-legal-jp/CLAUDE.md` の `## 案件ワークスペース` を確認する。`有効` が `✗` の場合: 「案件ワークスペースはオフです。企業内知財部の設定では、プラクティスレベルのコンテキストが自動的に使用されます。複数クライアントを扱う場合は、`/ip-legal-jp:cold-start-interview --redo` を実行し、法律事務所・特許事務所の設定を選択してください。」
2. サブコマンドに応じて処理を実行する。
3. 変更内容を表示し、書き込み前に確認する。

## 注意事項

- 案件間のコンテキスト読み取りは、`案件間コンテキスト` が `オン` の場合のみ許可。
- アーカイブは削除ではない — 保全・利益相反確認のため閲覧可能な状態を維持。
- スラッグは小文字・ハイフン区切り。

## 免責事項

本スキルの出力は法的助言ではありません。

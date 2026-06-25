---
name: review
description: >
  契約書をレビューする。文書タイプを検出し、適切なレビュースキル（vendor-agreement-review、
  nda-review、saas-msa-review）にルーティングする。「この契約書をレビューして」
  「このNDAを確認して」「業務委託契約書を見て」等のトリガーで起動。
argument-hint: "[ファイルパス | Driveリンク | CLM ID | テキスト貼付]"
---

# /review

`~/.claude/plugins/config/claude-for-legal/commercial-legal-jp/CLAUDE.md` のプレイブックに基づいて受領した契約書をレビューします。文書構造からタイトルを識別し、適切なスキルを選択し、confirm_routing が有効な場合はユーザーに確認してから実行します。

## 手順

1. **`~/.claude/plugins/config/claude-for-legal/commercial-legal-jp/CLAUDE.md` を読み込む。** プレースホルダーが存在する場合は停止し、「まず `/commercial-legal-jp:cold-start-interview` を実行してください --- プレイブックを学ばないとレビューできません。」と表示する。

   `## レビュー設定` → `confirm_routing` も読み込む。フィールドが存在しない場合は `true` として扱う。

2. **契約書を取得:** ファイルパス、Driveリンク、CLM ID、または貼り付けテキストから。未提供の場合は要求する。

3. **文書構造を読み取る --- まずタイトルから。**

   本文を読む前に以下を抽出：
   - メインの契約書タイトル（例：「業務委託基本契約書」「秘密保持契約書」）
   - すべての別紙、付属書、覚書のタイトル

   これがルーティングシグナル。本文のキーワードだけに頼らない。

4. **文書構造に基づいてスキルを選択する。**

   識別された文書またはセクションをスキルにマッピング：

   | 文書/セクションのタイトル | スキル |
   |---|---|
   | 秘密保持契約書、NDA、機密保持契約書（メイン契約として） | **nda-review** |
   | 業務委託契約書、業務委託基本契約書、コンサルティング契約書、準委任契約書 | **gyoumu-itaku-review** |
   | 基本契約書、取引基本契約書、売買基本契約書 | **vendor-agreement-review** |
   | SaaS利用契約書、クラウドサービス利用契約書、サブスクリプション契約書、ソフトウェアライセンス契約書（サブスクリプション型） | **saas-msa-review** |
   | 売買契約書、物品購入契約書 | **vendor-agreement-review** |
   | ライセンス契約書、使用許諾契約書 | **vendor-agreement-review** |
   | 個人情報取扱委託契約書、データ処理契約書（別紙またはスタンドアロン） | **vendor-agreement-review** → データ保護セクションへの注記 |
   | SLA、サービスレベル契約書（別紙として） | **saas-msa-review** → SLAセクションへの注記 |

   複数のスキルが適用される場合がある。一般的な組み合わせ：
   - 基本契約書 + 個別契約書 → vendor-agreement-review
   - SaaS利用契約書 + 申込書 + SLA別紙 → saas-msa-review（すべてカバー）
   - 業務委託契約書 + 秘密保持条項 → gyoumu-itaku-review（NDA条項を含む）

   タイトルを読んでも本当に曖昧な場合（例：「契約書」とだけ記載され別紙なし）、本文の最初の2ページを読んで判断する。

5. **下請法の適用チェック。**

   `~/.claude/plugins/config/claude-for-legal/commercial-legal-jp/CLAUDE.md` の資本金情報と契約相手方の資本金を照合し、下請法の適用可能性を判定する。

   適用の可能性がある場合：
   - ルーティング確認に `shitauke-ho-check` を追加
   - 「この取引は下請法の適用対象となる可能性があります。下請法チェックも実行しますか？」と確認

   資本金区分の判定基準：
   - 製造委託・修理委託：親事業者 3億円超 → 下請事業者 3億円以下、または親事業者 1千万円超3億円以下 → 下請事業者 1千万円以下
   - 情報成果物作成委託・役務提供委託：親事業者 5千万円超 → 下請事業者 5千万円以下、または親事業者 1千万円超5千万円以下 → 下請事業者 1千万円以下

6. **ルーティングを確認（有効な場合）。**

   `confirm_routing` が `true`（またはフィールドが存在しない）の場合：

   ```
   以下の内容でレビューを実行します：[契約類型]

   識別された文書：
   - [メイン契約書タイトル] → [スキル]
   - [別紙Aタイトル] → [処理方法]
   - [別紙Bタイトル] → [処理方法]
   - 下請法チェック → [該当/非該当/要確認]

   よろしいですか？（はい / いいえ --- 修正すべき点があれば教えてください）
   ```

   確認を待ってから進行する。

   `confirm_routing` が `false` の場合：サイレントに進行する。レビューメモの冒頭にルーティング決定を記録する。

7. **スキルを実行する。** 各スキルのワークフローを完全に実行する。複数のスキルが適用される場合は順次実行し、出力を一つのメモに統合する。

8. **エスカレーションをチェック:** レビュー結果に `~/.claude/plugins/config/claude-for-legal/commercial-legal-jp/CLAUDE.md` のマトリクスに基づいてレビュー担当者の権限を超える事項がある場合、**escalation-flagger** を起動してルーティングと稟議資料を作成する。

9. **フォローアップを提案:**
   - 事業部門向けのステークホルダーサマリー
   - 修正履歴付きの .docx レッドライン
   - CLMレコードの作成（接続済みの場合）
   - 更新台帳への追加（自動更新条項が見つかった場合）
   - 反社排除条項のチェック（`/commercial-legal-jp:hanshakai-check`）
   - 印紙税の確認（紙の契約書の場合、`/commercial-legal-jp:inshi-zei-check`）

## ルーティング確認の設定

`~/.claude/plugins/config/claude-for-legal/commercial-legal-jp/CLAUDE.md` → `## レビュー設定` に追加：

```markdown
## レビュー設定

confirm_routing: true   # falseに設定するとルーティング確認をスキップして自動的に進行
```

コールドスタートインタビューでこの設定を確認する。デフォルトは `true`。信頼が構築されたら `false` に設定可能。

## 使用例

```
/commercial-legal-jp:review 業務委託契約書_ABC社.pdf
```

```
/commercial-legal-jp:review https://drive.google.com/file/d/ABC123
```

```
/commercial-legal-jp:review
[契約書テキストを貼り付け]
```

## 出力

スキルのフォーマットに従ったフルレビューメモ。ルーティング決定を冒頭に記録。逸脱ごとの分析、具体的な修正文言案、承認者の指名。`~/.claude/plugins/config/claude-for-legal/commercial-legal-jp/CLAUDE.md` → 出力設定に従って保存先に出力。

## 免責事項

本スキルの出力は法的助言に代わるものではありません。最終的な判断は必ず弁護士にご確認ください。

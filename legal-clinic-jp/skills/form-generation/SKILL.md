---
name: form-generation
description: >
  参照: 非推奨 — 代わりに `/draft` を使用してください。このスキルはdraftスキルに
  統合されました。書面生成（訴状、答弁書、調停申立書等）はすべて `/draft` が処理します。
  リダイレクト用に保持。
user-invocable: false
---

# [非推奨] 書式生成 → `/draft` を参照

このスキルは `skills/draft/` に統合されました。`/draft` コマンドが、実務分野テンプレートと管轄裁判所に応じた書式を含む、すべてのクリニック書面の初稿生成を処理します。

**代わりに `/legal-clinic-jp:draft [書面タイプ]` を使用してください。**

調停申立書については `/legal-clinic-jp:chouteimoshitate` も利用可能です。
内容証明郵便については `/legal-clinic-jp:naiyoushoumei` も利用可能です。
労働審判申立書については `/legal-clinic-jp:roudoushimpan` も利用可能です。

`skills/draft/SKILL.md` でフルワークフローを参照してください。

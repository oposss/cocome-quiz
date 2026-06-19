# cocome-quiz

ココメ診断クイズ - Vercel にデプロイされた Flask アプリ。

## プロジェクト構成

```
api/index.py        # Flask アプリ本体（Vercel エントリーポイント）
templates/
  index.html        # トップページ（3問のクイズフォーム）
  result.html       # 診断結果ページ
static/
  A.png / B.png / C.png  # 結果タイプ別の画像
vercel.json         # Vercel デプロイ設定
requirements.txt    # Flask==2.3.2
```

## 起動方法

```bash
pip install -r requirements.txt
FLASK_APP=api/index.py flask run --port 5000
```

## 開発ブランチ

`claude/claude-md-review-x40kF` で開発中。

## 未完了タスク

- [ ] リモートへのプッシュ（前セッションで 403 エラー。Settings → Actions → General → Workflow permissions を「Read and write permissions」に変更済みのため、新セッションでは `git push -u origin claude/claude-md-review-x40kF` を実行する）

## スコアロジック（api/index.py）

3問、各0か1で回答 → 合計スコアで結果タイプを判定。
現状スコア最大3なので `cocome_fuwafuwa` のみ到達可能。
他タイプ（majime / tension / tsundere / uranai）を到達可能にするには質問数を増やす必要がある。

# cocome-quiz

ココメ診断クイズ + ラーメン店長SNS動画 - Vercel にデプロイされた Flask アプリ。

---

## プロジェクト構成

```
api/index.py           # Flask アプリ本体（Vercel エントリーポイント）
ramen_story.html       # SNS動画アニメーション（スタンドアロン HTML）
templates/
  index.html           # 診断トップページ
  result.html          # 診断結果ページ
static/
  A.png / B.png / C.png        # 診断結果画像
  story01.jpg〜story12.jpg     # ラーメン店長インフォグラフィック（差し替え用）
  bgm.mp3                      # BGM（Sunoで作成・差し替え可）
vercel.json            # Vercel デプロイ設定
requirements.txt       # Flask==2.3.2
```

---

## SNS動画アニメーション（ramen_story.html）

### コンセプト
- ラーメン店長の12テーマをカード＋ストーリーシーンで紹介する縦型（540×960）動画
- 合計117秒（1分57秒）でBGM1曲とぴったり合う
- Vercel プレビュー URL: `https://cocome-quiz-git-claude-ramen-story-video-dhsl5-oposss-projects.vercel.app/ramen`

### シーン構成
```
イントロ(3s) → [カード(5s) + ストーリー(4s)] × 12回 → ありがとうカード(3s) → エンド(3s)
合計 = 3 + (5+4)×12 + 3 + 3 = 117秒
```

### 画像の差し替え方法
1. `story01.jpg`〜`story12.jpg` を用意する（各テーマのインフォグラフィック画像）
2. `static/` フォルダに配置してコミット＆プッシュ
3. Vercel が自動デプロイ → `/ramen` を開くと画像が表示される

**画像ルール：**
- ファイル名は `story01.jpg`〜`story12.jpg`（ゼロ埋め2桁）
- 推奨サイズ：540×960px（縦型）または正方形でも可（`object-fit:contain` で収まる）
- 画像がない場合は青いテキストシーンが代わりに表示される（`onerror` フォールバック）

### BGMの追加方法
**方法A（ブラウザ再生用）：** ページ上の「ファイル選択」ボタンからMP3を選ぶ

**方法B（MP4出力用）：** 下記「動画ファイル生成」を参照

---

## 動画ファイル（MP4）の生成方法

Playwright + ffmpeg でブラウザを自動録画してMP4を作成する。

### 必要パッケージのインストール
```bash
pip install playwright moviepy flask --ignore-installed
```

### 録画スクリプト
スクリプトは `/tmp/` に作成して実行する：

```python
import subprocess, time, os

FFMPEG = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
VIDEO_DIR = "/tmp/video_frames"
OUTPUT_MP4 = "/home/user/cocome-quiz/ramen_story.mp4"
os.makedirs(VIDEO_DIR, exist_ok=True)

# Flask サーバー起動
env = os.environ.copy()
env["FLASK_APP"] = "api/index.py"
flask_proc = subprocess.Popen(
    ["python3", "-m", "flask", "run", "--port", "5556"],
    cwd="/home/user/cocome-quiz", env=env,
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
)
time.sleep(4)

from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path='/opt/pw-browsers/chromium',
        args=['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
    )
    context = browser.new_context(
        viewport={'width': 540, 'height': 960},
        record_video_dir=VIDEO_DIR,
        record_video_size={'width': 540, 'height': 960}
    )
    page = context.new_page()
    page.goto("http://localhost:5556/ramen")
    page.wait_for_timeout(2000)
    page.click('#brec')         # RECボタン → UIを隠して自動再生開始
    page.wait_for_timeout(120000)  # 117秒 + バッファ
    webm_path = page.video.path()
    context.close()
    browser.close()

flask_proc.terminate()

# WebM → MP4 変換
subprocess.run([
    FFMPEG, '-i', webm_path,
    '-c:v', 'libx264', '-preset', 'fast', '-pix_fmt', 'yuv420p',
    '-y', OUTPUT_MP4
])
print(f"映像のみ MP4: {OUTPUT_MP4}")
```

Bash ツールの実行タイムアウトは `180000`ms に設定すること。

### BGM付きMP4の合成
```bash
FFMPEG="/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"

$FFMPEG -i ramen_story.mp4 -i static/bgm.mp3 \
  -c:v copy -c:a aac -b:a 192k \
  -map 0:v:0 -map 1:a:0 \
  -shortest -y ramen_story_with_bgm.mp4
```

BGMファイルはユーザーがアップロードしたものを使う（パスは `/root/.claude/uploads/...`）。

### 生成ファイルの扱い
MP4は `.gitignore` に追加してコミットしない：
```
ramen_story.mp4
ramen_story_with_bgm.mp4
```

---

## デザインルール（SNS広告アニメーション）

### 全体方針
- **シンプルで読める** — テキストは3行以内、1カードに1メッセージ
- **縦型 540×960px** — Instagram Reels / TikTok / YouTube Shorts 対応
- **BGMと秒数を合わせる** — シーン数×秒数でBGM尺に合わせる

### カードシーン（奇数シーン）
- 背景：温かみのある生成り色 `rgba(253,245,228,.97)`
- アクセント：ボルドー〜ゴールド `#c04010` / `#e8c060`
- フォント：明朝体（日本語らしさ）
- 構成：番号バッジ → 絵文字アイコン → 見出し → 本文

### ストーリーシーン（偶数シーン）
- 背景：深い紺ブルー `#050a1a → #152545`（夜・情熱・プロ感）
- テキスト：薄いブルーホワイト
- 画像がある場合：全面表示（`object-fit:contain`、背景は生成り色）
- 画像がない場合：絵文字＋テキストで代替表示

### アニメーション
- カード登場：`fadeSlideUp`（下から上へフェードイン）
- ストーリー：`fadeIn`（シンプルにフェード）
- パーティクル演出：イントロ・エンドに集中させる

---

## Flask / Vercel

### ローカル起動
```bash
pip install -r requirements.txt
FLASK_APP=api/index.py flask run --port 5000
```

### Vercel デプロイ
`main` ブランチへマージすると本番デプロイされる。
ブランチの PR を作ると Vercel がプレビュー URL を自動生成する。

### Flask ルート
| パス | 内容 |
|------|------|
| `/` | 診断クイズトップ |
| `/result` | 診断結果（POST） |
| `/ramen` | SNS動画アニメーション |

---

## 診断スコアロジック（api/index.py）

8問、各0か1で回答 → 合計スコアで5タイプを判定：

| スコア | タイプ |
|--------|--------|
| 0〜3 | cocome_fuwafuwa |
| 4〜5 | cocome_majime |
| 6 | cocome_tension |
| 7 | cocome_tsundere |
| 8 | cocome_uranai |

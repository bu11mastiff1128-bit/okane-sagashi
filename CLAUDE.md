# おかねさがし（個人用パズルゲーム）

## これは何か

行・列・色のエリアに1枚ずつ、斜めも含めて隣り合わないように隠れたお金を推理で見つけるパズルゲーム。ゲーム本体は依存なしの単一HTML（`docs/index.html`）で、それを以下の2つの形で持ち主の端末に入れる。**ストアには出さない。個人の端末で使うだけ。**

- **iPhone**：`docs/` を GitHub Pages で公開し、Safariの「ホーム画面に追加」で使う（PWA。`sw.js` でオフライン動作）
- **Android（Pixel）**：`android/` の Kotlin プロジェクト。WebView で `assets/index.html` を表示するだけのアプリ。デバッグ鍵で署名して直接インストールする

## フォルダ

```
docs/                 GitHub Pagesで公開するフォルダ（iPhone用）
  index.html          ゲーム本体（これが正本）
  manifest.webmanifest, sw.js, icons/
android/              Android Studio / Gradle プロジェクト
  app/src/main/assets/index.html   docs/index.html のコピー
  app/src/main/java/jp/mastiff/okanesagashi/MainActivity.kt
tools/release.py      更新時に実行（キャッシュ名更新・assetsへコピー・版番号を上げる）
README.md             人間向けの手順書
```

## 持ち主について

- 使用環境：M1 iMac（この作業をする機械）、Pixel 11、iPhone
- 返答は日本語の敬語。結論から書く。前置きと要約の繰り返しは不要
- 作業の前に「何ができて何ができないか」を先に示す
- Android は Kotlin、スクリプトは Python
- Claude Code は Pro サブスクで使用中。`ANTHROPIC_API_KEY` をシェル設定に書く提案はしない

## 最初にやってほしいこと

### A. Android版をPixelに入れる

1. 環境確認
   - JDK 17以上：Android Studio が入っていれば同梱のものを使う
     `export JAVA_HOME="/Applications/Android Studio.app/Contents/jbr/Contents/Home"`
   - Android SDK：通常 `~/Library/Android/sdk`。無ければ Android Studio を入れてもらうか、
     `brew install --cask android-commandlinetools` →
     `sdkmanager "platform-tools" "platforms;android-35" "build-tools;35.0.0"` → `sdkmanager --licenses`
   - `android/local.properties` に `sdk.dir=/Users/（ユーザー名）/Library/Android/sdk` を書く（git管理外）
2. ビルド：`cd android && ./gradlew assembleDebug`
   - エラーが出たら原因を直す。AGP 8.7.3 / Kotlin 2.0.21 / Gradle 8.9 / compileSdk 35 で書いてある。必要なら手元の環境に合う版へ上げてよい
3. Pixelへのインストール
   - 持ち主にPixelの「USBデバッグ」をオンにしてUSBでつないでもらう（手順は README.md）
   - `adb devices` で認識を確認 → `adb install -r app/build/outputs/apk/debug/app-debug.apk`
   - USBが使えない場合は、APKの場所を伝えて持ち主に転送してもらう

### B. iPhone用を GitHub Pages で公開する

1. `gh` が無ければ `brew install gh`
2. `gh auth status` で未ログインなら、持ち主に `gh auth login` を**ターミナルで**実行してもらう（対話式のため）
3. このフォルダ全体を1つのリポジトリにして公開する
   ```
   git init && git add . && git commit -m "おかねさがし v1.0.0"
   gh repo create okane-sagashi --public --source=. --push
   gh api -X POST repos/{owner}/okane-sagashi/pages -f "source[branch]=main" -f "source[path]=/docs"
   ```
   - 無料プランの GitHub Pages は公開リポジトリが必要。リポジトリ名やPublicにすることは、実行前に持ち主に確認する
4. 公開URL `https://{owner}.github.io/okane-sagashi/` が開けるまで待ち、URLを持ち主に伝える
5. 持ち主の作業：iPhoneの**Safari**でURLを開く → 共有 →「ホーム画面に追加」

## ゲームを直したあとの更新手順

1. `docs/index.html` を編集（単一ファイルのまま。外部ライブラリは使わない）
2. `python3 tools/release.py 1.0.1`（版番号は上げていく）
3. iPhone用：`git commit` → `git push`（数分でPagesに反映。iPhoneはアプリを開き直すと更新）
4. Android用：`./gradlew assembleDebug` → `adb install -r ...`（データは残る）

## ゲームの中身で注意すること

- データは `localStorage` に保存（キーは `nawabari.` で始まる）。所持金・家具・進み具合など。キー名を変えると持ち主のデータが消えるので変えない
- 問題は `generatePuzzle(n, seed, tier, opts)` で自動生成。唯一解かつ論理だけで解けるものだけを出す。「やさしい」には1マスだけの色を必ず1つ入れる
- お金の単位「1枚分」は、その問題のお金1枚の金額（ステージや難易度で変わる）
- 画面は縦向き・スマホ幅（約400px）が基準。ライト／ダーク両対応

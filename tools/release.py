#!/usr/bin/env python3
"""ゲームを更新したあとに実行する。

使い方:
    python3 tools/release.py 1.0.1

やること:
  1. docs/sw.js のキャッシュ名を新しい版にする（iPhoneのホーム画面アプリが更新を拾う）
  2. docs/index.html を Android の assets にコピーする
  3. Android の versionName / versionCode を上げる
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    if len(sys.argv) != 2 or not re.fullmatch(r"\d+\.\d+\.\d+", sys.argv[1]):
        sys.exit("使い方: python3 tools/release.py 1.0.1")
    ver = sys.argv[1]

    sw = ROOT / "docs" / "sw.js"
    text = sw.read_text(encoding="utf-8")
    text, n = re.subn(r"const CACHE='okane-[^']*';", f"const CACHE='okane-{ver}';", text)
    if n != 1:
        sys.exit("sw.js のキャッシュ名が見つかりません")
    sw.write_text(text, encoding="utf-8")

    shutil.copy(ROOT / "docs" / "index.html", ROOT / "android" / "app" / "src" / "main" / "assets" / "index.html")

    gradle = ROOT / "android" / "app" / "build.gradle.kts"
    g = gradle.read_text(encoding="utf-8")
    code = int(re.search(r"versionCode = (\d+)", g).group(1)) + 1
    g = re.sub(r"versionCode = \d+", f"versionCode = {code}", g)
    g = re.sub(r'versionName = "[^"]*"', f'versionName = "{ver}"', g)
    gradle.write_text(g, encoding="utf-8")

    print(f"v{ver}（versionCode {code}）に更新しました")


if __name__ == "__main__":
    main()

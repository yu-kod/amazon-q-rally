#!/usr/bin/env python3
"""
Web版ビルドスクリプト
pygbagを使用してブラウザ版を生成します
"""

import subprocess
import sys
import os

def build_web_version():
    """Web版をビルド"""
    print("🚗 Amazon Q Rally - Web版ビルド開始")
    
    # pygbagがインストールされているかチェック
    try:
        import pygbag
        print(f"✅ pygbag {pygbag.__version__} が見つかりました")
    except ImportError:
        print("❌ pygbagがインストールされていません")
        print("pip install pygbag でインストールしてください")
        return False
    
    # ビルドコマンドを実行
    cmd = [
        sys.executable, "-m", "pygbag",
        "--width", "800",
        "--height", "600", 
        "--name", "Amazon Q Rally",
        "--icon", "favicon.ico",  # アイコンファイルがある場合
        "main_web.py"
    ]
    
    print("🔨 ビルドコマンド実行中...")
    print(" ".join(cmd))
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ ビルド成功!")
        print("📁 dist/ フォルダにWeb版が生成されました")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ ビルドエラー: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False

def main():
    """メイン関数"""
    if not os.path.exists("main_web.py"):
        print("❌ main_web.py が見つかりません")
        return
    
    success = build_web_version()
    
    if success:
        print("\n🎉 Web版ビルド完了!")
        print("📖 使用方法:")
        print("1. dist/ フォルダの内容をWebサーバーにアップロード")
        print("2. ブラウザでindex.htmlにアクセス")
        print("3. ゲームを楽しむ!")
    else:
        print("\n💥 ビルドに失敗しました")

if __name__ == "__main__":
    main()

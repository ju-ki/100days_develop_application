# シンプルなHTTP静的ファイル配信サーバー

このプロジェクトは、Pythonで実装されたシンプルなHTTP静的ファイル配信サーバーです。HTML、CSS、JavaScriptなどの静的ファイルを配信することができます。

## 機能

- 静的ファイル（HTML、CSS、JavaScript）の配信
- ポートが使用中の場合、自動的に利用可能なポートを検索
- エラーハンドリング（404 Not Found）
- 適切なContent-Typeヘッダーの設定

## 必要条件

- Python 3.x
- 標準ライブラリのみを使用（追加のインストールは不要）

## 使用方法

1. サーバーを起動:
```bash
python server.py
```

2. デフォルトでは `localhost:8000` でサーバーが起動します
3. ポート8000が使用中の場合は、自動的に利用可能なポートを検索して使用します

## ディレクトリ構造

```
.
├── server.py          # メインのサーバーコード
├── public/           # 静的ファイルを格納するディレクトリ
│   ├── index.html    # メインのHTMLファイル
│   └── main.js       # JavaScriptファイル
└── README.md         # このファイル
```

## 対応しているファイル形式

- HTML (.html) - Content-Type: text/html
- CSS (.css) - Content-Type: text/css
- JavaScript (.js) - Content-Type: application/javascript

## 注意事項

- サーバーは開発環境での使用を想定しています
- 本番環境での使用は推奨されません
- セキュリティ機能は最小限の実装となっています 
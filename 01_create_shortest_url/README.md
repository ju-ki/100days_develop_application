# 100日アプリ作成チャレンジ - 1日目: URL短縮サービス

このプロジェクトは100日アプリ作成チャレンジの1日目の成果物として作成したURL短縮サービスです。

## 技術スタック

- フロントエンド: TypeScript + React
- バックエンド: Python (Flask)
- データベース: SQLite
- 外部API: TinyURL API

## 機能

- URLの短縮機能
- 短縮URLのデータベース保存
- シンプルなRESTful API

## プロジェクト構造

```
.
├── frontend/          # TypeScript + React フロントエンド
├── backend/           # Python バックエンド
│   ├── app.py        # Flaskアプリケーション
│   ├── database.db   # SQLiteデータベース
│   └── requirements.txt # Python依存関係
└── README.md         # プロジェクトの説明
```

## セットアップ方法

### フロントエンド

```bash
cd frontend
npm install
npm start
```

### バックエンド

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## API仕様

### URL短縮

- エンドポイント: `/api/url`
- メソッド: GET
- パラメータ: 
  - `url`: 短縮したいURL
- レスポンス:
  ```json
  {
    "short_url": "https://tinyurl.com/xxxxx"
  }
  ```
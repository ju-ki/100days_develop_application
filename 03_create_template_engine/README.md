# Day3. シンプルなテンプレートエンジン自作

このプロジェクトは、Pythonを使用してシンプルなテンプレートエンジンを自作した成果物です。HTTPサーバーと組み合わせて、動的なHTMLコンテンツの生成を実現しています。

## 🎯 プロジェクト概要

テンプレートエンジンは、静的なHTMLテンプレートに動的なデータを埋め込むための仕組みです。このプロジェクトでは、以下の機能を実装しました：

- **変数置換**: `{{ variable }}` 形式での変数展開
- **条件分岐**: `{{ if condition }}...{{ else }}...{{ endif }}` 形式での条件付き表示
- **ループ処理**: `{{ for item in items }}...{{ endfor }}` 形式での配列要素の繰り返し表示

## 🏗️ プロジェクト構造

```
.
├── server.py              # HTTPサーバーのメイン実装
├── router.py              # ルーティング処理
├── views.py               # ビュー関数の定義
├── engine/
│   ├── __init__.py
│   └── parser.py          # テンプレートエンジンのコア実装
├── static/
│   ├── index.html         # メインページ
│   └── template.html      # テンプレートエンジンのテスト用HTML
├── tests/
│   └── test_parser.py     # テンプレートエンジンのテスト
└── requirements.txt       # 依存関係
```

## 🚀 主な機能

### 1. テンプレートエンジン (`engine/parser.py`)

#### 変数置換
```html
Hello, {{ name }}! Welcome to {{ place }}.
```
```python
context = {"name": "Alice", "place": "Wonderland"}
# 結果: "Hello, Alice! Welcome to Wonderland."
```

#### 条件分岐
```html
{{ if condition }}
    Condition is true!
{{ else }}
    Condition is false!
{{ endif }}
```

#### ループ処理
```html
{{ for item in items }}
    - {{ item }}
{{ endfor }}
```
```python
context = {"items": ["apple", "banana", "cherry"]}
# 結果: "- apple\n- banana\n- cherry"
```

### 2. HTTPサーバー (`server.py`)

- 静的ファイル（HTML、CSS、JavaScript）の配信
- テンプレートエンジンによる動的コンテンツ生成
- ポート競合時の自動ポート切り替え機能

### 3. ルーティングシステム

- `/hello`: シンプルな挨拶メッセージ
- `/about/{id}`: 動的パラメータを使用したページ
- 静的ファイル配信

## 🧪 テスト

プロジェクトには包括的なテストスイートが含まれています：

```bash
# テストの実行
python -m pytest tests/
```

テスト内容：
- 変数置換のテスト
- 複数変数の置換テスト
- ループ処理のテスト
- 条件分岐のテスト

## 🛠️ セットアップと実行

### 1. 依存関係のインストール
```bash
pip install -r requirements.txt
```

### 2. サーバーの起動
```bash
python server.py
```

### 3. アクセス
- メインページ: `http://localhost:8000/`
- テンプレートテスト: `http://localhost:8000/template.html`
- Helloページ: `http://localhost:8000/hello`
- Aboutページ: `http://localhost:8000/about/123`

## 💡 技術的な実装ポイント

### 正規表現によるパース処理
```python
# 変数置換のパターン
pattern = re.compile(r'\{\{ \s*(\w+)\s* \}\}')

# ループ処理のパターン
pattern = re.compile(
    r'\{\{\s*for\s+(\w+)\s+in\s+(\w+)\s*\}\}(.*?)\{\{\s*endfor\s*\}\}',
    re.DOTALL
)
```

### コンテキストベースのレンダリング
テンプレートエンジンは、辞書形式のコンテキストを受け取り、テンプレート内の変数を実際の値に置換します。

### エラーハンドリング
- 存在しない変数への対応
- 不正なテンプレート構文の処理
- ポート競合の自動解決

## 🎨 使用例

### テンプレートファイル (`static/template.html`)
```html
<!DOCTYPE html>
<html>
<body>
    <h1>テンプレートエンジンのテスト</h1>
    
    {{ if is_test }}
    <p>これはテストです</p>
    {{ else }}
    <p>これは表示されません</p>
    {{ endif }}

    {{ for item in items }}
    <li>{{ item }}</li>
    {{ endfor }}
</body>
</html>
```

### サーバー側でのコンテキスト設定
```python
context = {
    'is_test': True,
    'is_test2': False,
    'items': ['apple', 'banana', 'cherry'],
}
```

## 🔮 今後の拡張予定

- [ ] ネストしたループの対応
- [ ] より複雑な条件式のサポート
- [ ] フィルター機能の追加
- [ ] テンプレート継承の実装
- [ ] キャッシュ機能の追加

## 📚 学習成果

このプロジェクトを通じて以下の技術を習得しました：

- **正規表現**を使ったテキストパース処理
- **テンプレートエンジン**の基本的な仕組み
- **HTTPサーバー**の実装
- **テスト駆動開発**の実践
- **モジュール設計**と**コード構造化**

---

*このプロジェクトは学習目的で作成されたものです。実用的なテンプレートエンジンとしては、Jinja2やDjango Templatesなどの既存ライブラリの使用をお勧めします。* 
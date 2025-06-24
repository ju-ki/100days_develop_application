# Day4. JSONパーサーの自作

このプロジェクトは、Pythonを使用してJSONパーサーを自作した成果物です。字句解析器（Tokenizer）と構文解析器（Parser）を実装し、JSON文字列をPythonの辞書やリストに変換する機能を提供しています。

## 🎯 プロジェクト概要

JSONパーサーは、JSON形式の文字列を解析して、Pythonのネイティブなデータ構造（辞書、リスト、数値、文字列、真偽値、null）に変換するための仕組みです。このプロジェクトでは、以下の機能を実装しました：

- **字句解析（Lexical Analysis）**: JSON文字列をトークンに分割
- **構文解析（Syntax Analysis）**: トークンを解析してPythonオブジェクトに変換
- **ネストしたオブジェクトと配列の対応**: 複雑なJSON構造の解析
- **基本データ型のサポート**: 文字列、数値、真偽値、null値の解析

## 🏗️ プロジェクト構造

```
.
├── engine/
│   ├── __init__.py
│   ├── tokenizer.py      # 字句解析器の実装
│   └── parser.py         # 構文解析器の実装
├── tests/
│   └── test_parser.py    # パーサーのテスト
├── server.py             # HTTPサーバー（Day3の成果物）
├── router.py             # ルーティング処理
├── views.py              # ビュー関数
├── static/               # 静的ファイル
└── requirements.txt      # 依存関係
```

## 🚀 主な機能

### 1. 字句解析器 (`engine/tokenizer.py`)

JSON文字列をトークンに分割する字句解析器を実装しました。

#### 対応するトークン
- **識別子**: アルファベット、数字、アンダースコアで構成される文字列
- **数値**: 整数値
- **特殊文字**: `{`, `}`, `[`, `]`, `:`, `,`, `"` など
- **空白文字**: スペース、タブ、改行のスキップ
- **EOF**: ファイル終端の検出

#### 実装の特徴
```python
class Tokenizer:
    def __init__(self, source: str) -> None:
        self._source = source
        self._current_position = 0

    def next_token(self):
        # 空白文字のスキップ
        while self._current_char().isspace():
            self._current_position += 1
        
        # トークンの種類に応じた解析
        char = self._current_char()
        if char.isalpha():
            # 識別子の解析
        elif char.isnumeric():
            # 数値の解析
        else:
            # 特殊文字の解析
```

### 2. 構文解析器 (`engine/parser.py`)

トークンを解析してPythonオブジェクトに変換する構文解析器を実装しました。

#### 対応するJSON構造
- **オブジェクト**: `{"key": "value"}` → Python辞書
- **配列**: `["item1", "item2"]` → Pythonリスト
- **ネストした構造**: オブジェクト内のオブジェクト、配列内の配列
- **基本データ型**: 文字列、数値、真偽値、null値

#### 実装の特徴
```python
class JSONParser:
    def parse(self, json_str: str) -> dict:
        self.tokenizer = Tokenizer(json_str)
        self.current_token = self.tokenizer.next_token()
        return self._parse_object()

    def _parse_value(self):
        # 値の種類に応じた解析
        if self.current_token == '{':
            return self._parse_object()
        elif self.current_token == '[':
            return self._parse_array()
        elif isinstance(value, int):
            return int(value)
        # その他のデータ型...
```

## 🧪 テスト

プロジェクトには包括的なテストスイートが含まれています：

### 実行方法
```bash
# 環境変数を設定してテスト実行
PYTHONPATH=. python tests/test_parser.py
```

### テスト内容
- **シンプルなオブジェクトの解析**
  ```python
  input_str = '{"name": "Alice", "age": 30, "active": true, "bio": null}'
  expected = {"name": "Alice", "age": 30, "active": True, "bio": None}
  ```

- **ネストしたオブジェクトの解析**
  ```python
  input_str = '{"user": {"name": "Alice", "age": 30}}'
  expected = {"user": {"name": "Alice", "age": 30}}
  ```

- **配列の解析**
  ```python
  input_str = '{"tags": ["python", "json", "parser"]}'
  expected = {"tags": ["python", "json", "parser"]}
  ```

- **複雑なネスト構造の解析**
  ```python
  input_str = '''
  {
      "user": {
          "name": "Alice",
          "languages": ["Python", "JavaScript"]
      },
      "active": true
  }
  '''
  ```

## 💡 技術的な実装ポイント

### 1. 字句解析の設計
- **逐次解析**: 文字列を一度に読み込まず、必要に応じてトークンを生成
- **空白文字の効率的なスキップ**: パフォーマンスを考慮した実装
- **エラー検出**: 不正な文字列の早期検出

### 2. 構文解析の設計
- **再帰下降解析**: 各JSON構造に対応する専用の解析メソッド
- **トークンの先読み**: 次のトークンを確認して適切な解析方法を選択
- **エラーハンドリング**: 不正なJSON構文の検出と適切なエラーメッセージ

### 3. データ型の変換
- **型安全性**: JSONのデータ型を適切なPython型に変換
- **null値の処理**: JSONの`null`をPythonの`None`に変換
- **真偽値の処理**: JSONの`true`/`false`をPythonの`True`/`False`に変換

## 🎨 使用例

### 基本的な使用方法
```python
from engine.parser import JSONParser

# パーサーのインスタンス化
parser = JSONParser()

# シンプルなJSONの解析
json_str = '{"name": "Alice", "age": 30}'
result = parser.parse(json_str)
print(result)  # {'name': 'Alice', 'age': 30}

# 配列を含むJSONの解析
json_str = '{"items": ["apple", "banana"], "count": 2}'
result = parser.parse(json_str)
print(result)  # {'items': ['apple', 'banana'], 'count': 2}
```

### 複雑なJSONの解析
```python
# ネストしたオブジェクトと配列
complex_json = '''
{
    "user": {
        "name": "Alice",
        "profile": {
            "age": 30,
            "skills": ["Python", "JavaScript", "SQL"]
        }
    },
    "settings": {
        "theme": "dark",
        "notifications": true
    }
}
'''

result = parser.parse(complex_json)
# 結果: ネストした辞書とリストの構造
```

## 🔮 今後の拡張予定

- [ ] **浮動小数点数のサポート**: 現在は整数のみ対応
- [ ] **エスケープ文字の対応**: `\"`, `\\`, `\n` などのエスケープシーケンス
- [ ] **Unicode文字のサポート**: 日本語や特殊文字の対応
- [ ] **エラーメッセージの改善**: より詳細なエラー情報の提供
- [ ] **パフォーマンスの最適化**: 大規模JSONの効率的な解析
- [ ] **JSON生成機能**: PythonオブジェクトからJSON文字列への変換

## 📚 学習成果

このプロジェクトを通じて以下の技術を習得しました：

### コンパイラ理論
- **字句解析（Lexical Analysis）**: 文字列をトークンに分割する技術
- **構文解析（Syntax Analysis）**: トークンを意味のある構造に変換する技術
- **再帰下降解析**: 文法規則に基づいた解析手法

### プログラミング技術
- **状態管理**: パーサーの現在の状態を適切に管理
- **エラーハンドリング**: 不正な入力に対する適切な処理
- **テスト駆動開発**: 包括的なテストケースの作成

### データ構造とアルゴリズム
- **トークンストリーム**: 逐次的なデータ処理
- **再帰的データ構造**: ネストしたオブジェクトと配列の処理
- **型変換**: 異なるデータ型間の変換

## 🛠️ セットアップと実行

### 1. 環境の準備
```bash
# 仮想環境の作成（推奨）
python -m venv venv
source venv/bin/activate  # macOS/Linux
# または
venv\Scripts\activate     # Windows
```

### 2. 依存関係のインストール
```bash
pip install -r requirements.txt
```

### 3. テストの実行
```bash
# 環境変数を設定してテスト実行
PYTHONPATH=. python tests/test_parser.py
```

### 4. サンプルコードの実行
```bash
# インタラクティブなテスト
PYTHONPATH=. python -c "
from engine.parser import JSONParser
parser = JSONParser()
result = parser.parse('{\"name\": \"Alice\", \"age\": 30}')
print('Parsed result:', result)
"
```

## 🎯 技術的な挑戦と解決

### 1. トークン化の課題
**課題**: JSONの文字列リテラル（`"..."`）の適切な解析
**解決**: 現在は基本的な識別子解析のみ実装。今後、引用符で囲まれた文字列の解析を追加予定。

### 2. ネスト構造の解析
**課題**: オブジェクト内のオブジェクト、配列内の配列の再帰的解析
**解決**: 再帰下降解析手法を使用し、各構造に対応する専用メソッドを実装。

### 3. エラー処理
**課題**: 不正なJSON構文の検出と適切なエラーメッセージの提供
**解決**: 基本的なエラーハンドリングを実装。より詳細なエラー情報の提供を今後の課題として設定。

---

*このプロジェクトは学習目的で作成されたものです。実用的なJSONパーサーとしては、Pythonの標準ライブラリ`json`モジュールの使用をお勧めします。* 
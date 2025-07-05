# Day5. CSVパーサーの自作

このプロジェクトは、Pythonを使用してCSVパーサーを自作した成果物です。字句解析器（Tokenizer）と構文解析器（Parser）を実装し、CSV文字列をPythonのリスト構造に変換する機能を提供しています。

## 🎯 プロジェクト概要

CSVパーサーは、CSV（Comma-Separated Values）形式の文字列を解析して、Pythonのネイティブなデータ構造（リストのリスト）に変換するための仕組みです。このプロジェクトでは、以下の機能を実装しました：

- **字句解析（Lexical Analysis）**: CSV文字列をトークンに分割
- **構文解析（Syntax Analysis）**: トークンを解析してPythonオブジェクトに変換
- **引用符で囲まれたフィールドの対応**: カンマを含むテキストの適切な解析
- **エスケープ文字の対応**: 引用符内の引用符の処理
- **改行文字の処理**: フィールド内の改行文字の保持

## 🏗️ プロジェクト構造

```
.
├── engine/
│   ├── __init__.py
│   ├── tokenizer.py      # 字句解析器の実装
│   └── parser.py         # 構文解析器の実装（CSVパーサー含む）
├── tests/
│   └── test_parser.py    # パーサーのテスト（CSVテスト含む）
├── server.py             # HTTPサーバー（Day3の成果物）
├── router.py             # ルーティング処理
├── views.py              # ビュー関数
├── static/               # 静的ファイル
└── requirements.txt      # 依存関係
```

## 🚀 主な機能

### 1. 字句解析器 (`engine/tokenizer.py`)

CSV文字列をトークンに分割する字句解析器を実装しました。

#### 対応するトークン
- **識別子**: アルファベット、数字、アンダースコアで構成される文字列
- **数値**: 整数値
- **特殊文字**: `,`, `"`, `\n` など
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

### 2. CSV構文解析器 (`engine/parser.py`)

トークンを解析してPythonオブジェクトに変換するCSV構文解析器を実装しました。

#### 対応するCSV構造
- **基本的なCSV**: `name,age,city` → `["name", "age", "city"]`
- **引用符で囲まれたフィールド**: `"Hello, world!"` → `["Hello, world!"]`
- **エスケープされた引用符**: `"She said, ""Hello!"""` → `['She said, "Hello!"']`
- **改行を含むフィールド**: フィールド内の改行文字を保持
- **複数行のCSV**: ヘッダー行とデータ行の解析

#### 実装の特徴
```python
class CSVParser:
    def parse(self, csv_str: str) -> list:
        self.tokenizer = Tokenizer(csv_str)
        self.current_token = self.tokenizer.next_token()
        return self._parse_csv()

    def _parse_csv(self) -> list:
        result = []
        temp_result = []
        while self.current_token != '$EOF':
            if self.current_token == '"':
                # 引用符で囲まれたフィールドの解析
                comma_content = self._parse_comma()
                temp_result.append(comma_content)
            elif self.current_token == ',':
                # カンマの処理
                self._next()
                if self.current_token == '"':
                    temp_result.append(self._parse_comma())
                else:
                    temp_result.append(self.current_token)
            elif self.current_token == '\n':
                # 改行の処理（行の終了）
                result.append(temp_result)
                temp_result = []
            else:
                temp_result.append(self.current_token)
            self._next()
        return result

    def _parse_comma(self):
        # 引用符で囲まれたフィールドの詳細解析
        content = ''
        self._next()
        while self.current_token != '$EOF':
            if self.current_token == '"':
                if self._peek() == '"':
                    # エスケープされた引用符の処理
                    self._next()
                    content += '"'
                    self._next()
                else:
                    break
            else:
                content += self.current_token
                self._next()
        return content
```

## 🧪 テスト

プロジェクトには包括的なCSVパーサーのテストスイートが含まれています：

### 実行方法
```bash
# 環境変数を設定してテスト実行
PYTHONPATH=. python tests/test_parser.py
```

### テスト内容
- **基本的なCSVの解析**
  ```python
  csv_text = 'name,age,city\nAlice,30,Tokyo\nBob,25,Osaka\n'
  expected = [
      ["name", "age", "city"],
      ["Alice", 30, "Tokyo"],
      ["Bob", 25, "Osaka"],
  ]
  ```

- **引用符で囲まれたフィールドの解析**
  ```python
  csv_text = 'name,comment\nAlice,"Hello, world!"\nBob,"Nice to meet you."\n'
  expected = [
      ["name", "comment"],
      ["Alice", "Hello, world!"],
      ["Bob", "Nice to meet you."],
  ]
  ```

- **改行を含むフィールドの解析**
  ```python
  csv_text = 'name,comment\nAlice,"This is a\nmultiline\ncomment."\nBob,"Another line."\n'
  expected = [
      ["name", "comment"],
      ["Alice", "This is a\nmultiline\ncomment."],
      ["Bob", "Another line."],
  ]
  ```

- **エスケープされた引用符の解析**
  ```python
  csv_text = 'name,quote\nAlice,"She said, ""Hello!"""\nBob,"He replied, ""Goodbye!"""\n'
  expected = [
      ["name", "quote"],
      ["Alice", 'She said, "Hello!"'],
      ["Bob", 'He replied, "Goodbye!"'],
  ]
  ```

## 💡 技術的な実装ポイント

### 1. 引用符で囲まれたフィールドの処理
- **開始引用符の検出**: `"` トークンでフィールドの開始を認識
- **終了引用符の検出**: 対応する `"` トークンでフィールドの終了を認識
- **エスケープ文字の処理**: `""` でエスケープされた引用符を適切に処理

### 2. カンマの処理
- **フィールド区切り**: カンマでフィールドを区切る
- **引用符内のカンマ**: 引用符で囲まれたフィールド内のカンマは文字として扱う
- **空フィールド**: 連続するカンマで空フィールドを表現

### 3. 改行文字の処理
- **行区切り**: 改行文字で行を区切る
- **フィールド内の改行**: 引用符で囲まれたフィールド内の改行は保持
- **データ構造**: 各行をリストとして、全体をリストのリストとして返す

### 4. エラーハンドリング
- **不正な引用符**: 開始引用符に対応する終了引用符がない場合の処理
- **EOF検出**: ファイル終端での適切な処理
- **トークン先読み**: 次のトークンを確認して適切な解析方法を選択

## 🎨 使用例

### 基本的な使用方法
```python
from engine.parser import CSVParser

# パーサーのインスタンス化
parser = CSVParser()

# シンプルなCSVの解析
csv_str = 'name,age,city\nAlice,30,Tokyo\nBob,25,Osaka\n'
result = parser.parse(csv_str)
print(result)
# 出力:
# [
#     ["name", "age", "city"],
#     ["Alice", 30, "Tokyo"],
#     ["Bob", 25, "Osaka"]
# ]
```

### 引用符で囲まれたフィールドの解析
```python
# カンマを含むフィールド
csv_str = 'name,comment\nAlice,"Hello, world!"\nBob,"Nice to meet you."\n'
result = parser.parse(csv_str)
print(result)
# 出力:
# [
#     ["name", "comment"],
#     ["Alice", "Hello, world!"],
#     ["Bob", "Nice to meet you."]
# ]
```

### エスケープされた引用符の解析
```python
# 引用符内の引用符
csv_str = 'name,quote\nAlice,"She said, ""Hello!"""\nBob,"He replied, ""Goodbye!"""\n'
result = parser.parse(csv_str)
print(result)
# 出力:
# [
#     ["name", "quote"],
#     ["Alice", 'She said, "Hello!"'],
#     ["Bob", 'He replied, "Goodbye!"']
# ]
```

### 改行を含むフィールドの解析
```python
# フィールド内の改行
csv_str = 'name,comment\nAlice,"This is a\nmultiline\ncomment."\nBob,"Another line."\n'
result = parser.parse(csv_str)
print(result)
# 出力:
# [
#     ["name", "comment"],
#     ["Alice", "This is a\nmultiline\ncomment."],
#     ["Bob", "Another line."]
# ]
```

## 🔮 今後の拡張予定

- [ ] **浮動小数点数のサポート**: 現在は整数のみ対応
- [ ] **より複雑なエスケープ文字の対応**: `\n`, `\t`, `\r` などの制御文字
- [ ] **Unicode文字のサポート**: 日本語や特殊文字の対応
- [ ] **エラーメッセージの改善**: より詳細なエラー情報の提供
- [ ] **パフォーマンスの最適化**: 大規模CSVファイルの効率的な解析
- [ ] **CSV生成機能**: PythonオブジェクトからCSV文字列への変換
- [ ] **異なる区切り文字の対応**: タブ区切り（TSV）など
- [ ] **ヘッダー行の自動検出**: データ型の自動判定

## 📚 学習成果

このプロジェクトを通じて以下の技術を習得しました：

### コンパイラ理論
- **字句解析（Lexical Analysis）**: 文字列をトークンに分割する技術
- **構文解析（Syntax Analysis）**: トークンを意味のある構造に変換する技術
- **状態管理**: パーサーの現在の状態を適切に管理

### プログラミング技術
- **エラーハンドリング**: 不正な入力に対する適切な処理
- **テスト駆動開発**: 包括的なテストケースの作成
- **データ構造の設計**: CSVデータに適したリスト構造の設計

### データ処理技術
- **テキスト解析**: 構造化されたテキストデータの解析
- **エスケープ文字の処理**: 特殊文字の適切な処理
- **区切り文字の処理**: カンマ、改行などの区切り文字の処理

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
from engine.parser import CSVParser
parser = CSVParser()
result = parser.parse('name,age\\nAlice,30\\nBob,25')
print('Parsed result:', result)
"
```

## 🎯 技術的な挑戦と解決

### 1. 引用符で囲まれたフィールドの解析
**課題**: カンマを含むテキストを適切にフィールドとして解析する
**解決**: 引用符の開始と終了を検出し、その間の内容を一つのフィールドとして扱う

### 2. エスケープされた引用符の処理
**課題**: フィールド内の引用符を文字として扱う
**解決**: 連続する引用符（`""`）をエスケープ文字として処理し、一つの引用符として扱う

### 3. 改行文字の処理
**課題**: フィールド内の改行と行区切りの改行を区別する
**解決**: 引用符で囲まれたフィールド内の改行は保持し、引用符外の改行は行区切りとして扱う

### 4. 状態管理の複雑さ
**課題**: パーサーの現在の状態（引用符内かどうかなど）を適切に管理する
**解決**: トークンの種類と前後のコンテキストを考慮した状態遷移の実装

---

*このプロジェクトは学習目的で作成されたものです。実用的なCSVパーサーとしては、Pythonの標準ライブラリ`csv`モジュールの使用をお勧めします。* 
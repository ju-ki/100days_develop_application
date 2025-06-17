from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import sqlite3
import os

app = Flask(__name__)
CORS(app)

# データベースの初期化
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    # ここにテーブル作成のSQLを追加
    c.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_url TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print('Database initialized.')


def insert_url(original_url, short_url):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO urls (original_url, short_url) VALUES (?, ?)', (original_url, short_url))
    conn.commit()
    conn.close()

@app.route('/api/url', methods=['GET'])
def create_shorten_url():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400
    api_url = "http://tinyurl.com/api-create.php"
    params = {'url': url}
    response = requests.get(api_url, params=params)
    if response.status_code != 200:
        return jsonify({"error": "Failed to shorten URL"}), 500
    short_url = response.text
    insert_url(url, short_url)
    return jsonify({"short_url": short_url})
    
if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
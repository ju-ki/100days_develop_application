class Router:
    # 基本的なルーティング関数
    def hello_function(self):
        return "Hello, World!"

    # 渡ってきたIDを元に動的な値を返す関数
    def about_function(self, params):
        id = params.get('id', 'default')
        if not id.isdigit():
            return "Invalid ID"
        return f"About page for ID: {id}"

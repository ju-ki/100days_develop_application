class Tokenizer:
    def __init__(self, source: str) -> None:
        self._source = source
        self._current_position = 0

    def _current_char(self) -> str:
        if self._current_position < len(self._source):
            return self._source[self._current_position]
        return '$EOF'

    def next_token(self):
        while self._current_char().isspace():
            self._current_position += 1

        start = self._current_position

        char = self._current_char()
        if char == "$EOF":
            return "$EOF"
        elif char.isalpha():
            while self._current_char().isalnum() or self._current_char() == "_":
                self._current_position += 1
            return self._source[start:self._current_position]
        elif char.isnumeric():
            while self._current_char().isnumeric():
                self._current_position += 1
            return int(self._source[start:self._current_position])
        else:
            self._current_position += 1
            return self._source[start:self._current_position]
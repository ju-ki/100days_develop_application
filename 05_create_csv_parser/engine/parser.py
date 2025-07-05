import re
from engine.tokenizer import Tokenizer

# TODO: ネスト対応
class Parser:
    def render_template_all(self, template: str, context: dict) -> str:
        template = self.render_template_for_condition(template, context)
        template = self.render_template_for_loop(template, context)
        template = self.render_template(template, context)
        return template.strip()
    def render_template(self, template: str, context: dict) -> str:
        pattern = re.compile(r'\{\{ \s*(\w+)\s* \}\}') # simple pattern
        return pattern.sub(lambda match: str(context.get(match.group(1), "")), template)

    def render_template_for_loop(self, template: str, context: dict) -> str:
        pattern = re.compile(
            r'\{\{\s*for\s+(\w+)\s+in\s+(\w+)\s*\}\}(.*?)\{\{\s*endfor\s*\}\}',
            re.DOTALL
        )

        def replacer(match):
            item_name = match.group(1)
            list_name = match.group(2)
            block_name = match.group(3).strip()
            items = context.get(list_name, [])
            result = []
            for item in items:
                text = self.render_template(block_name, {item_name: item})
                result.append(text)
            return '\n'.join(result)
        return pattern.sub(replacer, template).strip()

    def render_template_for_condition(self, template: str, context: dict) -> str:
        pattern = re.compile(r'\{\{\s*if\s*(\w+)\s*\}\}(.*?)\{\{\s*else\s*\}\}(.*?)\{\{\s*endif\s*\}\}', re.DOTALL)

        def replacer(match):
            condition = match.group(1)
            if context.get(condition):
                return match.group(2)
            else:
                return match.group(3)
        return pattern.sub(replacer, template).strip()


class JSONParser:
    def parse(self, json_str: str) -> dict:
        self.tokenizer = Tokenizer(json_str)
        self.current_token = self.tokenizer.next_token()
        return self._parse_object()

    def _next(self):
        self.current_token = self.tokenizer.next_token()

    def _parse_value(self):
        value = self.current_token
        if self.current_token == '{':
            value = self._parse_object()
            return value
        elif self.current_token == '[':
            value = self._parse_array()
            return value
        elif isinstance(value, int):
            return int(value)
        elif value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False
        elif value.lower() == 'null':
            return None
        elif value.isspace():
            self._next()
            return self._parse_value()
        else:
            return value

    def _parse_array(self) -> list:
        result = []
        if self.current_token != '[':
            raise ValueError("JSON must start with '['")
        self._next()
        while self.current_token != '$EOF' and self.current_token != ']':
            if self.current_token in [',', ':', '"'] or str(self.current_token).isspace():
                self._next()
            else:
                value = self._parse_value()
                result.append(value)
                self._next()
        return result

    def _parse_object(self) -> dict:
        parsed_json = {}
        key = None

        # 先頭のスキップは除去
        while self.current_token.isspace():
            self._next()

        if(self.current_token != '{'):
            raise ValueError("JSON must start with '{'")

        self._next()

        while self.current_token != '$EOF' and self.current_token != '}':
            if self.current_token not in [':', '"', ','] and not str(self.current_token).isspace():
                if key is None:
                    key = self.current_token
                elif key is not None:
                    value = self._parse_value()
                    parsed_json[key] = value
                    key = None
            self._next()
        return parsed_json

class CSVParser:
    def parse(self, csv_str:str) -> list:
        self.tokenizer = Tokenizer(csv_str)
        self.current_token = self.tokenizer.next_token()
        return self._parse_csv();

    def _parse_csv(self) -> list:
        result = []
        temp_result = []
        while self.current_token != '$EOF':
            if self.current_token == '"':
                comma_content = self._parse_comma()
                temp_result.append(comma_content)
            else:
                if self.current_token == ',':
                    self._next()
                    if self.current_token == '"':
                        temp_result.append(self._parse_comma())
                    else:
                        temp_result.append(self.current_token)
                elif self.current_token == '\n':
                    result.append(temp_result)
                    temp_result = []
                else:
                    temp_result.append(self.current_token)
            self._next()
        return result

    def _parse_comma(self):
        content = ''
        self._next()
        while self.current_token != '$EOF':
            if self.current_token == '"':
                if self._peek() == '"':
                    self._next()
                    content += '"'
                    self._next()
                else:
                    break
            else:
                content += self.current_token
                self._next()
        return content

    def _next(self):
        self.current_token = self.tokenizer.next_token()

    def _peek(self):
        return self.tokenizer.get_next_token()
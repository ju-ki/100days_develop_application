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
        else:
            return value

    def _parse_array(self) -> list:
        result = []
        if self.current_token != '[':
            raise ValueError("JSON must start with '['")
        self._next()
        while self.current_token != '$EOF' and self.current_token != ']':
            if self.current_token in [',', ':', '"']:
                self._next()
            else:
                value = self._parse_value()
                result.append(value)
                self._next()
        return result

    def _parse_object(self) -> dict:
        parsed_json = {}
        key = None
        if(self.current_token != '{'):
            raise ValueError("JSON must start with '{'")

        self._next()

        while self.current_token != '$EOF' and self.current_token != '}':
            if self.current_token not in [':', '"', ',']:
                if key is None:
                    key = self.current_token
                elif key is not None:
                    value = self._parse_value()
                    parsed_json[key] = value
                    key = None
            self._next()
        return parsed_json
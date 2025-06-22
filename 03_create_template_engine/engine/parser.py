import re

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

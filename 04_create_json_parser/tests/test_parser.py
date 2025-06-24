from engine.parser import Parser, JSONParser

parser = Parser()

def test_parser_render_template():
    template = "Hello, {{ name }}! Welcome to {{ place }}."
    context = {
        "name": "Alice",
        "place": "Wonderland"
    }
    expected_output = "Hello, Alice! Welcome to Wonderland."

    result = parser.render_template(template, context)

    assert result == expected_output

def test_parser_render_template2():
    template = """
       {{ nameB }}: Hello, {{ nameA }}!
       {{ nameA }}: Hi, {{ nameB }}!
       {{ nameB }}: How are you?
       {{ nameA }}: I'm fine, thanks!
    """
    context = {
        "nameA": "Alice",
        "nameB": "Bob"
    }
    expected_output = """
       Bob: Hello, Alice!
       Alice: Hi, Bob!
       Bob: How are you?
       Alice: I'm fine, thanks!
    """

    result = parser.render_template(template, context)

    assert result == expected_output


def test_parser_render_array_template():
    template = """
        {{ for item in items }}
        - {{ item }}
        {{ endfor }}
    """
    context = {
        "items": ["apple", "banana", "cherry"]
    }

    expected_output = "- apple\n- banana\n- cherry"
    result = parser.render_template_for_loop(template, context)

    assert result == expected_output


def test_parser_render_condition_template():
    template = """
        {{ if condition }}
        Condition is true!
        {{ else }}
        Condition is false!
        {{ endif }}
    """
    context_true = {
        "condition": True
    }
    context_false = {
        "condition": False
    }

    expected_output_true = "Condition is true!"
    expected_output_false = "Condition is false!"

    result_true = parser.render_template_for_condition(template, context_true)
    result_false = parser.render_template_for_condition(template, context_false)

    assert result_true == expected_output_true
    assert result_false == expected_output_false


def test_parse_simple_object():
    input_str = '{"name": "Alice", "age": 30, "active": true, "bio": null}'
    result = JSONParser().parse(input_str)
    assert result == {"name": "Alice", "age": 30, "active": True, "bio": None}

def test_parse_nested_object():
    input_str = '{"user": {"name": "Alice", "age": 30}}'
    result = JSONParser().parse(input_str)
    assert result == {"user": {"name": "Alice", "age": 30}}

def test_parse_array():
    input_str = '{"tags": ["python", "json", "parser"]}'
    result = JSONParser().parse(input_str)
    print(result)
    assert result == {"tags": ["python", "json", "parser"]}

def test_parse_nested_object_with_array():
    input_str = '''
    {
        "user": {
            "name": "Alice",
            "languages": ["Python", "JavaScript"]
        },
        "active": true
    }
    '''
    result = JSONParser().parse(input_str)
    print(result)
    assert result == {
        "user": {
            "name": "Alice",
            "languages": ["Python", "JavaScript"]
        },
        "active": True
    }

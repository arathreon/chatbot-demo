from chatbot.tools.base import Tool


def handler(x):
    return {"result": x + 1}


def test_tool_instantiation():
    tool = Tool(
        name="test_tool",
        description="test_tool_description",
        parameters={
            "type": "object",
            "properties": {"x": {"type": "integer", "description": "Integer for adding one."}},
            "required": ["x"],
        },
        handler=handler,
    )

    assert tool.name == "test_tool"
    assert tool.description == "test_tool_description"
    assert tool.parameters == {
        "type": "object",
        "properties": {"x": {"type": "integer", "description": "Integer for adding one."}},
        "required": ["x"],
    }
    assert tool.handler == handler


def test_tool_open_ai_schema():
    tool = Tool(
        name="test_tool",
        description="test_tool_description",
        parameters={
            "type": "object",
            "properties": {"x": {"type": "integer", "description": "Integer for adding one."}},
            "required": ["x"],
        },
        handler=handler,
    )

    assert tool.to_openai_schema() == {
        "type": "function",
        "function": {
            "name": "test_tool",
            "description": "test_tool_description",
            "parameters": {
                "type": "object",
                "properties": {"x": {"type": "integer", "description": "Integer for adding one."}},
                "required": ["x"],
            },
        },
    }


def test_tool_execute():
    tool = Tool(
        name="test_tool",
        description="test_tool_description",
        parameters={
            "type": "object",
            "properties": {"x": {"type": "integer", "description": "Integer for adding one."}},
            "required": ["x"],
        },
        handler=handler,
    )

    result = tool.execute({"x": 10})
    assert result == '{"result": 11}'


def test_tool_execute_fails():
    def handle_raise(x: int):
        raise ValueError("Problem with invoking the handler.")

    tool = Tool(
        name="test_tool",
        description="test_tool_description",
        parameters={
            "type": "object",
            "properties": {"x": {"type": "integer", "description": "Integer for adding one."}},
            "required": ["x"],
        },
        handler=handle_raise,
    )

    result = tool.execute({"x": 10})
    assert result == '{"error": "Problem with invoking the handler."}'

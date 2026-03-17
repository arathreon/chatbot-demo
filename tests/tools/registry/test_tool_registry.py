import json

import pytest

from chatbot.tools.base import Tool
from chatbot.tools.registry import ToolRegistry


def handler(x):
    return {"result": x + 1}


def return_things(argument: str):
    assert argument == "this is the argument"
    return {
        "par1": "val1",
        "par2": "val2",
    }


def test_tool_registry_registers_tool():
    test_tool = Tool(
        name="test_tool",
        description="test_tool_description",
        parameters={
            "type": "object",
            "properties": {"x": {"type": "integer", "description": "Integer for adding one."}},
            "required": ["x"],
        },
        handler=handler,
    )
    registry = ToolRegistry()
    assert registry._tools == {}

    registry.register(test_tool)
    assert len(registry._tools) == 1
    assert registry._tools["test_tool"] == test_tool


def test_tool_registry_raises_on_registering_duplicity():
    test_tool = Tool(
        name="test_tool",
        description="test_tool_description",
        parameters={
            "type": "object",
            "properties": {"x": {"type": "integer", "description": "Integer for adding one."}},
            "required": ["x"],
        },
        handler=handler,
    )
    registry = ToolRegistry()
    registry.register(test_tool)
    assert len(registry._tools) == 1
    assert registry._tools["test_tool"] == test_tool

    test_tool_2 = Tool(
        name="test_tool",
        description="test_tool_description_2",
        parameters={
            "type": "object",
            "properties": {"x": {"type": "integer", "description": "Integer for adding one."}},
            "required": ["x"],
        },
        handler=handler,
    )

    with pytest.raises(ValueError):
        registry.register(test_tool_2)


def test_tool_registry_returns_unknown_tool():
    test_execute_tool_name = "test_tool"
    test_arguments = {}
    registry = ToolRegistry()

    assert registry._tools.get(test_execute_tool_name) is None

    result = registry.execute(test_execute_tool_name, test_arguments)
    assert result == json.dumps({"error": f"Unknown tool: '{test_execute_tool_name}'."})


def test_tool_registry_execute_returns_correctly():
    test_tool = Tool(
        name="test_tool",
        description="test_tool_description",
        parameters={
            "type": "object",
            "properties": {"argument": {"type": "string", "description": "Argument of the test function"}},
            "required": ["argument"],
        },
        handler=return_things,
    )

    registry = ToolRegistry()
    registry.register(test_tool)

    assert "test_tool" in registry._tools

    results = registry.execute("test_tool", {"argument": "this is the argument"})
    assert results == json.dumps(
        {
            "par1": "val1",
            "par2": "val2",
        }
    )


def test_tool_registry_returns_correct_openai_schema():
    test_tool = Tool(
        name="test_tool",
        description="test_tool_description",
        parameters={
            "type": "object",
            "properties": {"argument": {"type": "string", "description": "Argument of the test function"}},
            "required": ["argument"],
        },
        handler=return_things,
    )

    test_tool_2 = Tool(
        name="test_tool_2",
        description="test_tool_description_2",
        parameters={
            "type": "object",
            "properties": {"x": {"type": "integer", "description": "Integer for adding one."}},
            "required": ["x"],
        },
        handler=handler,
    )

    registry = ToolRegistry()
    registry.register(test_tool)
    registry.register(test_tool_2)

    results = registry.get_openai_schemas()

    assert results == [
        {
            "type": "function",
            "function": {
                "name": "test_tool",
                "description": "test_tool_description",
                "parameters": {
                    "type": "object",
                    "properties": {"argument": {"type": "string", "description": "Argument of the test function"}},
                    "required": ["argument"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "test_tool_2",
                "description": "test_tool_description_2",
                "parameters": {
                    "type": "object",
                    "properties": {"x": {"type": "integer", "description": "Integer for adding one."}},
                    "required": ["x"],
                },
            },
        },
    ]

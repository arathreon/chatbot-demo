import json
from unittest.mock import MagicMock, patch


from chatbot.chat.orchestration import run_agent_loop
from chatbot.tools.base import Tool
from chatbot.tools.registry import ToolRegistry


def make_stop_response(content: str) -> MagicMock:
    message = MagicMock()
    message.content = content
    message.tool_calls = None
    message.model_dump.return_value = {"role": "assistant", "content": content}

    choice = MagicMock()
    choice.finish_reason = "stop"
    choice.message = message

    response = MagicMock()
    response.choices = [choice]
    return response


def make_tool_calls_response(
    tool_name: str,
    tool_args: dict,
    tool_call_id: str = "call_1",
) -> MagicMock:
    tool_call = MagicMock()
    tool_call.id = tool_call_id
    tool_call.function.name = tool_name
    tool_call.function.arguments = json.dumps(tool_args)

    message = MagicMock()
    message.content = None
    message.tool_calls = [tool_call]
    message.model_dump.return_value = {
        "role": "assistant",
        "content": None,
        "tool_calls": [
            {
                "id": tool_call_id,
                "function": {
                    "name": tool_name,
                    "arguments": json.dumps(tool_args),
                },
            }
        ],
    }

    choice = MagicMock()
    choice.finish_reason = "tool_calls"
    choice.message = message

    response = MagicMock()
    response.choices = [choice]
    return response


def make_unexpected_response(reason: str = "content_filter") -> MagicMock:
    message = MagicMock()
    message.content = None
    message.tool_calls = None

    choice = MagicMock()
    choice.finish_reason = reason
    choice.message = message

    response = MagicMock()
    response.choices = [choice]
    return response


def make_tool(name: str = "get_vacation_days", return_value: dict | None = None) -> Tool:
    handler = MagicMock(return_value=return_value or {"days": 10})
    return Tool(
        name=name,
        description="Returns vacation days for an employee.",
        parameters={
            "type": "object",
            "properties": {"employee_id": {"type": "integer"}},
            "required": ["employee_id"],
        },
        handler=handler,
    )


@patch("chatbot.chat.orchestration.OpenAI")
def test_run_agent_loop_stops_immediately(mock_openai_cls):
    client = mock_openai_cls.return_value
    client.chat.completions.create.return_value = make_stop_response("This is the answer")

    conversation_history = []
    result = run_agent_loop("test user input", ToolRegistry(), conversation_history)

    assert result == "This is the answer"
    client.chat.completions.create.assert_called_once()
    assert conversation_history[-1] == {"role": "assistant", "content": "This is the answer"}


@patch("chatbot.chat.orchestration.OpenAI")
def test_run_agent_loop_calls_tool_then_stops(mock_openai_cls):
    tool = make_tool(return_value={"days": 10})
    registry = ToolRegistry()
    registry.register(tool)

    client = mock_openai_cls.return_value
    client.chat.completions.create.side_effect = [
        make_tool_calls_response("get_vacation_days", {"employee_id": 42}, "call_abc"),
        make_stop_response("You have 10 vacation days."),
    ]

    conversation_history = []
    result = run_agent_loop(
        "How many vacation days do I have?",
        registry,
        conversation_history,
        max_iterations=5,
    )

    assert result == "You have 10 vacation days."
    assert client.chat.completions.create.call_count == 2
    tool.handler.assert_called_once_with(employee_id=42)

    tool_messages = [m for m in conversation_history if m.get("role") == "tool"]
    assert len(tool_messages) == 1
    assert tool_messages[0]["tool_call_id"] == "call_abc"
    assert json.loads(tool_messages[0]["content"]) == {"days": 10}


@patch("chatbot.chat.orchestration.OpenAI")
def test_run_agent_loop_stops_unexpectedly(mock_openai_cls):
    client = mock_openai_cls.return_value
    client.chat.completions.create.return_value = make_unexpected_response("content_filter")

    result = run_agent_loop("some input", ToolRegistry(), [])

    assert result == "I was unable to complete your request. Please try again."
    client.chat.completions.create.assert_called_once()


@patch("chatbot.chat.orchestration.OpenAI")
def test_run_agent_loop_reaches_max_iterations(mock_openai_cls):
    tool = make_tool(return_value={"days": 5})
    registry = ToolRegistry()
    registry.register(tool)

    client = mock_openai_cls.return_value
    client.chat.completions.create.return_value = make_tool_calls_response(
        "get_vacation_days", {"employee_id": 1}, "call_x"
    )

    max_iterations = 3
    result = run_agent_loop("input", registry, [], max_iterations=max_iterations)

    assert result == "I was unable to complete your request. Please try again."
    assert client.chat.completions.create.call_count == max_iterations

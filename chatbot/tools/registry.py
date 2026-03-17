import json

from chatbot.tools.base import Tool


class ToolRegistry:
    """
    The registry collects tools and dispatches them by name.
    """

    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool):
        if tool.name in self._tools:
            raise ValueError(f"A tool with the name '{tool.name}' already exists in the registry")

        self._tools[tool.name] = tool

    def get_openai_schemas(self) -> list[dict]:
        return [tool.to_openai_schema() for tool in self._tools.values()]

    def execute(self, name: str, arguments: dict) -> str:
        tool = self._tools.get(name)

        if not tool:
            return json.dumps({"error": f"Unknown tool: '{tool.name}'."})

        try:
            return tool.execute(arguments)
        except Exception as e:
            return json.dumps({"error": str(e)})

import json
import logging

from chatbot.tools.base import Tool


logger = logging.getLogger(__name__)


class ToolRegistry:
    """
    The registry collects tools and dispatches them by name.
    """

    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool):
        if tool.name in self._tools:
            logger.error("A tool with the name '%s' already exists in the registry", tool.name)
            raise ValueError(f"A tool with the name '{tool.name}' already exists in the registry")

        self._tools[tool.name] = tool

    def get_openai_schemas(self) -> list[dict]:
        return [tool.to_openai_schema() for tool in self._tools.values()]

    def execute(self, name: str, arguments: dict) -> str:
        tool = self._tools.get(name)

        if not tool:
            logger.error("Unknown tool: '%s'.", name)
            return json.dumps({"error": "Unknown tool: '{name}'."})

        try:
            return tool.execute(arguments)
        except Exception as e:
            logger.exception("Could not execute tool: '%s'", tool.name)
            return json.dumps({"error": str(e)})

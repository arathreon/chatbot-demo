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
            message = f"A tool with the name '{tool.name}' already exists in the registry"
            logger.error(message)
            raise ValueError(message)

        self._tools[tool.name] = tool

    def get_openai_schemas(self) -> list[dict]:
        return [tool.to_openai_schema() for tool in self._tools.values()]

    def execute(self, name: str, arguments: dict) -> str:
        tool = self._tools.get(name)

        if not tool:
            message = f"Unknown tool: '{name}'."
            logger.error(message)
            return json.dumps({"error": message})

        try:
            return tool.execute(arguments)
        except Exception as e:
            logger.exception(f"Could not execute tool: '{tool.name}'")
            return json.dumps({"error": str(e)})

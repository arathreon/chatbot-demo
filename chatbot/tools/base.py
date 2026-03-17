import json
from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    parameters: dict[str, Any]
    handler: Callable[..., dict]

    def execute(self, arguments: dict) -> str:
        try:
            results = self.handler(**arguments)
            return json.dumps(results)
        except Exception as e:
            return json.dumps({"error": str(e)})

    def to_openai_schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }

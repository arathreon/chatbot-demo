from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Any


@dataclass
class Document:
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)


DocumentLoader = Callable[[Path], list[Document]]

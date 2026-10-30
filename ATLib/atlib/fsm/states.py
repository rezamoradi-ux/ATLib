"""State and StatesGroup definitions."""

from __future__ import annotations
from typing import Any


class State:
    def __init__(self, name: str | None = None, group: type | None = None):
        self.name = name
        self.group = group

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name
        self.group = owner

    def __str__(self) -> str:
        if self.group:
            return f"{self.group.__name__}:{self.name}"
        return self.name or "State"

    def __repr__(self) -> str:
        return f"<State {self}>"


class StatesGroupMeta(type):
    def __new__(mcs, name: str, bases: tuple, namespace: dict[str, Any]):
        cls = super().__new__(mcs, name, bases, namespace)
        for key, value in namespace.items():
            if isinstance(value, State):
                value.name = key
                value.group = cls
        return cls


class StatesGroup(metaclass=StatesGroupMeta):
    """Base class for grouping related states."""
    pass

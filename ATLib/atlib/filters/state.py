"""FSM state filter."""

from __future__ import annotations
from .base import Filter
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..types.updates import Update
    from ..context import Context


class StateFilter(Filter):
    def __init__(self, state: Any):
        self.state = state

    async def check(self, update: Update, ctx: Context) -> bool:
        if ctx.fsm is None:
            return False
        current = await ctx.fsm.get_state()
        if self.state is None:
            return current is None
        expected = str(self.state) if not isinstance(self.state, str) else self.state
        return current == expected

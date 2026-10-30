"""Pytest fixtures."""

import pytest
from atlib.storage.memory import MemoryStorage
from atlib.fsm.manager import FSMManager


@pytest.fixture
def memory_storage():
    return MemoryStorage()


@pytest.fixture
def fsm_manager(memory_storage):
    return FSMManager(memory_storage)

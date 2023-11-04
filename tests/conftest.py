from typing import Any, Callable

import pytest

DeleteKeys = Callable[[dict[str, Any], list[str]], None]


@pytest.fixture
def delete_keys() -> DeleteKeys:
    def remove_items(idict: dict[str, Any], keys: list[str]):
        for key in keys:
            del idict[key]

    return remove_items

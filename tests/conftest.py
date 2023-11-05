from typing import Any, Callable

import pytest

ExcludeKeys = Callable[[dict[str, Any], list[str]], None]
IncludeKeys = Callable[[dict[str, Any], list[str]], dict[str, Any]]


@pytest.fixture
def exclude_keys() -> ExcludeKeys:
    def local_func(idict: dict[str, Any], keys: list[str]):
        for key in keys:
            del idict[key]

    return local_func


@pytest.fixture
def include_keys() -> IncludeKeys:
    def local_func(idict: dict[str, Any], keys: list[str]):
        new_dict = dict()

        for key in keys:
            new_dict[key] = idict[key]

        return new_dict

    return local_func


@pytest.fixture
def jwt_token() -> str:
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJyYW5kdXNlciIsImV4cCI6MTY5OTcyMjQzN30.M4GwAZR66Xi2XfNvuR2kNTBa3xEi3mg0nd_ZUPL21o4"

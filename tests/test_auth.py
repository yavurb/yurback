from typing import Any, Generator

from fastapi.testclient import TestClient
from pytest import MonkeyPatch, fixture

from src.core.auth.deps import check_scopes
from src.crud.user import user as CRUD
from src.main import app
from src.models.user import User

from .conftest import IncludeKeys

client = TestClient(app)
BASE_PATH = "/auth"


@fixture
def user() -> dict[str, Any]:
    return {
        "id": 1,
        "username": "randuser",
        "email": "randuser@testmail.com",
        "password": "Tespass1234.",
        "scopes": [],
        "disabled": False,
        "created_at": "2023-10-27T15:58:51.928350",
        "updated_at": "2023-10-28T16:58:51.928350",
    }


@fixture
def user_model(user) -> User:
    user[
        "password"
    ] = "$argon2i$v=19$m=16,t=2,p=1$N2pFZUxiVDhYbzR3NWN3eQ$XQUnaQ4/VzoBkQ7KpUo/WQ"
    return User(
        **user,
    )


@fixture
def override_auth() -> Generator[None, None, None]:
    default_root_user = {
        "id": 1,
        "username": "rootuser",
    }

    def override_check_scopes():
        return default_root_user

    app.dependency_overrides[check_scopes] = override_check_scopes

    yield None

    app.dependency_overrides = {}


class TestSignUp:
    def test_create_account(
        self,
        user: dict[str, Any],
        user_model: User,
        include_keys: IncludeKeys,
        jwt_token: str,
        override_auth,
        monkeypatch: MonkeyPatch,
    ):
        monkeypatch.setattr(CRUD, CRUD.get_by_username.__name__, lambda _db, _: None)
        monkeypatch.setattr(CRUD, CRUD.create.__name__, lambda _db, **_args: user_model)
        monkeypatch.setattr("src.api.endpoints.auth.encode_token", lambda _: jwt_token)
        iuser = include_keys(user, ["username", "email", "password"])

        response = client.post(f"{BASE_PATH}/signup", json=iuser)

        assert response.json() == {"token": jwt_token}

    def test_require_authentication(self):
        response = client.post(
            f"{BASE_PATH}/signup",
            json={},
        )

        assert (
            "Not authenticated" in response.json()
        )  # TODO: Return a dictionay instead


class TestSignIn:
    def test_get_authenticated(
        self,
        user: dict[str, Any],
        user_model: User,
        jwt_token: str,
        include_keys: IncludeKeys,
        monkeypatch: MonkeyPatch,
    ):
        monkeypatch.setattr(
            CRUD, CRUD.authenticate.__name__, lambda _db, *args: user_model
        )
        monkeypatch.setattr("src.api.endpoints.auth.encode_token", lambda _: jwt_token)
        iuser = include_keys(user, ["username", "password"])

        response = client.post(f"{BASE_PATH}/signin", json=iuser)

        assert response.json() == {"token": jwt_token}

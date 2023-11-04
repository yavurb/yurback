from typing import Any, Generator

from fastapi.testclient import TestClient
from pytest import MonkeyPatch, fixture

from src.core.auth.deps import check_scopes
from src.crud.post import post as CRUD
from src.main import app
from src.models.post import Post

client = TestClient(app)
BASE_PATH = "/posts"


@fixture
def post() -> dict[str, Any]:
    return {
        "id": 1,
        "title": "How to deploy an AWS EC2 instance",
        "author": "Claudia Frazier",
        "slug": "post-how-to-build-a-website",
        "status": "editing",
        "description": "This article discuses how to build a website",
        "content": "## Nice Title",
        "created_at": "2023-10-27T15:58:51.928350",
        "updated_at": "2023-10-28T16:58:51.928350",
        "published_at": None,
    }


@fixture
def post_models(post) -> list[Post]:
    def make_instances(post_data: dict[str, Any]) -> Post:
        return Post(**post_data)

    return list(map(make_instances, [post]))


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


class TestGetPostOperation:
    def test_return_all_posts(
        self,
        post: dict[str, Any],
        post_models: list[Post],
        monkeypatch: MonkeyPatch,
    ):
        monkeypatch.setattr(CRUD, CRUD.get_multi.__name__, lambda _db: post_models)

        response = client.get(BASE_PATH)

        assert response.json() == {"data": [post]}


class TestGetSinglePost:
    def test_get_post(self, post: dict[str, Any], monkeypatch: MonkeyPatch):
        monkeypatch.setattr(
            CRUD, CRUD.get_by_id.__name__, lambda _db, _id: Post(**post)
        )

        response = client.get(f"{BASE_PATH}/1")

        assert response.json() == post


class TestCreatePostOperation:
    def test_create_post(
        self,
        post,
        post_models,
        override_auth,
        monkeypatch: MonkeyPatch,
    ):
        monkeypatch.setattr(CRUD, CRUD.get.__name__, lambda _db, *args: None)
        monkeypatch.setattr(
            CRUD, CRUD.create.__name__, lambda _db, **kargs: post_models[0]
        )
        post_input = {**post}
        del post_input["id"]
        del post_input["published_at"]

        response = client.post(BASE_PATH, json=post_input)

        assert response.json() == post

    def test_require_authentication(self):
        response = client.post(
            BASE_PATH,
            json={},
        )

        assert (
            "Not authenticated" in response.json()
        )  # TODO: Return a dictionay instead

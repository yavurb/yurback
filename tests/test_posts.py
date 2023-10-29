from typing import Any, Callable

from fastapi.testclient import TestClient
from pytest import MonkeyPatch, fixture

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
        "published_at": "2023-10-28T18:58:51.928350",
    }


@fixture
def post_models(post) -> Callable[[Any], list[Post]]:
    def make_instances(post_data: dict[str, Any]) -> Post:
        return Post(**post_data)

    return lambda _db: (list(map(make_instances, [post])))


class TestGetPost:
    def test_should_return_all_posts(
        self,
        post,
        post_models,
        monkeypatch: MonkeyPatch,
    ):
        monkeypatch.setattr(CRUD, "get_multi", post_models)

        response = client.get(BASE_PATH)

        assert response.json() == {"data": [post]}

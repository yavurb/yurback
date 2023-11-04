from typing import Any, Generator

from fastapi.testclient import TestClient
from pytest import MonkeyPatch, fixture

from src.core.auth.deps import check_scopes
from src.crud.project import project as CRUD
from src.main import app
from src.models.project import Project

from .conftest import DeleteKeys

client = TestClient(app)
BASE_PATH = "/projects"


@fixture
def project() -> dict[str, Any]:
    return {
        "id": 1,
        "name": "This website's backend",
        "status": "editing",
        "image": "https://cdn.yurb.dev/catto.jpeg",
        "url": "https://api.yurb.dev/docs",
        "description": "A blog-like backend to serve content to yurb.dev 🐙",
        "tags": ["Python", "AWS", "FastAPI", "PostgreSQL"],
        "post_id": None,
        "created_at": "2023-10-27T15:58:51.928350",
        "updated_at": "2023-10-28T16:58:51.928350",
    }


@fixture
def project_models(project) -> list[Project]:
    def make_instances(project_data: dict[str, Any]) -> Project:
        return Project(**project_data)

    return list(map(make_instances, [project]))


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


class TestGetProjectsOperation:
    def test_get_all_projects(
        self,
        project: dict[str, Any],
        project_models: list[Project],
        monkeypatch: MonkeyPatch,
    ):
        monkeypatch.setattr(CRUD, CRUD.get_multi.__name__, lambda _db: project_models)

        response = client.get(BASE_PATH)

        assert response.json() == {"data": [project]}


class TestGetSingleProject:
    def test_get_project(self, project: dict[str, Any], monkeypatch: MonkeyPatch):
        monkeypatch.setattr(
            CRUD, CRUD.get_by_id.__name__, lambda _db, _id: Project(**project)
        )

        response = client.get(f"{BASE_PATH}/1")

        assert response.json() == project


class TestCreateProjectOperation:
    def test_create_project(
        self,
        project,
        project_models,
        override_auth,
        delete_keys: DeleteKeys,
        monkeypatch: MonkeyPatch,
    ):
        monkeypatch.setattr(CRUD, CRUD.get.__name__, lambda _db, *args: None)
        monkeypatch.setattr(
            CRUD, CRUD.create.__name__, lambda _db, **kargs: project_models[0]
        )
        post_input = {**project}
        delete_keys(post_input, ["id", "post_id", "status", "created_at", "updated_at"])

        print(post_input)

        response = client.post(BASE_PATH, json=post_input)

        assert response.json() == project

    def test_require_authentication(self):
        response = client.post(
            BASE_PATH,
            json={},
        )

        assert (
            "Not authenticated" in response.json()
        )  # TODO: Return a dictionay instead

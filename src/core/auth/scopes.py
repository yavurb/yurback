from enum import Enum


class Scope(Enum):
    CREATE_POST = "posts:create"
    UPDATE_POST = "posts:update"
    DELETE_POST = "posts:delete"

    CREATE_PROJECT = "projects:create"
    UPDATE_PROJECT = "projects:update"
    DELETE_PROJECT = "projects:delete"

    AUTH_CREATE = "auth:create"

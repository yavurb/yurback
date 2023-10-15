from enum import Enum


class Scope(Enum):
    CREATE_PROJECT = "projects:create"
    UPDATE_PROJECT = "projects:update"
    DELETE_PROJECT = "projects:delete"

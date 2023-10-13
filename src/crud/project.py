from src.crud.base import CRUDBase
from src.models.project import Project
from src.schemas.project import ProjectCreate, ProjectUpdate


class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    pass


project = CRUDProject(Project)

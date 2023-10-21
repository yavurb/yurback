from src.crud.base import CRUDBase
from src.models.project import Project
from src.schemas.project import ProjectCreate, ProjectUpdate, QuerySchema


class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate, QuerySchema]):
    pass


project = CRUDProject(Project)

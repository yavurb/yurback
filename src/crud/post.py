from src.crud.base import CRUDBase
from src.models.post import Post
from src.schemas.post import PostCreate, PostUpdate, QuerySchema


class CRUDPost(CRUDBase[Post, PostCreate, PostUpdate, QuerySchema]):
    pass


post = CRUDPost(Post)

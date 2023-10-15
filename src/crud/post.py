from src.crud.base import CRUDBase
from src.models.post import Post
from src.schemas.post import PostCreate, PostUpdate


class CRUDPost(CRUDBase[Post, PostCreate, PostUpdate]):
    pass


post = CRUDPost(Post)

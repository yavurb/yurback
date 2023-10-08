from crud.base import CRUDBase
from models.post import Post
from schemas.post import PostCreate, PostUpdate


class CRUDPost(CRUDBase[Post, PostCreate, PostUpdate]):
    pass


post = CRUDPost(Post)

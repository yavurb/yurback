from src.crud.base import CRUDBase
from src.models.post import Post
from src.schemas.post import Post as PostSchema
from src.schemas.post import PostCreate, PostUpdate, QuerySchema


class CRUDPost(
    CRUDBase[
        Post,
        PostSchema,
        PostCreate,
        PostUpdate,
        QuerySchema,
    ]
):
    pass


post = CRUDPost(Post, PostSchema)

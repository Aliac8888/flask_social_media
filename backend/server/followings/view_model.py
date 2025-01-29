from pydantic import BaseModel

from server.model_utils import ObjectIdStr


class Following(BaseModel):
    follower_id: ObjectIdStr
    following_id: ObjectIdStr

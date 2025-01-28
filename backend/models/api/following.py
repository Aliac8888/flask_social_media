from pydantic import BaseModel

from models.mongo import ObjectIdStr


class Following(BaseModel):
    follower_id: ObjectIdStr
    following_id: ObjectIdStr

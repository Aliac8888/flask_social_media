"""Models for User Followings API."""

from pydantic import BaseModel

from server.model_utils import ObjectIdStr


class Following(BaseModel):
    """User following."""

    follower_id: ObjectIdStr
    following_id: ObjectIdStr

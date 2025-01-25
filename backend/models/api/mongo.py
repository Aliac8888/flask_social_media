from typing import Annotated

from bson.objectid import ObjectId
from pydantic import AfterValidator, AliasChoices, BeforeValidator, Field


class InvalidObjectIdError(ValueError):
    def __init__(self, value: str) -> None:
        super().__init__(f"Invalid ObjectId: {value}")


def ensure_str(value: str | ObjectId) -> str:
    return str(value) if isinstance(value, ObjectId) else value


def check_object_id(value: str) -> str:
    if not ObjectId.is_valid(value):
        raise InvalidObjectIdError(value)

    return value


ObjectIdStr = Annotated[
    str,
    BeforeValidator(ensure_str),
    AfterValidator(check_object_id),
]

SelfIdStr = Annotated[ObjectIdStr, Field(validation_alias=AliasChoices("id", "_id"))]

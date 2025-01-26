from typing import Annotated

from bson.errors import InvalidId
from bson.objectid import ObjectId
from pydantic import (
    AliasChoices,
    BeforeValidator,
    Field,
    GetPydanticSchema,
    PlainSerializer,
)
from pydantic_core.core_schema import any_schema, str_schema


class InvalidObjectIdError(ValueError):
    def __init__(self, value: str | ObjectId) -> None:
        super().__init__(f"Invalid ObjectId: {value!r}")


def to_oid(value: str | ObjectId) -> ObjectId:
    try:
        return ObjectId(value)
    except InvalidId as e:
        raise InvalidObjectIdError(value) from e


ObjectIdRaw = Annotated[
    ObjectId,
    GetPydanticSchema(
        lambda _tp, _handler: any_schema(),
        lambda _tp, handler: handler(str_schema()),
    ),
    BeforeValidator(to_oid),
]

ObjectIdStr = Annotated[
    ObjectIdRaw,
    PlainSerializer(str),
]

SelfIdRaw = Annotated[
    ObjectIdRaw,
    Field(
        validation_alias=AliasChoices("id", "_id"),
        serialization_alias="_id",
    ),
]
SelfIdStr = Annotated[
    ObjectIdStr,
    Field(
        validation_alias=AliasChoices("id", "_id"),
    ),
]

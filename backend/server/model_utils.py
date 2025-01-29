from datetime import UTC, datetime
from typing import Annotated

from bson.errors import InvalidId
from bson.objectid import ObjectId
from pydantic import (
    AfterValidator,
    AliasChoices,
    BaseModel,
    BeforeValidator,
    Field,
    GetPydanticSchema,
    PlainSerializer,
)
from pydantic_core.core_schema import any_schema, str_schema

Instant = Annotated[
    datetime,
    AfterValidator(lambda x: x.astimezone(tz=UTC)),
    PlainSerializer(lambda x: x.strftime("%Y-%m-%dT%H:%M:%SZ")),
]


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


class EmptyPatchError(ValueError):
    def __init__(self) -> None:
        super().__init__("Patch is empty")


def model_convert[T: BaseModel](target: type[T], value: BaseModel) -> T:
    return target.model_validate(value.model_dump(by_alias=True))

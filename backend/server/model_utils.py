"""Helpers for defining and user Pydantic models."""

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
"""A point in time, relative to UTC, stored as an ISO 8601 string."""


class InvalidObjectIdError(ValueError):
    """Given ObjectId was invalid."""

    def __init__(self, value: str | ObjectId) -> None:
        """Represent an invalid ObjectId.

        Args:
            value (str | ObjectId): Given ObjectId.

        """
        super().__init__(f"Invalid ObjectId: {value!r}")


def to_oid(value: str | ObjectId) -> ObjectId:
    """Convert the given value to an ObjectId object.

    Args:
        value (str | ObjectId): Value to convert.

    Raises:
        InvalidObjectIdError: Value cannot be converted to an ObjectId.

    Returns:
        ObjectId: Converted ObjectId.

    """
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
"""Raw ObjectId, also deserializes string into ObjectId."""

ObjectIdStr = Annotated[
    ObjectIdRaw,
    PlainSerializer(str),
]
"""Stringified ObjectId, also deserializes string into ObjectId."""

SelfIdRaw = Annotated[
    ObjectIdRaw,
    Field(
        validation_alias=AliasChoices("id", "_id"),
        serialization_alias="_id",
    ),
]
"""Raw ObjectId with alias for `id`, also deserializes string into ObjectId."""

SelfIdStr = Annotated[
    ObjectIdStr,
    Field(
        validation_alias=AliasChoices("id", "_id"),
    ),
]
"""Stringified ObjectId with alias for `_id`, also deserializes string into ObjectId."""


class EmptyPatchError(ValueError):
    """The requested modification is empty."""

    def __init__(self) -> None:
        """Represent an empty modification."""
        super().__init__("Patch is empty")


def model_convert[T: BaseModel](target: type[T], value: BaseModel) -> T:
    """Convert a Pydantic model instance into another Pydantic model.

    Raises:
        ValidationError: Could not convert between the models.

    Returns:
        T: Instance of the other pydantic model.

    """
    return target.model_validate(value.model_dump(by_alias=True))

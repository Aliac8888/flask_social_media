from typing import Annotated, Any
from pydantic import AfterValidator, AliasChoices, BeforeValidator, Field
from bson import ObjectId


def ensure_str(value: Any):
    return str(value) if isinstance(value, ObjectId) else value


def check_object_id(value: str) -> str:
    if not ObjectId.is_valid(value):
        raise ValueError("Invalid ObjectId")

    return value


ObjectIdStr = Annotated[
    str, BeforeValidator(ensure_str), AfterValidator(check_object_id)
]

SelfIdStr = Annotated[ObjectIdStr, Field(validation_alias=AliasChoices("id", "_id"))]

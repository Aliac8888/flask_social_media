from typing import Annotated, Any

from bson.objectid import ObjectId
from pydantic import AliasChoices, Field, GetPydanticSchema
from pydantic_core import core_schema

ObjectIdRaw = Annotated[
    ObjectId,
    GetPydanticSchema(
        lambda _tp, handler: core_schema.no_info_after_validator_function(
            ObjectId, handler(Any)
        )
    ),
]

SelfIdRaw = Annotated[ObjectIdRaw, Field(validation_alias=AliasChoices("_id", "id"))]

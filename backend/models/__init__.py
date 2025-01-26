from pydantic import BaseModel


def model_convert[T: BaseModel](target: type[T], value: BaseModel) -> T:
    return target.model_validate(value.model_dump(by_alias=True))

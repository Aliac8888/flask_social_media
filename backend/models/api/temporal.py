from datetime import UTC, datetime
from typing import Annotated

from pydantic import AfterValidator, PlainSerializer

Instant = Annotated[
    datetime,
    AfterValidator(lambda x: x.astimezone(tz=UTC)),
    PlainSerializer(lambda x: x.strftime("%Y-%m-%dT%H:%M:%SZ")),
]

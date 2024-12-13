from os import getenv
from dotenv import load_dotenv


def non_falsy[T](value: T | None) -> T:
    assert value
    return value


load_dotenv()

db_user = non_falsy(getenv("SOCIAL_BE_DB_USER"))
db_pass = non_falsy(getenv("SOCIAL_BE_DB_PASS"))
db_host = non_falsy(getenv("SOCIAL_BE_DB_HOST"))
db_port = int(non_falsy(getenv("SOCIAL_BE_DB_PORT")))

be_host = non_falsy(getenv("SOCIAL_BE_HOST"))
be_port = int(non_falsy(getenv("SOCIAL_BE_PORT")))

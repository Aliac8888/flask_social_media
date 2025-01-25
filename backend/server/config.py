from os import getenv

from dotenv import load_dotenv


def non_falsy[T](value: T | None) -> T:
    if not value:
        raise AssertionError

    return value


load_dotenv()

maintenance = getenv("SOCIAL_BE_MAINTENANCE") == "1"

db_root_user = getenv("SOCIAL_DB_ROOT_USER", "")
db_root_pass = getenv("SOCIAL_DB_ROOT_PASS", "")

db_backend_user = non_falsy(getenv("SOCIAL_BE_DB_USER"))
db_backend_pass = non_falsy(getenv("SOCIAL_BE_DB_PASS"))

db_user = db_root_user if maintenance else db_backend_user
db_pass = db_root_pass if maintenance else db_backend_pass

db_host = non_falsy(getenv("SOCIAL_BE_DB_HOST"))
db_port = int(non_falsy(getenv("SOCIAL_BE_DB_PORT")))

be_host = non_falsy(getenv("SOCIAL_BE_HOST"))
be_port = int(non_falsy(getenv("SOCIAL_BE_PORT")))

fe_url = non_falsy(getenv("SOCIAL_BE_FE_URL"))

jwt_secret = non_falsy(getenv("SOCIAL_BE_JWT_SECRET"))
jwt_expiry = int(getenv("SOCIAL_BE_JWT_EXPIRY") or "0")

admin_email = non_falsy(getenv("SOCIAL_BE_ADMIN_EMAIL"))
admin_pass = non_falsy(getenv("SOCIAL_BE_ADMIN_PASS"))

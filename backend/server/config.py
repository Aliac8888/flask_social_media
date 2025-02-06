"""Server config loader."""

from os import getenv

from dotenv import load_dotenv


class MissingEnvError(ValueError):
    """Required environment variable was missing."""

    def __init__(self, name: str) -> None:
        """Represent a missing environment variable."""
        super().__init__(
            f"Required environment variable {name} was not defined (or was empty)."
        )


def getenv_required(name: str) -> str:
    """Get a required environment variable.

    Args:
        name (str): variable name.

    Raises:
        MissingEnvError: variable was None or an empty string.

    Returns:
        str: variable value.

    """
    value = getenv(name)

    if not value:
        raise MissingEnvError(name)

    return value


load_dotenv()

maintenance = getenv("SOCIAL_BE_MAINTENANCE") == "1"
"""Is maintenance mode enabled."""

db_root_user = getenv("SOCIAL_DB_ROOT_USER", "")
"""Database root username. Prefer using the effective user/pass."""
db_root_pass = getenv("SOCIAL_DB_ROOT_PASS", "")
"""Database root password. Prefer using the effective user/pass."""

db_backend_user = getenv_required("SOCIAL_BE_DB_USER")
"""Database backend username. Prefer using the effective user/pass."""
db_backend_pass = getenv_required("SOCIAL_BE_DB_PASS")
"""Database backend password. Prefer using the effective user/pass."""

db_user = db_root_user if maintenance else db_backend_user
"""Database effective username."""
db_pass = db_root_pass if maintenance else db_backend_pass
"""Database effective password."""

db_host = getenv_required("SOCIAL_BE_DB_HOST")
"""Database hostname."""
db_port = int(getenv_required("SOCIAL_BE_DB_PORT"))
"""Database port."""

be_host = getenv_required("SOCIAL_BE_HOST")
"""Internal backend hostname."""
be_port = int(getenv_required("SOCIAL_BE_PORT"))
"""Internal backend port."""

fe_url = getenv_required("SOCIAL_BE_FE_URL")
"""Public frontend URL."""

jwt_secret = getenv_required("SOCIAL_BE_JWT_SECRET")
"""Secret key for JWT tokens."""
jwt_expiry = int(getenv("SOCIAL_BE_JWT_EXPIRY") or "0")
"""Expiry time of JWT tokens."""

admin_email = getenv_required("SOCIAL_BE_ADMIN_EMAIL")
"""Admin account email."""
admin_pass = getenv_required("SOCIAL_BE_ADMIN_PASS")
"""Admin account password."""

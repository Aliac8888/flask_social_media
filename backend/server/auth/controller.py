"""Controller of Authentication/Authorization."""

from bson.objectid import ObjectId

from server.auth.controller_model import AuthnFailedError
from server.plugins import bcrypt
from server.users.controller_model import DbUser


def login(email: str, password: str) -> DbUser:
    """Validate user password. Used for logging in.

    Args:
        email (str): Email address of user.
        password (str): Password of user.

    Raises:
        DbUserNotFound: No user with the given email address exists.
        AuthnFailedError: The given password is incorrect.

    Returns:
        DbUser: Validated user data.

    """
    from server.users.controller import get_user_by_email

    user = get_user_by_email(email)

    if (user.credential or password) and not bcrypt.check_password_hash(
        user.credential,
        password,
    ):
        raise AuthnFailedError

    return user


def change_password(
    user_id: ObjectId,
    password: str,
) -> None:
    """Change a user's password.

    Args:
        user_id (ObjectId): Id of user.
        password (str): New password of user.

    Raises:
        DbUserNotFoundError: No user with the given id exist.

    """
    from server.users.controller import update_user

    update_user(
        user_id,
        credential=bcrypt.generate_password_hash(password) if password else b"",
    )


def signup(
    name: str,
    email: str,
    password: str,
) -> DbUser:
    """Create a new user.

    Args:
        name (str): Name of user.
        email (str): Email address of user.
        password (str): Password of user.

    Raises:
        DbUserExistsError: User with given email address already exists.

    Returns:
        DbUser: Created user.

    """
    from server.users.controller import create_user

    credential = bcrypt.generate_password_hash(password) if password else b""

    return create_user(
        name=name,
        email=email,
        credential=credential,
    )

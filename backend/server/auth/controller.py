from bson.objectid import ObjectId

from server.auth.controller_model import AuthnFailedError
from server.plugins import bcrypt
from server.users.controller_model import DbUser


def login(email: str, password: str) -> DbUser:
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
    from server.users.controller import create_user

    credential = bcrypt.generate_password_hash(password) if password else b""

    return create_user(
        name=name,
        email=email,
        credential=credential,
    )

from models.db.auth import AuthFailedError
from models.db.user import DbUser
from server.plugins import bcrypt


def login(email: str, password: str) -> DbUser:
    from controllers.user import get_user_by_email

    user = get_user_by_email(email)

    if (user.credential or password) and not bcrypt.check_password_hash(
        user.credential,
        password,
    ):
        raise AuthFailedError

    return user


def signup(
    name: str,
    email: str,
    password: str,
) -> DbUser:
    from controllers.user import create_user

    credential = bcrypt.generate_password_hash(password) if password else b""

    return create_user(
        name=name,
        email=email,
        credential=credential,
    )

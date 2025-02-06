from flask.app import Flask

__version_info__: tuple[str, ...] = ("1", "0", "1")
__version__: str = "1.0.1"
__author__: str = "Max Countryman"
__license__: str = "BSD"
__copyright__: str = "(c) 2011 by Max Countryman"

__all__ = ["Bcrypt", "check_password_hash", "generate_password_hash"]

def generate_password_hash(
    password: str | bytes, rounds: int | None = None
) -> bytes: ...
def check_password_hash(pw_hash: bytes, password: str | bytes) -> bool: ...

class Bcrypt(object):  # noqa: UP004
    def __init__(self, app: Flask | None = None) -> None: ...
    def init_app(self, app: Flask) -> None: ...
    def generate_password_hash(
        self,
        password: str | bytes,
        rounds: int | None = None,
        prefix: str | None = None,
    ) -> bytes: ...
    def check_password_hash(self, pw_hash: bytes, password: str | bytes) -> bool: ...

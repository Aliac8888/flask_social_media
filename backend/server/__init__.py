import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from server.app import create_app

__all__ = ["create_app"]

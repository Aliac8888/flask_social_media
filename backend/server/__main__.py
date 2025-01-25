import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from server.app import create_app
from server.config import be_host, be_port

create_app().run(be_host, be_port, debug=True)

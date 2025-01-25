from app import create_app
from config import be_host, be_port

create_app().run(be_host, be_port, debug=True)

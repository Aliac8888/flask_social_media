# Chamran Social

Backend Stack:

- <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/flask/flask-original.svg" alt="" height="16px"> Flask: WSGI Web Server
- <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/openapi/openapi-plain.svg" alt="" height="16px"> Flask-OpenAPI3: OpenAPI Generator
- <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/mongodb/mongodb-original.svg" alt="" height="16px"> Pymongo: MongoDB Client
- <img src="https://docs.pydantic.dev/latest/favicon.png" alt="" height="16px"> Pydantic: Data Validation and Serialization
- <img src="https://docs.astral.sh/uv/assets/logo-letter.svg" alt="" height="16px"> UV: Package and Project Manager

Frontend Stack:

- <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/typescript/typescript-original.svg" alt="" height="16px"> TypeScript: Type Checking
- <img src="https://heyapi.dev/images/logo-48w.png" alt="" height="16px"> Hey API: Type-Safe Fetch API
- <img src="https://preactjs.com/branding/symbol.svg" alt="" height="16px"> Preact: UI Library
- <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/vitejs/vitejs-original.svg" alt="" height="16px"> Vite: Bundler
- <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/pnpm/pnpm-original.svg" alt="" height="16px"> pnpm: Package and Project Manager

## Setup

- `git clone https://github.com/Aliac8888/flask_social_media.git`
- `cd flask_social_media`
- edit `.env`
- `docker-compose up -d` (Runs database)
- `cd backend`
- `uv sync`
- `SOCIAL_BE_MAINTENANCE=1 uv run tasks/setup.py`
- `uv run server &` (Runs backend)
- `cd ../frontend`
- `pnpm install`
- `pnpm vite &` (Runs frontend)

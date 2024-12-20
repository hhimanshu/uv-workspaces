# Quick Start Guide

Essential commands to work with the UV Workspaces project.

## Setup

Create and activate a virtual environment:

```bash
# Create virtual environment
uv venv

# Activate on Unix/macOS
source .venv/bin/activate

# Activate on Windows
.venv\Scripts\activate
```

Install dependencies and configure development environment:

```bash
python -m scripts.setup
```

## Run Server

Start the development server:

```bash
python -m scripts.dev
```

The API will be available at:

- API Documentation: http://localhost:8000/docs
- OpenAPI Schema: http://localhost:8000/openapi.json

## Run Tests

```bash
# Run all tests
python -m scripts.test

# Run only API tests
python -m scripts.test api

# Run only app tests
python -m scripts.test app
```

## Next Steps

- Restructure the code.
  - Move `packages/services` to `app/services`.
    - Ensure the tests are working that depend on TestContainer.
  - In `api/`, create routes per project such as `platform`, `cc` (meaning clean carrot), etc
  - Rename `app` workspace to `platform`.
- Develop API endpoints for users (finding the glue between openapi and fastapi).
  - Create `fastapi` code in `api/` for user endpoints.
    - Create necessary `dto`, `routes` and `services` for user endpoints.
    - Write tests for user endpoints.
    - Document the process.
  - **Note**: The `openapi/` directory is for the OpenAPI schema. This is generated using [`tspec101`](https://github.com/hhimanshu/tspec101) codebase.

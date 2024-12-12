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

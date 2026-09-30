# MyApp

FastAPI application managed with [uv](https://docs.astral.sh/uv/).

## Setup

```bash
./scripts/setup.sh
```

## Development

```bash
uv run fastapi dev
```

## Validation

Run all checks:

```bash
uv run task validate
```

This runs linting, formatting, type checking, and tests.

## Tasks

```bash
uv run task lint
uv run task format
uv run task typecheck
uv run task test
uv run task validate
```

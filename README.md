# Flow Manager

FastAPI microservice that executes sequential task flows with condition-based routing.

## Flow Design

A **flow** is a directed graph defined by tasks and conditions:

- **Tasks** are async handlers registered via `@task_handler("name")`. Each receives accumulated context (outputs of previous tasks) and returns a result dict. Raising = failure.
- **Conditions** connect tasks. After a task completes, the engine finds its outgoing condition and routes to `target_task_success` or `target_task_failure`. `None` ends the flow.

```
task1 ──success──► task2 ──success──► task3
  │                   │                  │
  failure             failure            failure
  │                   │                  │
  ▼                   ▼                  ▼
  end                 end                end
```

If a task fails and has no `target_task_failure`, the flow ends as failed. Conditions can also route to rollback/cleanup tasks on failure.

## API

All endpoints under `/api/v1`.

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/flow/` | Create flow definition |
| GET | `/api/v1/flow/` | List flows |
| GET | `/api/v1/flow/{flow_id}` | Get flow |
| PUT | `/api/v1/flow/{flow_id}` | Update flow |
| DELETE | `/api/v1/flow/{flow_id}` | Delete flow |
| POST | `/api/v1/flow/{flow_id}/execute` | Execute a flow |
| GET | `/api/v1/execution/` | List executions (`?flow_id=` filter) |
| GET | `/api/v1/execution/{id}/` | Get execution |

## Project Structure

```
app/
  main.py                          # FastAPI app
  api/v1/                          # Versioned routers
  modules/
    flows/                         # Flow definitions
      models.py, repository.py, service.py, executor.py
    executions/                    # Execution tracking
      models.py, repository.py, service.py
    tasks/                         # Task handlers
      models.py, repository.py, handlers.py, utils.py
tests/
  unit/                            # Isolated tests (mocked deps)
  integration/                     # Service + repo tests (real deps)
  e2e/                             # Full HTTP stack tests
```

## Quick Start

```bash
python -m venv .venv           # Create virtual environment
source .venv/bin/activate      # Activate it
pip install poetry
poetry install                 # Install dependencies
```

```bash
make run        # Start server on :8000
make test       # All tests
make test-unit  # Unit tests only
make lint       # Ruff check
make format     # Ruff format
```
from app.modules.tasks.utils import task_handler


@task_handler("task1")
async def fetch_data(context: dict) -> dict:
    return {"raw_data": [1, 2, 3], "source": "api"}


@task_handler("task2")
async def process_data(context: dict) -> dict:
    raw = context.get("task1", {}).get("raw_data", [])
    processed = [x * 10 for x in raw]
    return {"processed_data": processed, "count": len(processed)}


@task_handler("task3")
async def store_data(context: dict) -> dict:
    processed = context.get("task2", {}).get("processed_data", [])
    return {"stored": True, "records_written": len(processed)}

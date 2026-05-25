from typing import Callable, Any, Coroutine

TaskHandler = Callable[[dict[str, Any]], Coroutine[Any, Any, dict[str, Any]]]

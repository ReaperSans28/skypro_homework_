from typing import Any, Callable, Dict, Optional, Tuple


def log(file_name: Optional[str] = None) -> Callable[[Callable], Callable]:
    def decorator(func: Callable) -> Callable:

        def decorator_(*args: Tuple[Any], **kwargs: Dict[str, Any]) -> Any:
            try:
                result = func(*args, **kwargs)
            except Exception as error:
                log_message = f"2018-10-31 20:31:00 {func.__name__} error: {error}. Inputs: {args}, {kwargs}\n"
            else:
                log_message = f"2018-10-31 20:31:00 {func.__name__} ok\n"

            if file_name is not None:
                try:
                    with open(file_name, "a") as file:
                        file.write(log_message)
                except FileNotFoundError:
                    print(log_message)
            else:
                print(log_message)

            return result

        return decorator_

    return decorator


@log(file_name="")
def my_function(x: int, y: int) -> int:
    return x + y

from typing import Any, Callable, Dict, Tuple


def log(file_name: str) -> Callable[[Callable], Callable]:
    """
    Функция принимающая имя файла.
    """
    def decorator(func: Callable) -> Callable:
        """
        Функция принимающая функцию my_function.
        """
        def decorator_(*args: Tuple[Any], **kwargs: Dict[str, Any]) -> Any:
            """
            Функция проверяющая результат работы функции my_function и записывающая его в mylog.txt.
            """
            try:
                result = func(*args, **kwargs)
            except Exception as error:
                with open(file_name, "a") as file:
                    file.write(f"2018-10-31 20:31:00 {func.__name__} error: {error}. Inputs: {args}, {kwargs}\n")
            else:
                with open(file_name, "a") as file:
                    file.write(f"2018-10-31 20:31:00 {func.__name__} ok\n")
                return result

        return decorator_

    return decorator


@log(file_name="mylog.txt")
def my_function(x: int, y: int) -> int:
    """
    Функция сложения двух чисел.
    """
    return x + y

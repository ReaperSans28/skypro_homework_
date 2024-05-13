from typing import Any, Callable, Dict, Tuple, Optional


def log(file_name: Optional[str] = None) -> Callable[[Callable], Callable]:
    """
    Функция принимающая имя файла, если имени нет, то все выведется в консоль.
    """

    def decorator(func: Callable) -> Callable:
        """
        Функция принимающая функцию my_function.
        """

        def decorator_(*args: Tuple[Any], **kwargs: Dict[str, Any]) -> Any:
            """
            Функция проверяющая результат работы функции my_function и записывающая его в указанный файл
            Если файла нет, то вывод происходит в консоль.
            """
            try:
                result = func(*args, **kwargs)
            except Exception as error:
                try:
                    with open(file_name, "a") as file:
                        file.write(f"2018-10-31 20:31:00 {func.__name__} error: {error}. Inputs: {args}, {kwargs}\n")
                except FileNotFoundError:
                    print(f"2018-10-31 20:31:00 {func.__name__} error: {error}. Inputs: {args}, {kwargs}\n")
            else:
                try:
                    with open(file_name, "a") as file:
                        file.write(f"2018-10-31 20:31:00 {func.__name__} ok\n")
                except FileNotFoundError:
                    print(f"2018-10-31 20:31:00 {func.__name__} ok")
                return result

        return decorator_

    return decorator


@log(file_name="")
def my_function(x: int, y: int) -> int:
    """
    Функция сложения двух чисел.
    """
    return x + y

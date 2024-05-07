from src.decorators import my_function

file_data = [
    "2018-10-31 20:31:00 my_function ok",
    "2018-10-31 20:31:00 my_function error: unsupported operand type(s) for +: 'int' and 'dict'. Inputs: (1, {}), {}",
]


def write_to_file(file_path: str, content: str) -> None:
    with open(file_path, "w") as file:
        file.write(content)


def test_write_to_file() -> None:
    file_path = "mylog.txt"

    my_function(1, 2)
    my_function(1, {})

    with open(file_path, "r") as file:
        assert file_data[0] in file.read()
    with open(file_path, "r") as file:
        assert file_data[1] in file.read()

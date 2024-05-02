from src.masks import mask_account_number, mask_card_number


def convert_date_(input_date: str) -> str:
    """
    Функция выдает нам дату.
    """
    date_parts = input_date.split("T")[0].split("-")
    return f"{date_parts[2]}.{date_parts[1]}.{date_parts[0]}"


def number_or_account(user_input: str) -> str:
    """
    Функция определяет работаем мы с счетом или картой.
    """
    if "Счет" in user_input:
        return f"Счет {mask_account_number(user_input)}"
    else:
        user_card = user_input.split()
        card_name = user_card[:-1]
        card_number = user_card[-1]
        return " ".join(card_name) + " " + mask_card_number(card_number)

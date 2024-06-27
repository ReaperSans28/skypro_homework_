from src.logging import logging_setup

logger = logging_setup()


def mask_card_number(user_card_number: str) -> str:
    """
    Функция принимает номер банковской карты и возвращает ее маску.
    """
    if len(user_card_number) == 16:
        masked_number = user_card_number[:4] + " " + user_card_number[4:6] + "** **** " + user_card_number[12:]
        logger.info("Сработала mask_card_number")
        return masked_number
    else:
        logger.error("Не сработала mask_card_number")
        return "Неа"


def mask_account_number(user_account_number: str) -> str:
    """
    Функция принимает номер счета и возвращает маску счета.
    """
    if user_account_number:
        masked_number = "**" + user_account_number[-4:]
        logger.info("Сработала mask_account_number")
        return masked_number
    else:
        logger.error("Не сработала mask_account_number")
        return "Неа"

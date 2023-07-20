from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

FRAZES = {
    "create_offer": "Создать предложение",
    "confirm_offer_yes": "Да",
    "confirm_offer_no": "Нет",
    "example_offer": "Пример предложения"
}


def kb_create_offer():
    return InlineKeyboardMarkup(row_width=1, resize_keyboard=True).add(
        InlineKeyboardButton(
            FRAZES["create_offer"],
            callback_data="create_offer"
        )
    )


def kb_confirm_offer():
    return InlineKeyboardMarkup(row_width=2, resize_keyboard=True).add(
        InlineKeyboardButton(
            FRAZES["confirm_offer_yes"],
            callback_data="confirm_next"
        ),
        InlineKeyboardButton(
            FRAZES["confirm_offer_no"],
            callback_data="offer_cancel"
        )
    )


def kb_example_offer_and_create():
    return InlineKeyboardMarkup(row_width=1, resize_keyboard=True).add(
        InlineKeyboardButton(
            FRAZES["example_offer"],
            callback_data="example_offer"
        ),
        InlineKeyboardButton(
            FRAZES["create_offer"],
            callback_data="create_offer"
        ),
    )


def kb_example_offer():
    return InlineKeyboardMarkup(row_width=1, resize_keyboard=True).add(
        InlineKeyboardButton(
            FRAZES["example_offer"],
            callback_data="example_offer"
        )
    )

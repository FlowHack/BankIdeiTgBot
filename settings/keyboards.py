from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

FRAZES = {
    "create_offer": "Создать предложение",
    "continue_offer": "Продолжить заполнение",
    "edit_before": "Редактировать предыдущий этап",
    "stop_create_offer": "Остановить заполнение",
    "confirm_offer_yes": "Да",
    "confirm_offer_no": "Нет",
    "cancel_edit": "Отменить"
}

FIELDS = {
        0: "ФИО",
        1: "Филиал",
        2: "Должность",
        3: "Наименование предложение",
        4: "Предложение"
}


def kb_create_offer(new: bool = False) -> InlineKeyboardMarkup:
    kb_create = InlineKeyboardButton(
        FRAZES["create_offer"],
        callback_data="create_offer"
    )
    kb_continue = InlineKeyboardButton(
        FRAZES["continue_offer"],
        callback_data="create_offer"
    )
    return InlineKeyboardMarkup(row_width=1, resize_keyboard=True).add(
        kb_create if new else kb_continue
    )


def kb_edit_before_and_stop() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)

    keyboard.add(
        InlineKeyboardButton(
            FRAZES["edit_before"],
            callback_data="edit_before"
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            FRAZES["stop_create_offer"],
            callback_data="stop_create_offer"
        )
    )
    return keyboard


def kb_cancel_edit_and_stop() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)

    keyboard.add(
        InlineKeyboardButton(
            FRAZES["cancel_edit"],
            callback_data="cancel_edit"
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            FRAZES["stop_create_offer"],
            callback_data="stop_create_offer"
        )
    )
    return keyboard


def kb_confirm_offer() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(row_width=2, resize_keyboard=True).add(
        InlineKeyboardButton(
            FRAZES["confirm_offer_yes"],
            callback_data="offer_send"
        ),
        InlineKeyboardButton(
            FRAZES["confirm_offer_no"],
            callback_data="offer_edit"
        )
    )


def kb_edit_all() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    for key, value in FIELDS.items():
        keyboard.add(
            InlineKeyboardButton(
                value,
                callback_data=f"edit_{key}"
            )
        )

    return keyboard


def kb_stop_create_offer() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(row_width=1, resize_keyboard=True).add(
        InlineKeyboardButton(
            FRAZES["stop_create_offer"],
            callback_data="stop_create_offer"
        )
    )


KEYBOARDS = {
    "create_offer": kb_create_offer(True),
    "continue_offer": kb_create_offer(),
    "edit_and_stop": kb_edit_before_and_stop(),
    "confirm_offer": kb_confirm_offer(),
    "edit_all": kb_edit_all(),
    "cancel_edit_and_stop": kb_cancel_edit_and_stop(),
    "stop_create_offer": kb_stop_create_offer()
}

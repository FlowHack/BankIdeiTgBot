from time import sleep

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import NetworkError

from data_base import UserOffer, session
from func_bot import check_field, send_offer, write_data_user
from settings import FIELDS, KEYBOARDS, REQUESTS, TOKEN

bot_api = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot_api)

req_info = REQUESTS["info"]
req_template = REQUESTS["template"]


@dp.message_handler(commands="start")
async def start_command(message: types.Message) -> None:
    """Функция обработки команды /start

    Args:
        message (types.Message): Объект сообщения
    """
    if not UserOffer.exists(message.from_user.id):
        await message.answer(
            req_info["start"],
            reply_markup=KEYBOARDS["create_offer"]
        )
        return

    await message.answer(
        req_info["start"],
        reply_markup=KEYBOARDS["continue_offer"]
    )


async def check_user(message: types.Message, user_id: int, mention: str):
    """Функция, проверяющие наличие пользователя в БД и создающая его,
    если такового нет

    Args:
        message (types.Message): Объект сообщения
        user_id (int): ID пользователя
        mention (str): Краткое имя пользователя

    Returns:
        UserOffer: Объект класса UserOffer
    """
    user, new = UserOffer.get_or_create(user_id, mention)

    if new:
        await message.answer(
            req_info["create_offer"],
            reply_markup=KEYBOARDS["stop_create_offer"]
        )
        return False
    if user.completion is False:
        user.completion = True
        session.commit()

    return user


async def create_edit_offer(
        message: types.Message, user_id: int = None, mention: str = None,
        edit: bool = False) -> None:
    """Функуия запрашивает у пользователя значения полей

    Args:
        message (types.Message): Объект сообщения
        user_id (int, optional): ID пользователя. Defaults to None.
        mention (str, optional): Краткое имя пользователя. Defaults to None.
        edit (bool, optional): Режим редактирования полей. Defaults to False.
    """
    if user_id is None:
        user_id = message.from_user.id
    if mention is None:
        mention = message.from_user.mention
    user = await check_user(message, user_id, mention)

    if not user:
        return
    if user.return_to_send:
        await message.answer(
            req_info[f"edit_offer_{user.step}"],
            reply_markup=KEYBOARDS["cancel_edit_and_stop"]
        )
        return
    if user.step == 0:
        await message.answer(
            req_info["create_offer"]
        )
        return
    if edit:
        user.step -= 1
        session.commit()

        await message.answer(
            req_info[f"edit_offer_{user.step}"],
            reply_markup=KEYBOARDS["cancel_edit_and_stop"]
        )
        return
    if user.step > 4:
        await message.answer(
            req_template["offer"].format(
                FIO=user.FIO, branch=user.branch, post=user.post,
                name_offer=user.name_offer, offer=user.offer
            ), reply_markup=KEYBOARDS["confirm_offer"]
        )
        return
    await message.answer(
        req_info[f"create_offer_{user.step}"],
        reply_markup=KEYBOARDS["edit_and_stop"]
    )


@dp.callback_query_handler(text="create_offer")
async def create_offer_btn(callback_query: types.CallbackQuery) -> None:
    """Функция обрабатывает нажатие на кнопку создания предложения

    Args:
        callback_query (types.CallbackQuery): Объект клика по кнопке
    """
    await create_edit_offer(
        callback_query.message,
        callback_query.from_user.id,
        callback_query.from_user.mention
    )


@dp.message_handler(commands="create_offer")
async def create_offer_command(message: types.Message) -> None:
    """Функция обработки команды /create_offer

    Args:
        message (types.Message): Объект сообщения
    """
    await create_edit_offer(message)


@dp.callback_query_handler(text="edit_before")
async def edit_before_btn(callback_query: types.CallbackQuery) -> None:
    """Функция обработки нажатия на кнопку редактикрования предыдущего поля

    Args:
        callback_query (types.CallbackQuery): Объект клика по кнопке
    """
    user_id = callback_query.from_user.id
    mention = callback_query.from_user.mention
    message = callback_query.message

    await create_edit_offer(message, user_id, mention, True)


@dp.callback_query_handler(text="cancel_edit")
async def cancel_edit_btn(callback_query: types.CallbackQuery) -> None:
    """Функция обработки нажатия на кнопки отмены редактирования поля

    Args:
        callback_query (types.CallbackQuery): Объект клика по кнопке
    """
    user_id = callback_query.from_user.id
    mention = callback_query.from_user.mention
    message = callback_query.message

    user = await check_user(message, user_id, mention)

    if not user:
        return
    if not await check_field(user):
        await message.answer(
            f"Вы не заполнили \"{FIELDS[user.step]}\"!\n\n" +
            "Напишите для него значение"
        )
        return
    if user.return_to_send or user.step >= 4:
        await message.answer(
            req_template["offer"].format(
                FIO=user.FIO, branch=user.branch, post=user.post,
                name_offer=user.name_offer, offer=user.offer
            ), reply_markup=KEYBOARDS["confirm_offer"]
        )
        return

    user.step += 1
    session.commit()

    await message.answer(
        req_info[f"create_offer_{user.step}"],
        reply_markup=KEYBOARDS["edit_and_stop"]
    )


@dp.callback_query_handler(text="offer_send")
async def confirm_offer_yes_btn(callback_query: types.CallbackQuery) -> None:
    """Функция обработки клика по кнопке отправки предложения

    Args:
        callback_query (types.CallbackQuery): Объект клика по кнопке
    """
    user_id = callback_query.from_user.id
    message = callback_query.message

    try:
        await send_offer(user_id)
        await message.answer(
            req_info["confirm_offer_yes"],
            reply_markup=KEYBOARDS["create_offer"]
        )
    except ValueError as error:
        await message.answer(
            str(error), reply_markup=KEYBOARDS["create_offer"]
        )
        print(str(error))
    except Exception as error:
        await message.answer(
            "Произошла непредвиденная ошибка. Попробуйте позже."
        )
        print(str(error))


@dp.callback_query_handler(text="offer_edit")
async def confirm_offer_no_btn(callback_query: types.CallbackQuery) -> None:
    """Функция обработки клика по кнопке отправки на редактирование всего
    предложения

    Args:
        callback_query (types.CallbackQuery): Объект клика по кнопке
    """
    user = await check_user(
        callback_query.message,
        callback_query.from_user.id,
        callback_query.from_user.mention
    )
    if not user:
        return
    if None in [user.FIO, user.branch, user.post, user.name_offer, user.offer]:
        UserOffer.delete_by_id(user.user_id)
        await callback_query.message.answer(
            "Какие-то из полей не заполнены!\n\n" +
            "Попробуйте заполнить предложение снова.",
            reply_markup=KEYBOARDS["create_offer"]
        )
        return

    await callback_query.message.answer(
        req_info["confirm_offer_no"], reply_markup=KEYBOARDS["edit_all"]
    )


@dp.callback_query_handler(text="stop_create_offer")
async def stop_offer(callback_query: types.CallbackQuery) -> None:
    """Функция обработки кнопки прекращения заполнения полей. (Остановка)

    Args:
        callback_query (types.CallbackQuery): Объект клика по кнопке
    """
    user = UserOffer.get_by_id(callback_query.from_user.id)
    user.completion = False
    session.commit()

    create_offer = KEYBOARDS["create_offer"]
    continue_offer = KEYBOARDS["continue_offer"]

    await callback_query.message.answer(
        req_info["stop"],
        reply_markup=create_offer if user.step == 0 else continue_offer
    )


@dp.callback_query_handler(text=[f'edit_{i}' for i in FIELDS.keys()])
async def edit(callback_query: types.CallbackQuery) -> None:
    """Функция оработки кнопок выбора поля для редактирования

    Args:
        callback_query (types.CallbackQuery): Объект клика по кнопке
    """
    message = callback_query.message
    user_id = callback_query.from_user.id
    mention = callback_query.from_user.mention
    user = await check_user(message, user_id, mention)

    if not user:
        return
    if None in [user.FIO, user.branch, user.post, user.name_offer, user.offer]:
        UserOffer.delete_by_id(user.user_id)
        await callback_query.message.answer(
            "Какие-то из полей не заполнены!\n\n" +
            "Попробуйте заполнить предложение снова.",
            reply_markup=KEYBOARDS["create_offer"]
        )
        return

    user.return_to_send = True
    user.step = int(callback_query.data.split('_')[1])
    session.commit()

    await message.answer(
        req_info[f"edit_offer_{user.step}"],
        reply_markup=KEYBOARDS["cancel_edit_and_stop"]
    )


@dp.message_handler(commands="help")
async def help(message: types.Message) -> None:
    """Функция обработки команды /help

    Args:
        message (types.Message): Объект сообщения
    """
    await message.answer(req_info["help"])


@dp.message_handler()
async def all_handler(message: types.Message) -> None:
    """Функция обработки всех сообщений, что не подошли под команды выше

    Args:
        message (types.Message): Объект сообщения
    """
    user_id = message.from_user.id
    user = UserOffer.get_by_id(user_id)

    if user is None or user.completion is False:
        await message.answer(
            "Неизвестная команда\n\n " +
            "Проверьте правильность её написания и попробуйте снова!"
        )
        return

    try:
        await write_data_user(user, message.text)
    except ValueError as error:
        await message.answer(str(error))

    if user.return_to_send or user.step >= 4:
        user.step = 5
        user.return_to_send = False
        session.commit()

        await message.answer(
            req_template["offer"].format(
                FIO=user.FIO, branch=user.branch, post=user.post,
                name_offer=user.name_offer, offer=user.offer
            ), reply_markup=KEYBOARDS["confirm_offer"]
        )
        return

    user.step += 1
    session.commit()
    await create_edit_offer(message, user_id)


if __name__ == "__main__":
    try:
        executor.start_polling(dp, skip_updates=True)
    except NetworkError as error:
        print(f"Произошла ошибка соединения: {error}")
        sleep(5000)
        executor.start_polling(dp, skip_updates=True)

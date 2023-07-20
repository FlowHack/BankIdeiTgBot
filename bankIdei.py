from aiogram import Bot, Dispatcher, executor, types
from settings import TOKEN, KEYBOARDS, REQUESTS
from func_bot import get_offer, send_offer
from data_base import session, UserOffer
from aiogram.utils.exceptions import NetworkError
from time import sleep

bot_api = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot_api)

req_info = REQUESTS["info"]
req_template = REQUESTS["template"]


async def start(message: types.Message):
    await message.answer(
        req_info["start"],
        reply_markup=KEYBOARDS["create_offer"]
    )


@dp.message_handler(content_types=[types.ContentType.NEW_CHAT_MEMBERS])
async def new_members_handler(message: types.Message):
    await start(message)


@dp.message_handler(commands="start")
async def start_command(message: types.Message):
    await start(message)


@dp.callback_query_handler(text="create_offer")
async def create_offer_btn(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        req_info["create_offer"],
        reply_markup=KEYBOARDS["example_offer"]
    )


@dp.message_handler(commands="create_offer")
async def create_offer(message: types.Message):
    await message.answer(
        req_info["create_offer"],
        reply_markup=KEYBOARDS["example_offer"]
    )


@dp.message_handler(commands="offer")
async def offer(message: types.Message):
    try:
        offer = get_offer(
            message.text, message.from_user.id,
            message.from_user.mention
        )
    except ValueError as error:
        await message.answer(str(error))
        return

    text = req_template["offer"]
    text = text.format(
        FIO=offer.FIO, branch=offer.branch,
        post=offer.post, name_offer=offer.name_offer, offer=offer.offer
    )
    await message.answer(
        text, reply_markup=KEYBOARDS["confirm_offer"]
    )


async def confirm_offer_yes(message: types.Message, user_id: int):
    try:
        await send_offer(user_id)
        await message.answer(req_info["confirm_offer_yes"])
    except Exception as error:
        await message.answer(
            "Произошла непредвиденная ошибка. Попробуйте позже."
        )
        print(str(error))


@dp.callback_query_handler(text="confirm_next")
async def confirm_offer_yes_btn(callback_query: types.CallbackQuery):
    await confirm_offer_yes(
        callback_query.message, callback_query.from_user.id
    )


@dp.message_handler(commands="confirm_next")
async def confirm_offer_yes_command(message: types.Message):
    await confirm_offer_yes(message, message.from_user.id)


async def confirm_offer_no(message: types.Message, user_id: int):
    user: UserOffer = session.query(UserOffer).filter(
        UserOffer.user_id == user_id
    ).first()

    if user is None:
        await message.answer(
            "Произошла ошибка, видимо вашего предложения нет!",
            reply_markup=KEYBOARDS['example_offer_and_create']
        )
        return

    await message.answer(req_info["confirm_offer_no"])
    await message.answer(
        req_info["confirm_offer_no_offer"].format(
            FIO=user.FIO, branch=user.branch,
            post=user.post, name_offer=user.name_offer,
            offer=user.offer
        ), reply_markup=KEYBOARDS["example_offer_and_create"]
    )


@dp.callback_query_handler(text="offer_cancel")
async def confirm_offer_no_btn(callback_query: types.CallbackQuery):
    await confirm_offer_no(callback_query.message, callback_query.from_user.id)


@dp.message_handler(commands="offer_cancel")
async def confirm_offer_no_command(message: types.Message):
    await confirm_offer_no(message, message.from_user.id)


@dp.message_handler(commands="example_offer")
async def example_offer(message: types.Message):
    await message.answer(
        req_info["example_offer"],
        reply_markup=KEYBOARDS["create_offer"]
    )


@dp.callback_query_handler(text="example_offer")
async def example_offer_btn(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        req_info["example_offer"],
        reply_markup=KEYBOARDS["create_offer"]
    )


if __name__ == "__main__":
    try:
        executor.start_polling(dp, skip_updates=True)
    except NetworkError as error:
        print(f"Произошла ошибка соединения: {error}")
        sleep(5000)
        executor.start_polling(dp, skip_updates=True)

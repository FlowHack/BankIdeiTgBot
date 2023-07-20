from data_base import session, UserOffer
from settings import send_email


def get_offer(message, user_id, mention):
    if "Предложение::" not in message:
        raise ValueError(
            "Не указано предложение, либо указано неверно!" +
            "\n\nПовторите попытку, исправив ошибку."
        )
    text = message.split("/offer")[1].strip().split("Предложение::")
    befor_offer = text[0].strip().split("\n")

    if len(befor_offer) < 4:
        raise ValueError(
            "Указано меньше полей, чем ожидалось.\nОжидалось 4 поля " +
            f"до \"Предложение::\", а пришло {len(befor_offer)}." +
            "\n\nПовторите попытку, исправив ошибку."
        )
    if len(befor_offer) > 4:
        raise ValueError(
            "Указано больше полей, чем ожидалось.\nОжидалось 4 поля " +
            f"до \"Предложение\", а пришло {len(befor_offer)}." +
            "\n\nПовторите попытку, исправив ошибку."
        )
    if text[1].strip() == "":
        raise ValueError(
            "Поле \"Предложение\" пустое.\n\nПовторите попытку," +
            "исправив ошибку."
        )
    text = befor_offer + [text[1].strip()]

    user: UserOffer = session.query(UserOffer).filter(
        UserOffer.user_id == user_id
    ).delete()

    user = UserOffer(
        user_id=user_id,
        FIO=text[0],
        branch=text[1],
        post=text[2],
        name_offer=text[3],
        offer=text[4],
        mention=mention[1:],
    )
    session.add(user)
    session.commit()

    user = session.query(UserOffer).filter(
        UserOffer.user_id == user_id
    ).first()

    return user


async def send_offer(user_id: int) -> bool:
    user: UserOffer = session.query(UserOffer).filter(
        UserOffer.user_id == user_id
    ).first()

    subject = "Банк Идей: " + user.name_offer
    text_email = f"""Предложение в Банк идей

ФИО: {user.FIO}
Филиал: {user.branch}
Должность: {user.post}
Предложение: {user.offer}

Telegram сотрудника
"""
    html_email = f"""
<html>
  <head></head>
  <body>
    <h3 align="center">Предложение в Банк идей</h3><br>
    <p>
      <b><i>ФИО:</i></b><br>
      &nbsp;&nbsp;{user.FIO}
    </p>
    <p><b><i>Филиал:</i></b><br>&nbsp;&nbsp;{user.branch}</p>
    <p><b><i>Должность:</i></b><br>&nbsp;&nbsp;{user.post}</p>
    <p><b><i>Предложение:</i></b><br>&nbsp;&nbsp;{user.offer}</p><br><br>
    <p align="center">
      <a href="https://t.me/{user.mention}">
        <b><i>Telegram сотрудника</i></b>
      </a>
    </p>
  </body>
</html>
"""

    await send_email(subject, text_email, html_email)

    user: UserOffer = session.query(UserOffer).filter(
        UserOffer.user_id == user_id
    ).delete()

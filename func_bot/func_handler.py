from data_base import session, UserOffer
from settings import send_email
from datetime import datetime
from pytz import timezone


async def write_data_user(user: UserOffer, data: str) -> None:
    """Функция записывает значение data в поле пользователя,
    которое определяется по шагу заполнения анкеты

    Args:
        user (UserOffer): Объект модели БД пользователя
        data (str): Строковое значение поля БД пользователя

    Raises:
        ValueError: Ошибка, означающее сбой в заполнении значений полей
    """
    step = user.step
    data = data.strip()

    if data == "":
        raise ValueError(
            "Заполняемое поле не может быть пустым!" +
            "\n\nПовторите попытку"
        )

    if step == 0:
        user.FIO = data
    if step == 1:
        user.branch = data
    if step == 2:
        user.post = data
    if step == 3:
        user.name_offer = data
    if step == 4:
        user.offer = data
    session.commit()


async def check_field(user: UserOffer) -> bool:
    """Функция проверяет на пустоту поле шага анкеты

    Args:
        user (UserOffer): Объект модели БД пользователя

    Returns:
        bool: Поле заполнено - True, False - пустое
    """
    step = user.step

    if step == 0 and user.FIO is None:
        return False
    if step == 1 and user.branch is None:
        return False
    if step == 2 and user.post is None:
        return False
    if step == 3 and user.name_offer is None:
        return False
    if step == 4 and user.offer is None:
        return False

    return True


async def send_offer(user_id: int) -> None:
    """Функция отправки предложения на почту

    Args:
        user_id (int): Числовое значение ID пользователя

    Raises:
        ValueError: Ошибки, связанные с ошибками значений полей анкеты
    """
    user: UserOffer = session.query(UserOffer).filter(
        UserOffer.user_id == user_id
    ).first()
    if user is None:
        raise ValueError(
            """Вы ещё не создали предложение!

Создайте сначала предложение.
"""
        )
    if None in [user.FIO, user.branch, user.post, user.name_offer, user.offer]:
        UserOffer.delete_by_id(user_id)
        raise ValueError(
            """Какие-то из полей не заполнены!

Попробуйте заполнить предложение снова.
"""
        )

    date = datetime.now(timezone("Etc/GMT+4")).strftime("%d/%m/%Y %H:%M:%S")
    subject = "Банк Идей: Предложение"
    mention = user.mention[1:] if user.mention[0] == "@" else user.mention
    text_email = f"""{user.name_offer}

ФИО: {user.FIO}
Филиал: {user.branch}
Должность: {user.post}
Предложение: {user.offer}

{date}
Telegram сотрудника: https://t.me/{mention}
"""
    html_email = f"""
<html>
  <head></head>
  <body>
    <h3 align="center">{user.name_offer}</h3><br>
    <p>
      <b><i>ФИО:</i></b><br>
      &nbsp;&nbsp;{user.FIO}
    </p>
    <p><b><i>Филиал:</i></b><br>&nbsp;&nbsp;{user.branch}</p>
    <p><b><i>Должность:</i></b><br>&nbsp;&nbsp;{user.post}</p>
    <p><b><i>Предложение:</i></b><br>&nbsp;&nbsp;{user.offer}</p><br><br>
    <p align="center">
      {date}
    </p>
    <p align="center">
      <a href="https://t.me/{mention}">
        <b><i>Telegram сотрудника</i></b>
      </a>
    </p>
  </body>
</html>
"""

    await send_email(subject, text_email, html_email)

    UserOffer.delete_by_id(user_id)

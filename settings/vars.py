from os import getenv


DEBUG = False

TOKEN = getenv("API_TOKEN")

EMAIL_LOGIN = getenv("EMAIL_LOGIN")
EMAIL_PASSWORD = getenv("EMAIL_PASSWORD")
EMAIL_HOST = getenv("EMAIL_HOST")
EMAIL_PORT = getenv("EMAIL_PORT")
EMAIL_TO = getenv("EMAIL_TO")

DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")
DB_NAME = getenv("DB_NAME")
DB_USER = getenv("POSTGRES_USER")
DB_PASSWORD = getenv("POSTGRES_PASSWORD")

REQUESTS = {
    "info": {
        "start": """<b><i>Здравствуйте!</i></b>

Я - бот, который поможет вам внести своё предложение в "Банк идей" по улучшению работы.

Чтобы создать своё предложение, нажмите на кнопку ниже, либо отправьте мне команду /create_offer.

Если Вам нужна помощь по командам, введите команду /help
""",
        "create_offer": """Я проведу вас пошагово для заполнения Вашего предложения.

Для начала, напишите мне Ваше ФИО
""",
        "create_offer_1": "Напишите мне название своего филиала",
        "create_offer_2": "Напишите мне название своей должности",
        "create_offer_3": "Напишите мне краткое название Вашего предложения",
        "create_offer_4": "Напишите мне Ваше предложение",
        "edit_offer_0": "Для исправления, напишите мне Ваше ФИО",
        "edit_offer_1": "Для исправления, напишите мне название своего филиала",
        "edit_offer_2": "Для исправления, напишите мне название своей должности",
        "edit_offer_3": "Для исправления, напишите мне краткое название Вашего предложения",
        "edit_offer_4": "Для исправления, напишите мне Ваше предложение",
        "confirm_offer_yes": """Спасибо за внесённый вклад в развитие проекта!

Если захотите написать ещё предложение, отправьте команду /create_offer, или нажмите на кнопку ниже!

<i>Хорошего Вам дня!</i>
""",
        "confirm_offer_no": """Что вы хотите исправить в вашем предложении?

Выберите один из вариантов
""",
        "stop": "Приостанавливаю заполнение предложения.\n\nКак захотите продолжить, отправьте мне команду /create_offer",
        "help": """<b>Список возможных команд и их описание:</b>
<b><i>/start</i></b> - Команда для начала общения со мной, нужна только при первом запуске
<b><i>/create_offer</i></b> - Команда, которая поможет вам создать ваше предложение

<b>Как заполнять поля:</b>
- Все поля, кроме поля "Предложение" необходим заполнять без переноса строки, а в поле "Предложение", соответственно, перенос строки допускается.
- <b><i>Поле ФИО</i></b> - Напишите свои фамилию, имя и отчество.
- <b><i>Поле Филиал</i></b> - Напишите ваш филиал, в котором вы работаете в компании.
- <b><i>Поле Должность</i></b> - Напишите должность, на которой вы работаете в компании.
- <b><i>Поле Название предложения</i></b> - Напишите краткое и лаконичное название вашего предложения.
- <b><i>Поле Предложение</i></b> - Здесь напишите само ваше предложение, можно использовать перенос строки. Пишите развёрнуто, но лаконично!
""",
        "null_data_offer": """Похоже, что некоторые поля не заполнены!

Попробуйте заполнить предложение заново!
""",
    },
    "template": {
        "offer": """Вот что получилось:

<b><i>ФИО:</i></b>
  {FIO}
<b><i>Филиал:</i></b>
  {branch}
<b><i>Должность:</i></b>
  {post}
<b><i>Название предложения:</i></b>
  {name_offer}
<b><i>Предложение:</i></b>
  {offer}

Проверьте своё предложение на ошибки и выберите один из вариантов:
- Да - Отправить Ваше предложение
- Нет - Исправить Ваше предложение
""",
    },
}

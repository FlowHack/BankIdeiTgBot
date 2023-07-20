from .keyboards import kb_create_offer, kb_confirm_offer, kb_example_offer, kb_example_offer_and_create
from os import getenv


DEBUG = True

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

KEYBOARDS = {
    "create_offer": kb_create_offer(),
    "confirm_offer": kb_confirm_offer(),
    "example_offer": kb_example_offer(),
    "example_offer_and_create": kb_example_offer_and_create(),
}

REQUESTS = {
    "info": {
        "start": """<b><i>Здравствуйте!</i></b>

Я - бот, который поможет вам внести своё предложение в "Банк идей" по улучшению работы.

Чтобы отправить своё предложение, нажмите на кнопку ниже, либо отправьте мне команду /create_offer.

Если Вам нужна помощь по командам, введите команду /help
""",
        "create_offer": """Чтобы отправить своё предложение, необходимо отправить мне его по шаблону ниже.

/offer

<b><i>[ФИО]</i></b> Дмитриев Дмитрий Дмитриевич [если нет отчества, просто не пишите его]
<b><i>[Филиал]</i></b> Ваш филиал
<b><i>[Должность]</i></b> Ваша должность
<b><i>Предложение::</i></b> Название вашего предложения
Описание предложения: Ваше предложение (конструктивный и лаконичный текст)

<b><i>ВАЖНО</i></b>
- Наименование поля "Предложение::" обязательно!
- В поле "Предложение" можно делать перенос строки
- Порядок строк нарушать нельзя
- Указанное в "[]" писать не надо
- Содержимое строк, кроме "Предложение" пишутся без переноса строки
- Между каждой строкой обязателен перенос строки
""",
        "confirm_offer_yes": """Спасибо за внесённый вклад в развитие проекта!

<i>Хорошего Вам дня!</i>
""",
        "confirm_offer_no": """Исправьте ошибки в своём предложении и отправьте его повторно, использовав вышеупомянутый шаблон.

Для удобства исправления, вот ваше предложение:
""",
        "confirm_offer_no_offer": """
{FIO}
{branch}
{post}
{name_offer}
Предложение:: {offer}
""",
        "example_offer": """/offer

Дмитриев Дмитрий Дмитриевич
Механики, робототехники, инженерии транспортных и технических систем
Техник
Банк Идей
Предложение:: Проект по сбору предложений от сотрудников.
Целью данного проекта будет являться улучшение качества и эффективности работы сотрудников компании.
""",
        "help": """Список возможных команд и их описание:
/start - Команда для начала общения со мной, нужна только при первом запуске
/
""",
    },
    "template": {
        "offer": """Вот что получилось:

<b><i>ФИО:</i></b> {FIO}
<b><i>Филиал:</i></b> {branch}
<b><i>Должность:</i></b> {post}
<b><i>Название предложения:</i></b> {name_offer}
<b><i>Предложение:</i></b> {offer}

Проверьте своё предложение на ошибки и выберите один из вариантов:
- Да (/confirm_next) - Отправить Ваше предложение
- Нет (/offer_cancel) - Исправить Ваше предложение
""",
    },
}
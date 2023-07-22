# BankIdeiTgBot v2.0

[Бот для теста](https://t.me/flowhack_bot) (_Не работает на данный момент_)

## Описание
_Благодаря этому боту, можно эффективно собирать предложения своих сотрудников по улучшению рабочего места_

## Технологии
- Python 3.9
- Aiogram 2.25.1
- AioSMTPlib 2.0.2
- SQLAlchemy 2.0.19

## Запуск проекта
- Установите [Docker](https://docs.docker.com/engine/install/) на свой сервер
- Из репозитория закиньте в одну папку файл docker-compose.yaml и создайте в этой же папке файл .env
- Заполните .env файл данными
```env
API_TOKEN=<Токен доступа к боту в Telegram>
EMAIL_LOGIN=<E-mail отправителя>
EMAIL_PASSWORD=<Пароль от E-mail отправителя>
EMAIL_HOST=<Адрес почтового сервера>
EMAIL_PORT=<Порт почтового сервера>
EMAIL_TO=<E-mail получателя ответов на анкету>
DB_HOST=db
DB_PORT=5432
DB_NAME=<Название таблицы PostgreSQL>
POSTGRES_USER=<Логин пользователя PostgreSQL>
POSTGRES_PASSWORD=<Пароль пользователя PostgreSQL>
```
- Запустите docker из папки
```bash
docker-compose up
```
## _Готово! Теперь бот сможет регистрировать ответы и отправлять их на почту!_
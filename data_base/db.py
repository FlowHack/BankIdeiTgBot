from sqlalchemy import Column, Integer, String, create_engine, Boolean
from sqlalchemy.orm import Session, declarative_base

from settings import (DB_HOST, DB_NAME, DB_PORT, DB_PASSWORD,
                      DB_USER, DEBUG)
from typing import List


if DEBUG:
    engine = create_engine(
        'postgresql+psycopg2://postgres:1234@localhost:5432/postgres'
    )
else:
    engine = create_engine(
        f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@'
        f'{DB_HOST}:{DB_PORT}/{DB_NAME}'
    )
model = declarative_base()
session = Session(bind=engine)


class UserOffer(model):
    __tablename__ = 'user_proposal'

    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), nullable=False)
    mention = Column(String(), nullable=False)
    step = Column(Integer(), nullable=False)
    completion = Column(Boolean(), nullable=False)
    return_to_send = Column(Boolean(), nullable=False)
    FIO = Column(String(), nullable=True)
    branch = Column(String(), nullable=True)
    post = Column(String(), nullable=True)
    name_offer = Column(String(), nullable=True)
    offer = Column(String(), nullable=True)

    def exists(user_id: int) -> bool:
        """Функция проверки наличия записи в БД

        Args:
            user_id (int): Числовое значение ID пользователя

        Returns:
            bool: True - есть запись, False - запись отсутсвует
        """
        exists = session.query(UserOffer).filter(
            UserOffer.user_id == user_id
        ).first()

        return True if exists is not None else False

    def get_by_id(user_id: int):
        """Функция получения записи о пользователе

        Args:
            user_id (int): Числовое значение ID пользователя

        Returns:
            user (UserOffer): Объект пользователя модели БД
        """
        return session.query(UserOffer).filter(
            UserOffer.user_id == user_id
        ).first()

    def delete_by_id(user_id: int) -> None:
        """Функция удаления пользователя

        Args:
            user_id (int): Числовое значение ID пользователя
        """
        session.query(UserOffer).where(UserOffer.user_id == user_id).delete()
        session.commit()

    def get_or_create(user_id: int, mention: str):
        """Функция получения пользователя, либо его создания, если нет
        записи в БД

        Args:
            user_id (int): Числовое значение ID пользователя
            mention (str): Строковое короткое имя пользователя

        Returns:
            List(UserOffer, bool): Возвращает объект пользователя и
            значение True - была создана новая зпись, False - пользователь уже был в БД
        """
        user = UserOffer.get_by_id(user_id)
        new = False

        if user is None:
            new = True
            user = UserOffer(
                user_id=user_id, mention=mention, step=0, completion=True,
                return_to_send=False
            )
            session.add(user)
            session.commit()

        return user, new

    def __repr__(self):
        return f'{self.user_id} Предложение: f{self.name_offer}'


model.metadata.create_all(engine)

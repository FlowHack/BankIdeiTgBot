from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base

from settings import (DB_HOST, DB_NAME, DB_PORT, DB_PASSWORD,
                      DB_USER, DEBUG)


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
    FIO = Column(String(), nullable=False)
    branch = Column(String(), nullable=False)
    post = Column(String(), nullable=False)
    name_offer = Column(String(), nullable=False)
    offer = Column(String(), nullable=False)

    def __repr__(self):
        return f'{self.user_id} Предложение: f{self.name_offer}'


model.metadata.drop_all(engine)
model.metadata.create_all(engine)

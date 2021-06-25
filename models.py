from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from constants import COUNTRY_NAME_API, ID_NAME_API, CUR_NAME_API, AMOUNT_NAME_API, DATE_NAME_API, DB_URL

Base = declarative_base()
session = sessionmaker(bind=create_engine(DB_URL))()


class Limit(Base):
    __tablename__ = 'limits'

    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String)
    cur = Column(String)
    amount = Column(Integer)

    @property
    def to_json(self):
        return {
            ID_NAME_API: self.id,
            COUNTRY_NAME_API: self.country,
            CUR_NAME_API: self.cur,
            AMOUNT_NAME_API: self.amount
        }


class Transfer(Base):
    __tablename__ = 'transfers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime)
    amount = Column(Integer)
    cur = Column(String)
    country = Column(String)

    @property
    def to_json(self):
        return {
            ID_NAME_API: self.id,
            DATE_NAME_API: self.date,
            AMOUNT_NAME_API: self.amount,
            CUR_NAME_API: self.cur,
            COUNTRY_NAME_API: self.country
        }

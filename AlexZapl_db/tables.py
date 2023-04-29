from sqlalchemy import Column, Integer, String, Date, DateTime
from .db import Base


class Users(Base):

    __tablename__ = 'users'

    id = Column(Integer, unique=True, index=True)
    login = Column(String, unique=True, index=True, primary_key=True)
    password = Column(String)
    login_date = Column(Date)
    phone_number = Column(String)
    email = Column(String)
    name = Column(String)
    fname = Column(String)
    cash = Column(Integer)


class History(Base):

    __tablename__ = 'history'

    time = Column(DateTime, index=True)
    userid = Column(Integer, index=True,  nullable=False)
    cash = Column(Integer, primary_key=True)
    why = Column(String)


class Card(Base):

    __tablename__ = 'card'

    userid = Column(Integer, index=True, unique=True)
    cardid = Column(String, primary_key=True, unique=True, index=True)
    enddate = Column(Date)
    cvv = Column(Integer, unique=True)
    cash = Column(Integer)
    currency = Column(String)

class Loans(Base):

    __tablename__ = 'loans'

    userid = Column(Integer, index=True, unique=True)
    dateend = Column(String, primary_key=True)
    loan = Column(Integer)
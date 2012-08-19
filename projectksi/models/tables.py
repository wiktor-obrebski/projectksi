from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy.orm import sessionmaker, scoped_session

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id_user = Column(Integer, primary_key=True)
    email = Column(String(60))
    password = Column(String(60))

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return "<User('%s','%s')>" % (self.email, self.password)
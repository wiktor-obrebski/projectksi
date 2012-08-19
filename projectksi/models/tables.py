from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy.orm import sessionmaker, scoped_session

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id_user = Column(Integer, primary_key=True)
    email = Column(String(60))
    password = Column(String(60))
    characters = relationship("Character", order_by='Character.id_character')

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return "<User('%s','%s')>" % (self.email, self.password)

class Character(Base):
    __tablename__ = 'characters'
    id_character = Column(Integer, primary_key=True)
    name = Column(String(90))
    id_user = Column(Integer, ForeignKey('users.id_user'))

    #I define relation in both classes, to make it clear and better working with IDEs auto-complete feature
    user = relationship("User")

    def __repr__(self):
        return "<Char('%s')>" % (self.name)
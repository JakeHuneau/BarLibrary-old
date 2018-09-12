from sqlalchemy import Column, Integer, Text, Index

from .meta import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

Index('my_index', User.name, unique=True, mysql_length=255)
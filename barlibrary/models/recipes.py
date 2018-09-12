from sqlalchemy import Column, Integer, Text, Index

from .meta import Base

class Recipe(Base):
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True)
    name = Column(Text)

Index('my_index', Recipe.name, unique=True, mysql_length=255)
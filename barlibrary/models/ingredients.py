from sqlalchemy import Column, Integer, Text, Index

from .meta import Base

class Ingredient(Base):
    __tablename__ = 'ingredients'
    id = Column(Integer, primary_key=True)
    name = Column(Text)

Index('my_index', Ingredient.name, unique=True, mysql_length=255)
"""
TODO: This is going to be a table that has 2 columns: specific, generic
where specific is something like "white rum" and generic is "rum". It should
connect to the recipes table so it uses the IDs instead of names. It can be used
for searching for drinks and not needing a specific ingredient but use a generic
instead
"""
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from barlibrary.models.meta import Base

class Subtype(Base):
    __tablename__ = 'subtypes'
    id = Column(Integer, primary_key=True)
    specific = Column(Integer, ForeignKey('ingredients.id'), unique=True)
    generic = Column(Integer, ForeignKey('ingredients.id'))


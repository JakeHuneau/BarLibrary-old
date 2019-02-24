from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship

from barlibrary.models.meta import Base

class Ingredient(Base):
    __tablename__ = 'ingredients'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)

    recipe_ingredient = relationship('RecipeIngredient', back_populates='ingredient')

    def __repr__(self):
        return self.name
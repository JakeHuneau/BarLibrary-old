from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship

from barlibrary.models.meta import Base

class Recipe(Base):
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    directions = Column(Text)

    recipe_ingredient = relationship('RecipeIngredient', back_populates='recipe')
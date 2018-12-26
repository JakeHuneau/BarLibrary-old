from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship

from barlibrary.models.meta import Base

class Recipe(Base):
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    directions = Column(Text)

    recipe_ingredient = relationship('RecipeIngredient', back_populates='recipe')

    def __repr__(self):
        return_str = f'---{self.name}---\n\n-Ingredients-\n'
        for ingredient in self.recipe_ingredient:
            return_str += f'{ingredient}\n'
        return_str += '\n-Directions-\n'
        return_str += self.directions

        return return_str
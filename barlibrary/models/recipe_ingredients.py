from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from barlibrary.models.meta import Base

class RecipeIngredient(Base):
    """
    1 to many with Recipe -> self, Ingredients -> self
    """
    __tablename__ = 'recipe_ingredients'
    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'))
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'))
    quantity = Column(Integer)
    unit = Column(Text)
    importance = Column(Integer)

    recipe = relationship('Recipe', back_populates='recipe_ingredient')
    ingredient = relationship('Ingredient', back_populates='recipe_ingredient')

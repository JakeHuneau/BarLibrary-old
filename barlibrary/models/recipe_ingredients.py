from sqlalchemy import Column, Integer, Text, ForeignKey, Float, Boolean
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
    quantity = Column(Float)
    unit = Column(Text)
    required = Column(Boolean)  # 0 means optional, 1 is required

    recipe = relationship('Recipe', back_populates='recipe_ingredient')
    ingredient = relationship('Ingredient', back_populates='recipe_ingredient')

    def __repr__(self):
        return_str = f'recipe_id[{self.recipe_id}] ingredient_id[{self.ingredient_id}] quantity[{self.quantity} {self.unit}]'
        if self.required == 0:
            return_str += ' - optional'

        return return_str
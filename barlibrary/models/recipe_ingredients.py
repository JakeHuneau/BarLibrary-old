from sqlalchemy import Column, Integer, Text, Index

from .meta import Base

class RecipeIngredients(Base):
    __tablename__ = 'recipe_ingredients'
    recipe_id = Column(Integer)
    ingredient_id = Column(Integer)
    quantity = Column(Integer)
    unit = Column(Text)
    directions= Column(Text)


Index('my_index', RecipeIngredients.name, unique=True, mysql_length=255)
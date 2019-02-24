from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from barlibrary.models.meta import Base

class Kitchen(Base):
    """
    What ingredients a user has
    """
    __tablename__ = 'kitchen'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'))

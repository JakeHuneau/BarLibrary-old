import transaction
from sqlalchemy import and_

from ..models import Ingredient, Kitchen, User


def get_all_ingredients(db, user):
    """
    Gets all the ingredients and which ones the user has.

    Args:
        db: (sqlalchemy session) Session with db
        user: (str) user name to get kitchen for

    Returns:
        (dict) {ingredient_name: True/False}. Each ingredient and if the user has it or not
    """
    all_ingredients = db.query(Ingredient).all()
    user_id = db.query(User).filter(User.name==user).first().id
    user_ingredients = {k.ingredient_id for k in db.query(Kitchen).filter(Kitchen.user_id==user_id).all()}
    return {i.name: True if i.id in user_ingredients else False for i in all_ingredients}


def update_kitchen(db, user, ingredients):
    """
    Updates the kitchen for that user by updating the db.

    Args:
        db: (sqlalchemy session) Session with db
        user: (str) user name to get kitchen for
        ingredients: (set) ingredients the user has
    """
    user_id = db.query(User).filter(User.name == user).first().id
    user_ingredients = {k.ingredient_id for k in db.query(Kitchen).filter(Kitchen.user_id == user_id).all()}
    ingredient_ids = {k.id for k in db.query(Ingredient).filter(Ingredient.name.in_(ingredients)).all()}
    to_add = ingredient_ids - user_ingredients
    to_remove = user_ingredients - ingredient_ids
    with transaction.manager:
        for add_id in to_add:
            db.add(Kitchen(user_id=user_id, ingredient_id=add_id))
        for delete_id in to_remove:
            to_remove = db.query(Kitchen).filter(and_(Kitchen.user_id==user_id, Kitchen.ingredient_id==delete_id)).first()
            db.delete(to_remove)
    return True

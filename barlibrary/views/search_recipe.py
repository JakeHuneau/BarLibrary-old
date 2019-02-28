from ..models import Recipe, RecipeIngredient, Ingredient
from .find import pretty_directions


def search(db, recipe_name):
    recipe = db.query(Recipe).filter(Recipe.name == recipe_name.lower()).first()
    if not recipe:
        return

    return_str = f'<br>---{recipe.name}---<br>'
    return_str += '<br>-Ingredients-<br>'

    ingredients = db.query(RecipeIngredient).filter(RecipeIngredient.recipe_id == recipe.id).all()
    for ingredient in ingredients:
        ingredient_name = db.query(Ingredient).filter(Ingredient.id == ingredient.ingredient_id).first().name
        return_str += f'{ingredient_name}: {ingredient.quantity} {ingredient.unit}<br>'
    return_str += f'<br>-Directions-<br>{pretty_directions(recipe.directions)}'
    return return_str

from collections import defaultdict

from ..models import Recipe, RecipeIngredient, Ingredient


def find_recipes(db, ingredients_str):
    """
    Finds all the recipes that can be made with the given ingredients

    Args:
        db: database session
        ingredients: (List[str]) ingredients

    Returns:
        (List[Recipe])
    """
    ingredients = set()
    for ingredient_str in ingredients_str:
        ingredient = db.query(Ingredient).filter_by(name=ingredient_str).first()
        if ingredient:
            ingredients.add(ingredient)
    ingredient_pieces = defaultdict(set)
    for ingredient in ingredients:
        recipe_pieces = db.query(RecipeIngredient).filter_by(ingredient_id=ingredient.id).all()
        for recipe_piece in recipe_pieces:
            if recipe_piece.required == 1:  # Only want to consider required ingredients
                ingredient_pieces[recipe_piece.recipe_id].add(recipe_piece)

    found_recipes = set()
    for possible_recipe_id, recipe_pieces in ingredient_pieces.items():
        full_recipe = set(db.query(RecipeIngredient).filter_by(recipe_id=possible_recipe_id,
                                                               required=1).all())
        if full_recipe == recipe_pieces:
            found_recipes.add(possible_recipe_id)

    return [format_recipe(db, found_recipe) for found_recipe in found_recipes]


def format_recipe(db, found_recipe):
    """
    Formats a found recipe to print onto the page

    Args:
        db: database session
        found_recipe: (int) id of recipe

    Returns:
        (str) Pretty format of recipe
    """
    recipe = db.query(Recipe).filter_by(id=found_recipe).first()
    return_str = f'<br>---{recipe.name}---<br>'
    return_str += '<br>-Ingredients-<br>'
    for ingredient in recipe.recipe_ingredient:
        ingredient_name = db.query(Ingredient.name).filter_by(id=ingredient.ingredient_id).first()[0]
        return_str += f'{ingredient_name}: {ingredient.quantity} {ingredient.unit}<br>'
    return_str += f'<br>-Directions-<br>{recipe.directions}'
    return return_str


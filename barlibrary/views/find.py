from collections import defaultdict

from ..models import Recipe, RecipeIngredient, Ingredient, Kitchen, User, Subtype


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
    for ingredient_str in set(ingredients_str):
        ingredient = db.query(Ingredient).filter_by(name=ingredient_str).first()
        if ingredient:
            ingredients.add(ingredient.id)

    # Add subtypes of every ingredient
    ingredients = ingredients.union(get_subtypes(db, ingredients))

    ingredient_pieces = defaultdict(set)
    for ingredient in ingredients:
        recipe_pieces = db.query(RecipeIngredient).filter_by(ingredient_id=ingredient).all()
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


def find_all_recipes(db, ingredients_str):
    ingredients = set()
    for ingredient_str in set(ingredients_str):
        ingredient = db.query(Ingredient).filter(Ingredient.name==ingredient_str).first()
        if ingredient:
            ingredients.add(ingredient.id)

    ingredients = ingredients.union(get_subtypes(db, ingredients))

    recipes = set()
    for ingredient in ingredients:
        for found_recipe in db.query(RecipeIngredient).filter(RecipeIngredient.ingredient_id==ingredient).all():
            if found_recipe:
                recipes.add(found_recipe.recipe_id)
    return [format_recipe(db, recipe) for recipe in recipes]


def format_recipe(db, found_recipe):
    """
    Formats a found recipe to print onto the page

    Args:
        db: database session
        found_recipe: (int) id of recipe

    Returns:
        (str) Pretty format of recipe
    """
    recipe = db.query(Recipe).filter(Recipe.id==found_recipe).first()
    if not recipe:
        return ''
    return_str = f'<br>---{recipe.name}---<br>'
    return_str += '<br>-Ingredients-<br>'
    for ingredient in recipe.recipe_ingredient:
        ingredient_name = db.query(Ingredient.name).filter(Ingredient.id==ingredient.ingredient_id).first()[0]
        return_str += f'{ingredient_name}: {ingredient.quantity} {ingredient.unit}<br>'
    return_str += f'<br>-Directions-<br>{pretty_directions(recipe.directions)}'
    return return_str


def pretty_directions(directions_str):
    """
    Puts a newline before each number in directions.

    Args:
        directions_str: (str) Looks like "1. something. 2. Something else"

    Returns:
        (str) pretty directions that look like:
            1. something
            2. something else
    """
    step = 2
    while True:
        old_str = directions_str
        directions_str = directions_str.replace(f'{step}. ', f'<br>{step}. ')
        if old_str == directions_str:
            break
        step += 1
    return directions_str

def get_initial_list(db, user):
    user_id = db.query(User).filter(User.name == user).first().id
    ingredient_ids = {k.ingredient_id for k in db.query(Kitchen).filter(Kitchen.user_id == user_id).all()}
    ingredient_names = [k.name for k in db.query(Ingredient).filter(Ingredient.id.in_(ingredient_ids)).all()]
    return ingredient_names


def get_subtypes(db, ingredients):
    """
    Finds all the subtypes of an ingredient

    Returns:
        (set[int]) a set of all id's for specific ingredients
    """
    new_ingredients = set()
    for ingredient in ingredients:
        subtypes = db.query(Subtype).filter(Subtype.generic==ingredient).all()
        for subtype in subtypes:
            new_ingredients.add(subtype.specific)
    return new_ingredients


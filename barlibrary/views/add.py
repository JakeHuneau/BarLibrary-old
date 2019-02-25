import re

from ..exceptions import BadIngredientInput, RecipeAlreadyExists
from ..models import Recipe, RecipeIngredient, Ingredient


def add_to_db(db, params):
    """
    Adds the recipe from the params to the db.

    Args:
        db: database session
        params: (dict) must contain keys 'recipe_name', 'ingredients', and 'directions'
    """
    recipe_name = params.get('recipe_name').strip().lower()
    ingredients = params.get('ingredients').lower()
    directions = params.get('directions').lower()

    if not (recipe_name and ingredients and directions):
        raise BadIngredientInput()

    recipe = db.query(Recipe).filter_by(name=recipe_name).first()
    if recipe:  # Don't want to add something with the same name
        raise RecipeAlreadyExists()

    # break apart the directions and add a number in front of each direction.
    numbered_directions = ''.join(f'{i+1}. {d.strip()}. ' for i, d in enumerate(directions.split(';'))).strip()
    recipe = Recipe(name=recipe_name, directions=numbered_directions)

    for ingredient_str in ingredients.split(','):
        ingredient_name, quantity, unit, required = parse_ingredient(ingredient_str)
        ingredient = db.query(Ingredient).filter_by(name=ingredient_name).first()
        if not ingredient:
            ingredient = Ingredient(name=ingredient_name)
            db.add(ingredient)
            db.flush()

        link = RecipeIngredient(recipe_id=recipe.id,
                                ingredient_id=ingredient.id,
                                quantity=quantity,
                                unit=unit,
                                required=required)
        db.add(recipe)
        db.add(link)
    db.flush()
    return recipe


def parse_ingredient(ingredient_str):
    """
    Parses the ingredient string that will look something like:

    'whiskey [1.0 oz]' or
    'cherry [1] x'

    where the x means it is not required.

    Returns:
        ingredient_name: (str) name of the ingredient
        quantity: (float) quantity needed
        unit: (str) unit of quantity
        required: (int) 1 if required, 0 if not
    """
    pattern = r'^\s*(?P<name>.+)\s+\[(?P<quantity>(\d *\.)?\d+)\s*(?P<unit>.+)?\]\s*(?P<required>x)?$'
    p = re.compile(pattern)
    res = p.match(ingredient_str)
    if not res:
        raise BadIngredientInput
    groups = res.groupdict()
    ingredient_name = groups.get('name')
    quantity = float(groups.get('quantity'))
    unit = groups.get('unit', '')
    if not unit:
        unit = ''
    required = 0 if groups.get('required') else 1
    return ingredient_name.lower(), quantity, unit, required

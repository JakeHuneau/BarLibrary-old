from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .add import add_to_db
from .find import find_recipes, find_all_recipes
from ..exceptions import BadIngredientInput, RecipeAlreadyExists


@view_config(route_name='home', renderer='../templates/home.jinja2')
def home_view(request):
    return {}

@view_config(route_name='add_recipe', renderer='../templates/add_recipe.jinja2')
def add_recipe_view(request):
    print('okay')
    if request.method == 'POST':
        print('no')
        return_template = {'recipe_name': request.params.get('recipe_name'),
                           'ingredients': request.params.get('ingredients'),
                           'directions': request.params.get('directions')}
        try:
            recipe = add_to_db(request.dbsession, request.params)
            return_template['recipe'] = str(recipe).replace('\n', '<br>')
        except BadIngredientInput:
            return_template['bad_ingredient_input'] = True
        except RecipeAlreadyExists:
            return_template['recipe_exists'] = True
        return return_template
    print('okay2')
    return {}

@view_config(route_name='edit_recipe', renderer='../templates/edit_recipe.jinja2')
def edit_recipe_view(request):
    return {}

@view_config(route_name='remove_recipe', renderer='../templates/remove_recipe.jinja2')
def remove_recipe_view(request):
    return {}

@view_config(route_name='find_recipes', renderer='../templates/find_recipes.jinja2')
def find_recipes_view(request):
    if request.method == 'GET':
        ingredients = request.params.get('ingredients')
        return_template = {'ingredients': ingredients}
        if ingredients:  # Make sure not none
            ingredients = [i.lower().strip() for i in ingredients.split(',')]
            recipes = find_recipes(request.dbsession, ingredients)
            return_template['recipes_found'] = recipes
        return return_template
    return {}

@view_config(route_name='find_all', renderer='../templates/find_all.jinja2')
def find_all_with_ingredients(request):
    if request.method == 'GET':
        ingredients = request.params.get('ingredients')
        return_template = {'ingredients': ingredients}
        if ingredients:  # Make sure not none
            ingredients = [i.lower().strip() for i in ingredients.split(',')]
            recipes = find_all_recipes(request.dbsession, ingredients)
            return_template['recipes_found'] = recipes
        return return_template
    return {}
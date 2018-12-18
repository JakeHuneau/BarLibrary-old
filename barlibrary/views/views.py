from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from barlibrary.models import Recipe
from barlibrary.forms import NewRecipeForm


@view_config(route_name='home', renderer='../templates/home.jinja2')
def home_view(request):
    return {}

@view_config(route_name='add_recipe', renderer='../templates/add_recipe.jinja2')
def add_recipe_view(request):
    if request.method == 'POST':

        print(request.params)
    return {}
    # form = NewRecipeForm(request.POST)
    # if request.method == 'POST' and form.validate():
    #     print('good')
    # return {}

@view_config(route_name='edit_recipe', renderer='../templates/edit_recipe.jinja2')
def edit_recipe_view(request):
    return {}

@view_config(route_name='remove_recipe', renderer='../templates/remove_recipe.jinja2')
def remove_recipe_view(request):
    return {}

@view_config(route_name='find_recipes', renderer='../templates/find_recipes.jinja2')
def find_recipes_view(request):
    return {}
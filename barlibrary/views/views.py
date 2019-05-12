from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

import requests

from .add import add_to_db
from .change_permission import change_user_permission
from .delete import delete_recipe
from .find import find_recipes, find_all_recipes, get_initial_list
from .kitchen import get_all_ingredients, update_kitchen
from .search_recipe import search
from ..models import Ingredient, Subtype
from ..security import validate_user, add_user, get_secret
from ..exceptions import BadIngredientInput, RecipeAlreadyExists, RecipeDoesntExist


@view_config(route_name='bar_library_home', renderer='../templates/bar_library_home.jinja2')
def bar_library_home_view(request):
    return_dict = {}
    if request.session.get('permission', 0) & 1:
        return_dict['can_write'] = True
    if request.session.get('permission', 0) & 2:
        return_dict['can_delete'] = True
    if request.session.get('permission', 0) & 4:
        return_dict['can_change_permissions'] = True
    return return_dict

@view_config(route_name='add_recipe', renderer='../templates/add_recipe.jinja2')
def add_recipe_view(request):
    if not request.session.get('permission', 0) & 1:  # Can add
        return {'get_out': 'YOU SHOULD NOT BE HERE.'}
    if 'add.submitted' in request.params:
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
    return {}

@view_config(route_name='remove_recipe', renderer='../templates/remove_recipe.jinja2')
def remove_recipe_view(request):
    if not request.session.get('permission', 0) & 2:  # Can delete
        return {'get_out': 'YOU SHOULD NOT BE HERE.'}
    if 'remove.submitted' in request.params:
        return_template = {}

        try:
            result = delete_recipe(request.dbsession, request.params)
            return_template['success'] = result
        except BadIngredientInput:
            return_template['bad_ingredient_input'] = True
        except RecipeDoesntExist:
            return_template['recipe_doesnt_exist'] = True
        return return_template

    return {}

@view_config(route_name='find_recipes', renderer='../templates/find_recipes.jinja2')
def find_recipes_view(request):
    if 'find.submitted' in request.params:
        ingredients = request.params.get('ingredients')
        return_template = {'ingredients': ingredients}
        if ingredients:  # Make sure not none
            ingredients = [i.lower().strip() for i in ingredients.split(',')]
            recipes = find_recipes(request.dbsession, ingredients)
            return_template['recipes_found'] = recipes
        return return_template
    user = request.session.get('user')
    if user:
        ingredients = ', '.join(get_initial_list(request.dbsession, user))
        return {'ingredients': ingredients}
    return {}

@view_config(route_name='find_all', renderer='../templates/find_all.jinja2')
def find_all_with_ingredients(request):
    if 'find_all.submitted' in request.params:
        ingredients = request.params.get('ingredients')
        return_template = {'ingredients': ingredients}
        if ingredients:  # Make sure not none
            ingredients = [i.lower().strip() for i in ingredients.split(',')]
            recipes = find_all_recipes(request.dbsession, ingredients)
            return_template['recipes_found'] = recipes
        return return_template
    return {}

@view_config(route_name='user_page', renderer='../templates/user.jinja2')
def user_page(request):
    return_dict = dict()
    if request.session.get('user'):
        return_dict['logged_in'] = True

    if 'user_form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        permission = validate_user(request.dbsession, login, password)
        if permission == -2:
            message = 'Account does not exist.'
        elif permission == -1:
            message = 'Incorrect password.'
        elif permission >= 0:
            message = 'Successful login'
            request.session['permission'] = permission
            request.session['user'] = login
            return_dict['logged_in'] = True
        else:
            message = 'Unknown error with login.'
        return_dict['message'] = message
        return_dict['login'] = login
        return_dict['password'] = password

    elif 'logout.submitted' in request.params:
        request.session['permission'] = 0
        request.session['user'] = ''
        return_dict['message'] = 'Successfully logged out'
        return_dict['logged_in'] = False

    elif 'new_user.submitted' in request.params:
        return HTTPFound(location=request.route_path('new_user'))

    return return_dict


@view_config(route_name='new_user', renderer='../templates/new_user.jinja2')
def new_user(request):
    secrets = get_secret()
    return_dict = {'google_public': secrets['google']['public']}
    if 'new_user.submitted' in request.params:
        url = 'https://www.google.com/recaptcha/api/siteverify'
        params = {'secret': get_secret()['google']['private'],
                  'response': request.params.get('g-recaptcha-response'),
                  'remoteip': request.remote_addr}
        r = requests.post(url, params=params)
        if r.status_code != 200:
            return_dict['message'] = 'Unknown Error. Try again, I guess.'
            return return_dict
        human = r.json()['success']
        if not human:
            return_dict['message'] = "Try again when you're human"
            return return_dict
        success = add_user(request.dbsession, request.params.get('username'), request.params.get('password'))
        if success == 0:
            return_dict['message'] = 'User already exists, try again'
        elif success == 1:
            return_dict['message'] = 'Successfully added user'
        else:
            return_dict['message'] = 'Unknown Error. Try again, I guess.'

    return return_dict


@view_config(route_name='change_permission', renderer='../templates/change_permission.jinja2')
def change_permission(request):
    if not request.session.get('permission', 0) & 4:  # Can add
        return {'get_out': 'YOU SHOULD NOT BE HERE.'}
    if 'form.submitted' in request.params:
        user = request.params['user']
        permission = int(request.params['permission'])
        success = change_user_permission(request.dbsession, user, permission)
        if success:
            return {'message': 'Success'}
        return {'message': 'Failed'}
    return {}


@view_config(route_name='kitchen', renderer='../templates/kitchen.jinja2')
def kitchen(request):
    user = request.session.get('user')
    if not user:
        return {'get_out': 'YOU SHOULD NOT BE HERE. PLEASE LOG INTO AN ACCOUNT.'}
    if 'update_ingredients.submitted' in request.params:
        checked_ingredients = {ing[0] for ing in request.params.items() if ing[1] == 'on'}
        update_kitchen(request.dbsession, user, checked_ingredients)
        return HTTPFound(location=request.route_path('find_recipes'))
    kitchen_dict = get_all_ingredients(request.dbsession, user)
    return {'kitchen_dict': kitchen_dict}


@view_config(route_name='search_recipe', renderer='../templates/search_recipe.jinja2')
def search_recipe(request):
    recipe = search(request.dbsession, request.params.get('drink', ''))
    return {'recipe': recipe}


@view_config(route_name='add_subtype', renderer='../templates/add_subtype.jinja2')
def add_subtype(request):
    if not request.session.get('permission', 0) & 4:
        return {'get_out': 'YOU SHOULD NOT BE HERE.'}

    if 'add_subtype.submitted' in request.params:
        return_dict = {}
        specific = request.params.get('specific')
        generic = request.params.get('generic')
        return_dict['specific'] = specific
        return_dict['generic'] = generic

        specific_id = request.dbsession.query(Ingredient).filter(Ingredient.name==specific).first()
        generic_id = request.dbsession.query(Ingredient).filter(Ingredient.name==generic).first()

        if not specific_id:
            return_dict['specific_dne'] = True
            return return_dict
        if not generic_id:
            return_dict['generic_dne'] = True
            return return_dict

        if request.dbsession.query(Subtype).filter(Subtype.specific==specific_id.id).first():
            return_dict['specific_already_subtype'] = True
            return return_dict

        new_subtype = Subtype(specific=specific_id.id, generic=generic_id.id)
        request.dbsession.add(new_subtype)
        request.dbsession.flush()

        return_dict['success'] = True
        return return_dict
    return {}

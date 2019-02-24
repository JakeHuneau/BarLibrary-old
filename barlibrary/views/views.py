from pyramid.view import view_config

from .add import add_to_db
from .find import find_recipes, find_all_recipes
from .delete import delete_recipe
from .change_permission import change_user_permission
from ..security import validate_user, add_user
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
    if request.method == 'POST':
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
    if request.method == 'POST':
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

@view_config(route_name='user_page', renderer='../templates/user.jinja2')
def user_page(request):
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
        else:
            message = 'Unknown error with login.'
        return {'message': message,
                'login': login,
                'password': password}
    elif 'logout.submitted' in request.params:
        request.session['permission'] = 0
        request.session['user'] = ''
        return {'message': 'Successfully logged out'}
    elif 'new_user.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        add_success = add_user(request.dbsession, login, password)
        if add_success == -1:
            message = 'Unknown error.'
        elif add_success == 0:
            message = 'User already exists.'
        else:
            message = 'Added user'
        return {'message': message}
    return {}


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

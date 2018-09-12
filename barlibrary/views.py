from pyramid.view import view_config, view_defaults


@view_defaults(route_name='add_recipe')
class RecipeViews:
    def __init__(self, request):
        self.request = request

    @view_config(route_name='home', renderer='templates/home.jinja2')
    def home(self):
        return {}

    @view_config(renderer='templates/add_recipe.jinja2')
    def add_recipe(self):
        return {}

    @view_config(request_method='POST', renderer='template/new_recipe.jinja2')
    def new_recipe(self):
        new_recipe = self.request.params['new_recipe']
        return {'new_recipe': new_recipe}

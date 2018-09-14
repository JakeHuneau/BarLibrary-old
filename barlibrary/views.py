from pyramid.response import Response
from pyramid.view import view_config, view_defaults

from sqlalchemy.exc import DBAPIError


@view_config(route_name='home', renderer='../templates/home.jinja2')
def home_view(request):
    return {}
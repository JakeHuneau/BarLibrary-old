from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from barlibrary.models import Recipe


@view_config(route_name='home', renderer='../templates/home.jinja2')
def home_view(request):
    try:
        query = request.dbsession.query(Recipe)
        one = query.filter_by(name='old fashioned').one()
    except DBAPIError as e:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'one': one, 'project': 'barLibrary'}

db_err_msg = """
uh oh, db bad
"""
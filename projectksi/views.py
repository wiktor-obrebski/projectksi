from pyramid.response import Response
from pyramid_viewscomposer.decorators import compose_view_config
from projectksi.models import tables
from projectksi.models.tables import DBSession
from pyramid.view import view_config


@compose_view_config(route_name='home', renderer='test_template.jinja2')
def my_view(request):
    char = DBSession.query(tables.Character).first()
    val = char.user
    return {'project': val}
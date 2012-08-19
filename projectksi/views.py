from pyramid.view import view_config
from projectksi.models import tables
from projectksi.models.tables import DBSession
import logging

@view_config(route_name='home', renderer='test_template.jinja2')
def my_view(request):
    user = DBSession.query(tables.User).first()
    val = user.email if user else 'empty database'

    return {'project':val}
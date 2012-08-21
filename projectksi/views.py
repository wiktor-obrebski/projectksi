from pyramid_viewscomposer.decorators import compose_view_config
from projectksi.models import tables
from projectksi.models.tables import DBSession
from projectksi import Resource

import logging

@compose_view_config(context=Resource, renderer='test_template.jinja2')
def my_view(request):
    char = DBSession.query(tables.Character).first()
    val = char.user
    return {'project':val}

@compose_view_config(context=Resource, name='second', renderer='test_template.jinja2')
def my_view2(request):
    char = DBSession.query(tables.Character).first()
    val = char.name

    return {'project':val}
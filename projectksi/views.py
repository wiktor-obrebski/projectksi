from pyramid.view import view_config
import logging

@view_config(route_name='home', renderer='test_template.jinja2')
def my_view(request):
    return {'project':'projectksi'}
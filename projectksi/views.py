from pyramid.view import view_config

@view_config(route_name='home', renderer='test_template.jinja2')
def my_view(request):
    request.deps.css('bootstrap')
    request.deps.css('bootstrap-responsive')
    request.deps.less('projectksi')
    request.deps.lib('less')
    request.deps.lib('jquery')

    return {'project':'projectksi'}

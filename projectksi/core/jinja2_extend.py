from jinja2 import contextfunction

def WebDepsIncluder(type):
    @contextfunction
    def include(context, files, **extra_context):
        method = getattr(context['request'].deps, type)
        method(files)
        return ''
    return include
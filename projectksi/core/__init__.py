from pyramid.events import subscriber
from pyramid.interfaces import INewRequest


@subscriber(INewRequest)
def new_requst(event):
    event.request.deps = event.request.registry.PageDeps()
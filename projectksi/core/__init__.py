from pyramid.events import subscriber
from pyramid import interfaces
import transaction

@subscriber(interfaces.INewRequest)
def new_requst(event):
    event.request.deps = event.request.registry.PageDeps()
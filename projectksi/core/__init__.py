from pyramid.events import subscriber
from pyramid import interfaces


@subscriber(interfaces.INewRequest)
def new_requst(event):
    event.request.css = event.request.registry.include_css
    event.request.js = event.request.registry.include_js

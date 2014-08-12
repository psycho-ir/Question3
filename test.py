__author__ = 'soroosh'

from twisted.web import server, resource
from twisted.internet import reactor, endpoints


class Counter(resource.Resource):
    def __index__(self, *args, **kwargs):
        super(Counter, self).__init__(self, args, kwargs)

    def render(self, request):
        print request
        return 'What?'


endpoints.serverFromString(reactor, "tcp:8080").listen(server.Site(Counter()))
reactor.run()

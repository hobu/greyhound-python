

from . import resource

class Server(object):

    def __init__(self, base):
        self.base = str(base)

    def get_resources(self):
        raise Exception("not implemented")

    resources = property(get_resources)

    def get_url(self, name):
        try:
            import urlparse as parse
        except ImportError:
            import urllib.parse as parse

        base = parse.urljoin(self.base, 'resource/')
        base = parse.urljoin(base, name)
        return base

    def get_resource(self, name):
        return resource.Resource(self, name)

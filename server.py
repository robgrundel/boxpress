import cherrypy
class index(object):
    def index(self):
        return "Hello World!"
    index.exposed = True

cherrypy.quickstart(index())
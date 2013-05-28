import cherrypy
from mako.template import Template

class index(object):
    def index(self):
    	mytemplate = Template(filename='/index.html')
	return mytemplate.render()
    index.exposed = True

cherrypy.quickstart(index())
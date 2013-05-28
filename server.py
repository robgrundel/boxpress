import cherrypy
from mako.template import Template
import os.path

current_dir = os.path.dirname(os.path.abspath(__file__))


class Boxpress:
	@cherrypy.expose
    	def index(self):
    		mytemplate = Template(filename='index.html')
		return mytemplate.render()
    	index.exposed = True

if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    conf = {
    		'global' :  {'server.socket_host': '127.0.0.1', 'server.socket_port': 80},
    		'/': {'tools.staticdir.root':  current_dir},
    		'/static': {'tools.staticdir.on':  True,'tools.staticdir.dir': 'static'}
    		}

cherrypy.quickstart(Boxpress(), '/', config=conf)
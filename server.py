import cherrypy
import os.path
from mako.template import Template

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
    		'global' :  {'server.socket_host': '0.0.0.0', 'server.socket_port': int(os.environ.get('PORT', '5000'))},
    		'/': {'tools.staticdir.root':  current_dir},
    		'/static': {'tools.staticdir.on':  True,'tools.staticdir.dir': 'static'}
    		}

cherrypy.quickstart(Boxpress(), '/', config=conf)
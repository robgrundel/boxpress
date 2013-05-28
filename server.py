import cherrypy
import os.path
from mako.template import Template
from cherrypy.process import servers

def fake_wait_for_occupied_port(host, port): return

servers.wait_for_occupied_port = fake_wait_for_occupied_port

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
    		'global' :  {'server.socket_host': '0.0.0.0', 'server.socket_port': 5000},
    		'/': {'tools.staticdir.root':  current_dir},
    		'/static': {'tools.staticdir.on':  True,'tools.staticdir.dir': 'static'}
    		}

cherrypy.quickstart(Boxpress(), '/', config=conf)
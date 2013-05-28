import cherrypy
import os.path
import codecs
import markdown
from mako.template import Template

current_dir = os.path.dirname(os.path.abspath(__file__))

class Boxpress:
  def index(self):
    input_file = codecs.open("how-I-wrote-this-blog.md", mode="r", encoding="utf-8")
    t = input_file.read()
    html = markdown.markdown(t)
    template = Template(filename='index.html')	
    return template.render(content=html)
  index.exposed = True

if __name__ == '__main__':
  current_dir = os.path.dirname(os.path.abspath(__file__))
  conf = {
		'global' :  {'server.socket_host': '0.0.0.0', 'server.socket_port': int(os.environ.get('PORT', '5000'))},
		'/': {'tools.staticdir.root':  current_dir},
		'/static': {'tools.staticdir.on':  True,'tools.staticdir.dir': 'static'}
		}

cherrypy.quickstart(Boxpress(), '/', config=conf)
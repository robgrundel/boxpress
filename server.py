import cherrypy
import os.path
import codecs
import markdown
import re
from mako.template import Template

current_dir = os.path.dirname(os.path.abspath(__file__))

class Boxpress:
  
  def index(self):
    input_file = codecs.open("how-I-wrote-this-blog.md", mode="r", encoding="utf-8")

    metadata = ''
    for x in range(0, 3):
	  metadata = metadata + input_file.readline()
    
    title = self.read_metadata(metadata, 'title')
    date =  self.read_metadata(metadata, 'date')
    tags = self.read_metadata(metadata, 'tags')

    t = ''
    for line in input_file:
    	t = t + line
    html = markdown.markdown(t)

    template = Template(filename='index.html')	
    
    return template.render(content=html, title=title, date=date, tags=tags)
  index.exposed = True
  
  def read_metadata(self, source, key):
    m = re.search('(?<=' + key + ':).*', source)
    return m.group(0)
  	 

if __name__ == '__main__':
  current_dir = os.path.dirname(os.path.abspath(__file__))
  conf = {
		'global' :  {'server.socket_host': '0.0.0.0', 'server.socket_port': int(os.environ.get('PORT', '5000'))},
		'/': {'tools.staticdir.root':  current_dir},
		'/static': {'tools.staticdir.on':  True,'tools.staticdir.dir': 'static'}
		}

cherrypy.quickstart(Boxpress(), '/', config=conf)
import cherrypy
import os.path
import codecs
import markdown
import re
from dropbox import client, rest, session
from mako.template import Template

APP_KEY = 'dzqhhfga39e41xf'
APP_SECRET = '8d2abh3qjg2epwk'

ACCESS_TYPE = 'app_folder'
sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)


current_dir = os.path.dirname(os.path.abspath(__file__))

class Boxpress:
  
  request_token = ''

  def set_dropbox_auth(self, oauth_token, uid):
  	print oauth_token
  	print uid
  	access_token = sess.obtain_access_token(self.request_token)
  	raise cherrypy.HTTPRedirect("/")
  
  	
  
  def index(self):
    try:	
      box_client = client.DropboxClient(sess)
      post, m = box_client.get_file_and_metadata('how-I-wrote-this-blog.md')
    except Exception:
      self.request_token = sess.obtain_request_token()
      url = sess.build_authorize_url(self.request_token, oauth_callback= cherrypy.request.base + '/set_dropbox_auth')
      raise cherrypy.HTTPRedirect(url)
    
    
    # metadata = ''

    # for x in range(0, 3):
	 # metadata = metadata + input_file.readline()
    
    #title = self.read_metadata(metadata, 'title')
    #date =  self.read_metadata(metadata, 'date')
    #tags = self.read_metadata(metadata, 'tags')
    t = post.read()
    
    html = markdown.markdown(t)

    template = Template(filename='index.html')	
    
    return template.render(content=html, title='title', date='date', tags='tags')
  index.exposed = True
  set_dropbox_auth.exposed = True
  
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
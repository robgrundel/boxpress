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
  TOKENS = 'dropbox_token.txt'

  def set_dropbox_auth(self, oauth_token, uid):
  	print oauth_token
  	print uid
  	access_token = sess.obtain_access_token(self.request_token)

  	token_file = open(self.TOKENS,'w')
  	token_file.write("%s|%s" % (access_token.key,access_token.secret) )
  	token_file.close()

  	raise cherrypy.HTTPRedirect("/")
  
    
  def index(self):
    if (os.path.exists(self.TOKENS) == False):
      self.request_token = sess.obtain_request_token()
      url = sess.build_authorize_url(self.request_token, oauth_callback= cherrypy.request.base + '/set_dropbox_auth')
      raise cherrypy.HTTPRedirect(url)
    token_file = open(self.TOKENS)
    token_key,token_secret = token_file.read().split('|')
    token_file.close()

    sess.set_token(token_key,token_secret)
    box_client = client.DropboxClient(sess)

    posts = []

    folder_metadata = box_client.metadata('/')
    for p in folder_metadata['contents']:
      post, m = box_client.get_file_and_metadata(p['path'])
      contents = post.read()
      title = self.read_metadata(contents, 'title')
      date =  self.read_metadata(contents, 'date')
      tags = self.read_metadata(contents, 'tags')
      html = markdown.markdown(self.strip_metadata(contents))
      posts.append({ 'content' : html, 'title' : title, 'date' : date, 'tags' : tags })

    template = Template(filename='index.html')	
    return template.render(posts=posts)
  index.exposed = True
  set_dropbox_auth.exposed = True
  
  def strip_metadata(self, contents):
  	return '\n'.join(contents.split('\n')[3:])

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
import cherrypy
import os.path
import codecs
import markdown
import re
from dropbox import client, rest, session
from mako.template import Template


current_dir = os.path.dirname(os.path.abspath(__file__))

class DropboxSession:
  request_token = ''
  TOKENS = 'dropbox_token.txt'
  APP_KEY = '7nof0ofovo9k6a3'
  APP_SECRET = 'wrt6hw6b369r6o4'
  ACCESS_TYPE = 'app_folder'
  sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)

  def get_client(self):
    return self.client

  def set_auth(self,oauth_token, uid):
    access_token = self.sess.obtain_access_token(self.request_token)
    token_file = open(self.TOKENS,'w')
    token_file.write("%s|%s" % (access_token.key,access_token.secret) )
    token_file.close()
    self.sess.set_token(access_token.key,access_token.secret)
    self.client = client.DropboxClient(self.sess)

  def needs_authentication(self):
    if(os.path.exists(self.TOKENS) == True):
      token_file = open(self.TOKENS)
      token_key,token_secret = token_file.read().split('|')
      token_file.close()
      self.sess.set_token(token_key,token_secret)
      self.client = client.DropboxClient(self.sess)
      return False
    return True

  def get_auth_url(self, path):
    self.request_token = sess.obtain_request_token()
    return sess.build_authorize_url(self.request_token, oauth_callback= cherrypy.request.base + path)


class PostGenerator:

  def strip_metadata(self, contents):
    return '\n'.join(contents.split('\n')[3:])

  def read_metadata(self, source, key):
    m = re.search('(?<=' + key + ':).*', source)
    return m.group(0)

  def generate_post(self,box_client,path):
    post, m = box_client.get_file_and_metadata(path)
    contents = post.read()
    title = self.read_metadata(contents, 'title')
    date =  self.read_metadata(contents, 'date')
    tags = self.read_metadata(contents, 'tags')
    html = markdown.markdown(self.strip_metadata(contents))
    return { 'content' : html, 'title' : title, 'date' : date, 'tags' : tags, 'permalink' : 'post/' + path[1:-3] }

class Post:

  def __init__(self, session):
    self.dropbox_session = session

  def default(self, post):
    generator = PostGenerator()
    post = generator.generate_post(self.dropbox_session.get_client(), '/' + post + '.md')
    template = Template(filename='index.html') 
    return template.render(posts=[post], is_index=False)
  default.exposed = True

class Boxpress: 
  dropbox_session = DropboxSession()
  generator = PostGenerator()

  def set_dropbox_auth(self, oauth_token, uid):  	
    self.dropbox_session.set_auth(oauth_token, uid)
    raise cherrypy.HTTPRedirect("/")

  def index(self):
    if(self.dropbox_session.needs_authentication()):
      raise cherrypy.HTTPRedirect(self.dropbox_session.get_auth_url('/set_dropbox_auth'))

    posts = []

    folder_metadata = self.dropbox_session.get_client().metadata('/')
    for f in folder_metadata['contents']:
      posts.append(self.generator.generate_post(self.dropbox_session.get_client(), f['path']))

    template = Template(filename='index.html')	
    return template.render(posts=posts, is_index=True)
  index.exposed = True
  set_dropbox_auth.exposed = True
  
 
  	 
if __name__ == '__main__':
  current_dir = os.path.dirname(os.path.abspath(__file__))
  conf = {
		'global' :  {'server.socket_host': '0.0.0.0', 'server.socket_port': int(os.environ.get('PORT', '5000'))},
		'/': {'tools.staticdir.root':  current_dir},
		'/static': {'tools.staticdir.on':  True,'tools.staticdir.dir': 'static'}
		}

root = Boxpress()
root.post = Post(root.dropbox_session)
cherrypy.quickstart(root, '/', config=conf)
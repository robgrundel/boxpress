import cherrypy
import datetime
import os.path
import codecs
import markdown
import re
from dropbox import client, rest, session
from mako.template import Template

import dateutil.tz
from dateutil.parser import *
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
    self.request_token = self.sess.obtain_request_token()
    return self.sess.build_authorize_url(self.request_token, oauth_callback= cherrypy.request.base + path)


class PostGenerator:

  def __init__(self, session):
    self.session = session
  
  def strip_metadata(self, contents):
    idx = contents.find('---')
    return contents[idx:]

  def get_metadata(self, contents):
    idx = contents.find('---')
    return contents[:idx]

  def read_metadata(self, source, key):
    m = re.search('(?<=' + key + ':)[^\r\n]*', source)
    return m.group(0).strip()

  def generate_excerpt(self, html):
    m = re.search('<p>[\S\s]*?<\/p>', html)
    return m.group(0).strip()

  def generate_post(self,path):
    post, m = self.session.get_client().get_file_and_metadata(path)
    contents = post.read()
    contents = contents.decode('utf-8')
    metadata = self.get_metadata(contents)
    title = self.read_metadata(metadata, 'title')
    date =  self.read_metadata(metadata, 'date')
    tags = self.read_metadata(metadata, 'tags')
    contents = self.strip_metadata(contents)
    html = markdown.markdown(contents)
    return { 'content' : html, 'title' : title, 'date' : date, 'tags' : tags, 'permalink' : 'post/' + path[1:-3], 'excerpt' : self.generate_excerpt(html) }

class Post:

  def __init__(self, session, generator):
    self.session = session
    self.generator = generator

  def default(self, post):    
    if(self.session.needs_authentication()):
      raise cherrypy.HTTPRedirect(self.session.get_auth_url('/set_dropbox_auth'))

    post = self.generator.generate_post('/' + post + '.md')
    template = Template(filename='index.html') 
    return template.render(posts=[post], is_index=False, is_post=True)
  default.exposed = True

class Boxpress: 
  def __init__(self, session, generator):
    self.session = session
    self.generator = generator

  def set_dropbox_auth(self, oauth_token, uid):  	
    self.session.set_auth(oauth_token, uid)
    raise cherrypy.HTTPRedirect("/")

  def posts(self,page=1):
    if(self.session.needs_authentication()):
      raise cherrypy.HTTPRedirect(self.session.get_auth_url('/set_dropbox_auth'))
    
    client = self.session.get_client()
    posts = []
    contents = sorted(client.metadata('/')['contents'], key=lambda post: parse(post['modified']))
    
    startIdx = (int(page)-1) * 10
    for f in contents[startIdx:startIdx+10]:
      if(f['path'].endswith('.md')):
        posts.append(self.generator.generate_post(f['path']))  

    num_posts = len(contents)
    are_more_posts =  (int(page) * 10) < num_posts
    
    template = Template(filename='index.html')	

    return template.render(posts=posts, is_index=True, is_post=False, are_more_posts=are_more_posts, page=int(page) )
  posts.exposed = True
  set_dropbox_auth.exposed = True
  
 
  	 
if __name__ == '__main__':
  current_dir    = os.path.dirname(os.path.abspath(__file__))
  conf = {
		'global' :  {'server.socket_host': '0.0.0.0', 'server.socket_port': int(os.environ.get('PORT', '5000'))},
		'/': {'tools.staticdir.root':  current_dir},
		'/static': {'tools.staticdir.on':  True,'tools.staticdir.dir': './static'}
		}

dropbox_session = DropboxSession()
generator = PostGenerator(dropbox_session)
root = Boxpress(dropbox_session, generator)
root.index = root.posts
root.post = Post(dropbox_session, generator)
cherrypy.quickstart(root, '/', config=conf)
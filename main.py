import tornado.ioloop
import tornado.web
import tornado
import tornado.httpserver

import re

from SQLiter import *
import Adminka as adm

s = SQLiter()

class MainHandler(tornado.web.RequestHandler):
  def get(self):
    s = SQLiter()
    Posts = s.select_post()
    print(Posts)
    self.render('templates/post.html', Posts=Posts, s=SQLiter)
    
  def get_current_user(self):
    return self.get_secure_cookie("user")
  
class ImportPost(MainHandler):
  def get(self):
    post_url = str(self.request.path)
    post_id = re.search(r"post[0-9]*", str(post_url), flags=0)
    post_id = re.search(r"st[0-9]*", str(post_id))
    post_id = post_id.group(0)[2:]
    post_info = s.post_po_id(post_id)[0]
    comments = s.select_comment(post_id)[::-1]
    print(comments)
    self.render('templates/INpost.html', post_info=post_info, comments=comments)
    
class AddComment(MainHandler):
  @tornado.gen.coroutine
  def post(self):
    comment_text = self.get_argument('comment_text', '')
    print(comment_text)
    post_url = str(self.request.path)
    post_id = re.search(r"post[0-9]*", str(post_url), flags=0)
    post_id = re.search(r"st[0-9]*", str(post_id))
    post_id = post_id.group(0)[2:]
    post_info = s.post_po_id(post_id)[0]
    if self.current_user:
      print(self.current_user)
      s.add_comment(self.current_user, str(comment_text), post_id)
    self.redirect(f"/open_post{post_id}")
    
class ImportRegister(MainHandler):
  def get(self):
    self.render('templates/register.html')
    
class Register(MainHandler):
  def post(self):
    username = self.get_argument("username", '')
    password1 = self.get_argument("password1", '')
    password2 = self.get_argument("password2", '')
    if password1 == password2:
      s.register_user(username, password1)
      self.redirect('/log')
    else:
      self.write('<strong>Error(((</strong>')
    
class ImportLogin(MainHandler):
  def get(self):
    self.render('templates/login.html')
    
class Login(MainHandler):  
  @tornado.gen.coroutine
  def post(self):
    username = self.get_argument("username", '')
    password = self.get_argument("password", '')
    print(username, password)
    users = s.select_user()
    print(users)
    if s.check_user(username, password):
      print(s.check_user_only_name(username))
      self.set_secure_cookie("user",  self.get_argument("username"), expires_days=2)
        
    self.redirect("/")
        
  get = post
  
class Logout(MainHandler):
  def get(self):
    self.clear_cookie("user")
    self.redirect("/")

def make_app():
  return tornado.web.Application([
      (r"/", MainHandler),
      (r"/open_post[0-9]*", ImportPost),
      (r"/open_post[0-9]*/post", AddComment),
      (r"/reg", ImportRegister),
      (r"/register", Register),
      (r"/log", ImportLogin),
      (r"/login", Login),
      (r"/logout", Logout),
      (r'/adminka', adm.Admin),
      (r'/adminka/add_post', adm.ImportAddPost),
      (r"/adminka/add_post/post", adm.Add_post),
      (r"/adminka/regpostlist", adm.ImportRegPostList),
      (r"/adminka/regpost[0-9]*", adm.ImportRegPost),
      (r"/adminka/regpost[0-9]*/post", adm.RegPost),
      # (r"/login", Login),
      # (r"/login/auto", Auto),
  ], cookie_secret="2332ddyffdy89sd69ds6dss6sd8")

if __name__ == "__main__":
  app = make_app()
  app.listen(8080)
  tornado.ioloop.IOLoop.current().start()

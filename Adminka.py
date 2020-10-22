from SQLiter import *
from main import *
import main
import re 

class Admin(main.MainHandler):
  def get(self):
    s = SQLiter()
    Posts = main.s.select_post()
    self.render('templates/adminka.html', Posts=Posts)
    
class ImportAddPost(Admin):
  def get(self):
    self.render('templates/add_post.html')

class Add_post(Admin):
  def post(self):
    try:
      s = SQLiter()
      title_post = self.get_argument('title_post', '')
      text_post = self.get_argument('text_post', '')
      user = self.current_user.decode()
      print(user)
      if [(1,)] == s.check_user_only_name(user):
        s.add_post(title_post, text_post)
        self.redirect('/adminka')
      else:
        print('Error404*_*')
        self.redirect('/adminka')
    except:
      print('Error404*_*')
      self.redirect('/adminka')
    #get = post
    
class ImportRegPostList(Admin):
  def get(self):
    Posts = main.s.select_post()
    self.render('templates/regpostlist.html', Posts=Posts)
    
class ImportRegPost(Admin):
  def get(self):
    post_url = str(self.request.path)
    post_id = re.search(r"regpost[0-9]*", str(post_url), flags=0)
    post_id = re.search(r"st[0-9]*", str(post_id))
    post_id = post_id.group(0)[2:]
    print(post_id)
    post_info = s.post_po_id(post_id)
    print(post_info)
    self.render('templates/regpost.html', post_id=post_id, post_info=post_info[0])
    
class RegPost(Admin):
  def post(self):
    try:
        s = SQLiter()
        title_post = self.get_argument('title_post', '')
        text_post = self.get_argument('text_post', '')
        user = self.current_user.decode()
        post_url = str(self.request.path)
        print(post_url)
        post_id = re.search(r"regpost[0-9]*", str(post_url), flags=0)
        print(post_id)
        post_id = re.search(r"st[0-9]*", str(post_id))
        post_id = post_id.group(0)[2:]
        if [(1,)] == s.check_user_only_name(user):
          s.reg_post(str(post_id), title_post, text_post)
          self.redirect('/adminka')
        else:
          print('Error404*_*')
          self.redirect('/adminka')
    except:
      print('Error404*_*')
      self.redirect('/adminka')
  
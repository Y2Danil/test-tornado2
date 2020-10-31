import sqlite3

class SQLiter:
  def __init__(self):
    self.con = sqlite3.connect('db.sqlite')
    self.cur = self.con.cursor()
    
  def post_po_id(self, post_id):
    with self.con:
      self.cur.execute("SELECT title_post, text_post, id FROM Post WHERE id=?", (str(post_id),))
      result = self.cur.fetchall()
      return result
    
  def select_post(self):
    with self.con:
      self.cur.execute("SELECT title_post, text_post, id FROM Post")
      result = self.cur.fetchall()
      return result
    
  def add_post(self, title_post, text_post=None):
    with self.con:
      return self.cur.execute("INSERT INTO Post(title_post, text_post) VALUES (?, ?)", (title_post, text_post))
    
  def reg_post(self, post_id, title_post, text_post=None):
    with self.con:
      return self.cur.execute("UPDATE Post SET title_post=?, text_post=? WHERE id=?", (title_post, text_post, str(post_id)))
    
  def select_user(self):
    self.cur.execute("SELECT name, password, admin FROM User")
    result = self.cur.fetchall()
    return result
  
  def check_user(self, name, password):
    self.cur.execute("SELECT name, password, admin FROM User WHERE name=? and password=?", (name, password))
    result = self.cur.fetchall()
    return result
  
  def check_user_only_name(self, name):
    self.cur.execute("SELECT admin FROM User WHERE name=?", (name,))
    result = self.cur.fetchall()
    return result
  
  def register_user(self, username, password):
    with self.con:
      return self.cur.execute("INSERT INTO User(name, password) VALUES (?, ?)", (username, password))
    
  def select_comment(self, post_id):
    self.cur.execute("SELECT Author, Text FROM Comment WHERE post_id=?", (post_id, ))
    result = self.cur.fetchall()
    return result
  
  def add_comment(self, author, text, post_id):
    with self.con:
      return self.cur.execute("INSERT INTO Comment(Author, Text, post_id) VALUES (?, ?, ?)", (author, text, post_id))
    
  def close(self):
    return self.con.close()
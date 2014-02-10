import string
import os.path
import datetime
import sys
import time
import XYAPTU
from cStringIO import StringIO
import tools
import urllib
import stat

"""
TODO
  updates and comments...? how...
"""

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
months = [None, "January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]

def makesafe(str):
  str = str.replace("-", "&#45;")
  str = str.replace("$","&#36;")
  return str

class Update:
  type = 'update'
  body = ''
  posttime = 0
  yr = ""
  mo_num = ""
  mo = ""
  da = ""
  dw = ""
  hr = ""
  min = ""
  ISOtime = ""
  timezone = ""
  def __lt__(self, other):
    return self.posttime < other.posttime
  def __le__(self, other):
    return self.posttime <= other.posttime
  def __gt__(self, other):
    return self.posttime > other.posttime
  def __ge__(self, other):
    return self.posttime >= other.posttime
  def __ne__(self, other):
    return self.posttime != other.posttime
  def __eq__(self, other):
    return self.posttime == other.posttime
  

class Comment:
  type = "comment"
  author = ''
  url = ''
  blog_name = ''
  title = ''
  body = ''
  posttime = 0

class Story:
  type = "story"

  def __init__(self, config):
    self.config = config
    self.author = ""
    self.path = "/"
    self.posttime = 0
    self.latestcommentposttime = 0
    self.latestupdateposttime = 0
    self.yr = ""
    self.mo_num = ""
    self.mo = ""
    self.da = ""
    self.dw = ""
    self.hr = ""
    self.min = ""
    self.ISOtime = ""
    self.timezone = ""
    self.title = ""
    self.body = ""
    self.updates = ""
    self.comments = ""
    self.num_comments = 0
    self.comment_str = "Comments"

  def doublejoin(self, p1, p2, p3):
    return os.path.join(os.path.join(p1, p2), p3)

  def writecomment(self):
    commentpath = self.doublejoin(self.config.plugin_state_dir, "comment", self.path[1:])
    if not os.path.exists(commentpath):
      os.makedirs(commentpath, \
          stat.S_IWUSR|stat.S_IRUSR|stat.S_IXUSR| \
          stat.S_IRGRP|stat.S_IWGRP|stat.S_IXGRP| \
          stat.S_IROTH|stat.S_IWOTH|stat.S_IXOTH)
    c = Comment()
    c.author = urllib.unquote(self.config.__dict__["param.comment.author"]).strip()
    c.url = urllib.unquote(self.config.__dict__["param.comment.url"]).strip()
    if self.config.__dict__.has_key("param.comment.blog_name"):
      c.blog_name = urllib.unquote(self.config.__dict__["param.comment.blog_name"]).strip()
    if self.config.__dict__.has_key("param.comment.title"):
      c.title = urllib.unquote(self.config.__dict__["param.comment.title"]).strip()
    else:
      c.title = ''
    c.body = urllib.unquote(self.config.__dict__["param.comment.body"]).strip()
    c.body = '<p class="commentpara">'+c.body.replace("\n", '</p> <p class="commentpara">')+"</p>"
    
    infile = file(os.path.join(commentpath, self.fn+".comment"), "a+")
    infile.write(str(time.time())+"\n")
    infile.write(c.author+"\n")
    infile.write(c.url+"\n")
    infile.write(c.blog_name+"\n")
    infile.write(c.title+"\n")
    infile.write(c.body+"\n")
    infile.close()
    os.chmod(os.path.join(commentpath, self.fn+".comment"),
     stat.S_IWUSR|stat.S_IRUSR|stat.S_IRGRP|stat.S_IWGRP|stat.S_IROTH|stat.S_IWOTH)

  def loadupdates(self):
    filepath = os.path.join(self.config.datadir,self.path[1:])
    files = os.listdir(filepath)
    t_path = tools.find_template(self.config, filepath, "update")
    if t_path == None: return
    updates = []
    for f in files:
      name, ext = os.path.splitext(f)
      if name == self.fn+"."+self.config.file_extension+".update": #and ext is anything
        u = Update()
        u.posttime = os.path.getmtime(os.path.join(filepath, f))
        if u.posttime > self.latestupdateposttime:
          self.latestupdateposttime = u.posttime
        date = datetime.datetime.fromtimestamp(u.posttime)
        u.ISOtime = date.isoformat()
        u.yr = "%0.4d"%(date.year,)
        u.mo_num = "%0.2d"%(date.month,)
        u.mo = months[date.month]
        u.da = "%0.2d"%(date.day,)
        u.dw = days[time.localtime(self.posttime)[6]]
        u.hr = "%0.2d"%(date.hour,)
        u.min = "%0.2d"%(date.minute,)
        u.timezone = date.tzname()
        infile = file(os.path.join(filepath, f))
        u.body = infile.read()
        infile.close()
        DNS = self.DNS
        DNS["update"] = u
        outStream = StringIO()
        xcp = XYAPTU.xcopier(DNS,ouf=outStream)
        xcp.xcopy(t_path)
        self.updates = self.updates+outStream.getvalue()

  def loadcomments(self):
    commentpath = self.doublejoin(self.config.plugin_state_dir, "comment", self.path[1:])
    if os.path.exists(os.path.join(commentpath, self.fn+".comment")):
      #load comments and comment template
      t_path = tools.find_template(self.config, self.path, "comment")
      if t_path == None: return
      infile = file(os.path.join(commentpath, self.fn+".comment"))
      inlines = infile.readlines()
      infile.close()
      #disallow python code
      for i in range(0, len(inlines), 6):
        self.num_comments += 1
        if self.num_comments == 1: self.comment_str = "Comment"
        else: self.comment_str = "Comments"
        outStream = StringIO()
        c = Comment()
        c.posttime = float(inlines[i].strip())
        if c.posttime > self.latestcommentposttime:
          self.latestcommentposttime = c.posttime
        c.author = makesafe(inlines[i+1].strip())
        c.url = makesafe(inlines[i+2].strip())
        c.blog_name = makesafe(inlines[i+3].strip())
        c.title = makesafe(inlines[i+4].strip())
        c.body = makesafe(inlines[i+5].strip())
        DNS={}
        DNS['comment'] = c
        xcp = XYAPTU.xcopier(DNS,ouf=outStream)
        xcp.xcopy(t_path)
        self.comments = self.comments+outStream.getvalue()

  def read(self, path, filename): 
    #self.fn = os.path.splitext(os.path.split(filename)[-1])[0]
    self.fn = os.path.splitext(filename)[0]

    #here's what we need:
    #self.path should be of form /stuf/stuf
    #path should be of form stuf/stuf
    if path == '' or path[0] != os.path.sep:
      self.path = os.path.sep+path
    else:
      self.path = path
      path = path[1:]
    if self.path[-1] != os.path.sep:
      self.path = self.path+os.path.sep
    filepath = self.doublejoin(self.config.datadir,path,filename)
    self.posttime = os.path.getmtime(filepath)
    date = datetime.datetime.fromtimestamp(self.posttime)
    self.ISOtime = date.isoformat()
    self.yr = "%0.4d"%(date.year,)
    self.mo_num = "%0.2d"%(date.month,)
    self.mo = months[date.month]
    self.da = "%0.2d"%(date.day,)
    self.dw = days[time.localtime(self.posttime)[6]]
    self.hr = "%0.2d"%(date.hour,)
    self.min = "%0.2d"%(date.minute,)
    self.timezone = date.tzname()

    infile = file(filepath)
    self.title = infile.readline().strip()
    self.body = infile.read()
    infile.close()

  def getText(self, template, ordinal, DNS):
    self.ordinal = ordinal
    self.DNS = DNS

    DNS['story'] = self
#    sys.stdout = temp
    #last, the comments. note how we don't interpolate on these
    if self.config.__dict__.has_key("param.comment.send"):
      self.writecomment()
    self.loadcomments()

    #now process updates
    self.loadupdates()
    inStream = StringIO(self.updates)
    outStream = StringIO()
    xcp = XYAPTU.xcopier(DNS,ouf=outStream)
    xcp.xcopy(inStream)
    self.updates = outStream.getvalue()
 
    #preprocess the template 
    inStream = StringIO(template)
    outStream = StringIO()
    temp = sys.stdout
    sys.stdout = outStream
    xcp = XYAPTU.xcopier(DNS,ouf=outStream)
    xcp.xcopy(inStream)
    template = outStream.getvalue()

    for var in self.__dict__:
      template = string.replace(template, "story."+var, 
                                "stories["+str(ordinal)+"]."+var)



    return template

  def __lt__(self, other):
    return self.posttime < other.posttime
  def __le__(self, other):
    return self.posttime <= other.posttime
  def __gt__(self, other):
    return self.posttime > other.posttime
  def __ge__(self, other):
    return self.posttime >= other.posttime
  def __ne__(self, other):
    return self.posttime != other.posttime
  def __eq__(self, other):
    return self.posttime == other.posttime

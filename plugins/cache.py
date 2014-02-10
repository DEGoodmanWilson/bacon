import Config
import os.path
from Plugin import Plugin

class Cache:
  def __init__(self):
    self.items = {}
  def read(self):
    try:
      infile = file(os.path.join(Config.plugin_state_path, "story.cache"), 'r')
    except:
      return
    lines = infile.readlines()
    infile.close()
    for line in lines:
      item = line.strip().split('\t')
      self.items[item[0]] = map(int,item[1:])
  def write(self):
    outfile = file(os.path.join(Config.plugin_state_path, "story.cache"), 'w')
    for key in self.items:
      outfile.write("%s\t%d\t%d\t%d\n"%(key,self.items[key][0],self.items[key][1],self.items[key][2]))
    outfile.close()
  def get(self, name): #todo, make this into a dictionary object
    if name in self.items.keys():
      return self.items[name]
    else: return None #and here is the place to insert a hook for pinging sites to alert them to new stories.
  def add(self, name, posttime, updatetime=0, commenttime=0):
    self.items[name] = [posttime,updatetime,commenttime]

class Cacher(Plugin):
  def __init__(self, blog):
    self.type = "Cacher"
    self.blog = blog
    self.cache = Cache()
  def postPreloadContent(self):
    #technically, we could do this in the constructor, but I'd rather do it here.
    self.cache.read()
    changed = False
    for story in blog.children['stories']:
      if self.cache.get(story.path_name) == None:
        #TODO PING SHIT HERE!
        changed = True
        self.cache.add(story.path_name, story.posttime, story.lastupdate, story.lastcomment)
    if changed:
      self.cache.write()

__cacher = Cacher(blog)
blog.cache = __cacher
plugins.append(__cacher)

from Plugin import Plugin
import Config
import os.path

class categories(Plugin):
  type = "categories"
  def __init__(self, blog):
    self.categories = ''
    self.cats = {}
    self.blog = blog

  def recurse(self, dic, prev):
    retval = ''
    keys = dic.keys()
    keys.sort()
    for key in keys:
      test = ''
      if prev == '':
        test = key
        val = self.recurse(dic[key],key)
      else:
        test = prev+'/'+key
        val = self.recurse(dic[key],prev+'/'+key)

      tretval = ''
      if self.blog.path == test:
        tretval = '<li class="this-category">'
        if val == '':
          retval+= tretval+key+'</li>\n'
        else:
          retval+= tretval+key+'\n<ul>'+val+'</ul></li>\n'
      else:
        tretval = '<li><a href="'+Config.url+'/'+test+'">'
        if val == '':
          retval += tretval+key+'</a></li>\n'
        else:
          retval += tretval+key+'</a>\n<ul>'+val+'</ul></li>\n'
    return retval

  def postLoadContent(self):
    cache = self.blog.cache
    for key in cache.cache.items.keys():
      cur = self.cats
      temp = key.split('/')[:-1]
      for cat in temp:
        if not cat in cur.keys():
          cur[cat] = {}
        cur = cur[cat]
    self.categories = '<ul class="categories">\n'
    if self.blog.path == '':
      self.categories += '<li class="this-category">root\n\t<ul>\n'
    else:
      self.categories += '<li><a href="'+Config.url+'">root</a>\n\t<ul>\n'
    self.categories += self.recurse(self.cats, '')
    self.categories += '\t</ul>\n</li></ul>\n'

__categories = categories(blog)
plugins.append(__categories)

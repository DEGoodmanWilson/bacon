from Plugin import Plugin
import string
import Config

def sortfunc(a, b):
  return a.lastcomment - b.lastcomment


class recent(Plugin):
  type = 'recent'

  def __init__(self, blog, form):
    self.blog = blog
    self.recent = False
    if form.getfirst('recent', '') != '':
      blog.item_limit = int(form.getfirst('recent'))
      blog.sortfunc = sortfunc

__recent = recent(blog, opts['form'])
plugins.append(__recent)

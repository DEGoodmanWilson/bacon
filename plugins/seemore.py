from Plugin import Plugin
import string
import Config

class seemore(Plugin):
  type = 'seemore'

  seemoreflavours = ['comments', 'leavewb']

  def __init__(self, blog, form):
    self.blog = blog
    self.seemore = False
    if form.getfirst('seemore', '') == 'y':
      self.seemore = True

  def postLoadContent(self):
    for story in self.blog.children['stories']:
      if '<!-- more -->' in story.body:
        if self.seemore == True or self.blog.flavour in self.seemoreflavours:
          story.body = string.replace(story.body, '<!-- more -->', '<hr class="seemore"/>')
        else:
          i = string.find(story.body, '<!-- more -->')
          story.body = story.body[:i]
          story.body += '\n<a href="'+Config.url+'/'+story.path_name+'.'+self.blog.flavour+'?seemore=y">see more...</a>\n'
        

__seemore = seemore(blog, opts['form'])
plugins.append(__seemore)

#note that this plugin assumes that posts will be in HTML or XHTML format...

from Plugin import Plugin
import sys
import Config
from HTMLParser import HTMLParser
import string

image_base = '/home/dgoodman/www'

class StoryParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.parsedbuffer = ''
  def reset(self):
    HTMLParser.reset(self)
    self.parsedbuffer = ''
  def translate(self, data):
    data = string.replace(data, '&amp;', '&')
    data = string.replace(data, '&', '\\&')
    return data

  def handle_entityref(self, e):
    if e == 'amp': self.parsedbuffer += '\\&'
    elif e == 'mdash': self.parsedbuffer += '--'
  def handle_charref(self, e):
    if e == '36': self.parsedbuffer += '\\$'

  def handle_starttag(self, tag, attrs):
    r = ''
    if tag == 'q':
      r = "``"
    elif tag == 'p':
      r = ''
    elif tag == 'ul':
      r = '\\begin{itemize}\n'
    elif tag == 'li':
      r = '\\item '
    elif tag == 'em' or tag == 'i':
      r = '\\textit{'
    elif tag == 'strong' or tag == 'bold':
      r = '\\textbf{'
    elif tag == 'a':
      for a in attrs:
        if a[0] == 'href':
          self.href = a[1]
          if self.href[0] == '/': self.href = Config.url+self.href
          r = '\\href{'+self.href+'}{'
    elif tag == 'img':
      for a in attrs:
        if a[0] == 'src':
          src = a[1]
          if src[0] == '/':
            r += '\\includegraphics[]{'+image_base+src+'}'
    self.parsedbuffer+=r

  def handle_startendtag(self, tag, attrs):
    if tag == 'img':
      for a in attrs:
        if a[0] == 'src':
          src = a[1]
          if src[0] == '/':
            self.parsedbuffer += '\\includegraphics[]{'+image_base+src+'}'

  def handle_endtag(self, tag):
    r = ''
    if tag == 'q':
      r = "''"
    elif tag == 'p':
      r = '\n'
    elif tag == 'ul':
      r = '\\end{itemize}'
    elif tag == 'li':
      r = '\n'
    elif tag == 'em' or tag == 'i' or tag == 'strong' or tag == 'em':
      r = '}'
    elif tag == 'strong' or tag == 'bold':
      r = '\\textbf{'
    elif tag == 'a':
      r = '}\\footnote{\url{'+self.translate(self.href)+'}}'
    self.parsedbuffer+=r

  def handle_data(self, data):
    self.parsedbuffer+=data

class pdf(Plugin):
  type = "pdf"
  def __init__(self, form, blog):
    self.active = False
    self.blog = blog
    if blog.flavour == 'pdf':
      self.active = True
      import commands
      self.pdflatex = commands.getoutput('which pdflatex')
      if 'no pdflatex in' in self.pdflatex:
        self.active = False
        return
      import os.path, os
      self.uid = commands.getoutput('uuidgen')
      self.path = os.path.join(Config.plugin_state_path, self.type)
      if not os.path.exists(self.path):
        os.makedirs(self.path)
      self.outfile = file(os.path.join(self.path,self.uid+'.latex'), 'w')
      self.tempout = sys.stdout
      sys.stdout = self.outfile
      self.toremove = []

  def postLoadContent(self):
    if self.active == True:
      #TODO processes stories here
      for story in self.blog.children['stories']:
        p = StoryParser()
        p.feed(story.title)
        story.title = p.parsedbuffer
        p.close()
        q = StoryParser()
        q.feed(story.body)
        story.body = q.parsedbuffer
        q.close()
        #TODO process children here....

  def postRender(self):
    if self.active == True:
      import os
      import commands
      self.outfile.close()
      sys.stdout = self.tempout
      commands.getoutput('cd '+self.path+';'+self.pdflatex+' '+self.uid+'.latex')
      infile = file(os.path.join(self.path,self.uid+'.pdf'))
      lines = infile.readlines()
      infile.close()
      for line in lines:
        sys.stdout.write(line)
      os.remove(os.path.join(self.path,self.uid+'.latex'))
      os.remove(os.path.join(self.path,self.uid+'.aux'))
      os.remove(os.path.join(self.path,self.uid+'.log'))
      os.remove(os.path.join(self.path,self.uid+'.out'))
      os.remove(os.path.join(self.path,self.uid+'.pdf'))
      #TODO remove image files, if any

__pdf = pdf(opts['form'], blog)
plugins.append(__pdf)

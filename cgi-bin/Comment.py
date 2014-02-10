"""
Copyright 2005, Donald E. Goodman, Jr.
This file is part of Bacon.

Bacon is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

Bacon is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Bacon; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

import Config
import os.path
from Item import Item
from CommentParser import CommentParser

class Comment(Item):
  def __init__(self, path, filename, flavour=None, opts=None):
    Item.__init__(self, path, filename, flavour, opts)
    self.classType = 'comment'
    self.child_count = 1 #count yerself
    #a Comment has children: threads
    self.children['replies'] = []
    #find children, if any.
    root, ext = os.path.splitext(filename)
    dir = os.listdir(os.path.join(Config.comment_path, path))
    for item in dir:
      i_root, i_ext = os.path.splitext(item)
      i_ext = i_ext[1:] #remove initial '.'
      i_suf, tmp = os.path.splitext(i_root)
      if (i_ext == Config.comment_extension) and (root ==i_suf) and (item != filename):
        self.children['replies'].append(Comment(path, item, flavour, opts))
        self.child_count += self.children['replies'][-1].child_count
    self.lastreply = 0

  #this should do for now
#  def makesafe(self, str):
#    str = str.replace("-", "&#45;")
#    str = str.replace("$","&#36;")
#    return str

  def loadTemplate(self):
    for child in self.children['replies']:
      child.blog = self.blog
      child.story = self.story
      child.parent = self
    Item.loadTemplate(self)

  def preloadContent(self):
    Item.preloadContent(self)
    for reply in self.children['replies']:
      if reply.posttime > self.lastreply:
        self.lastreply = reply.posttime
      if reply.lastreply > self.lastreply:
        self.lastreply = reply.lastreply

  def loadContent(self):
    Item.loadContent(self)
    if not self.__dict__.has_key('title'): #if it hasn't already been loaded
      f = file(os.path.join(os.path.join(Config.comment_path, self.path), self.filename))
#      self.title = self.makesafe(f.readline().strip())
      self.title = f.readline().strip()
      self.author = f.readline().strip()
      self.link = f.readline().strip()
      self.body = ''
      self.blog_name = ''
      lines = f.readlines()
      f.close()
      p = CommentParser()
      for line in lines:
        p.feed(line)
      self.body = p.parsedbuffer
      p.close()

  def render(self):
    return Item.render(self)


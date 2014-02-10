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
from Comment import Comment
from Update import Update
#from CommentParser import CommentParser

class Story(Item):
  def __init__(self, path, filename, flavour=None, opts=None):
    Item.__init__(self, path, filename, flavour, opts)
    self.category = self.path
    self.classType = 'story'
    self.num_comments = 0
    #a Story has children: updates and comments
    self.children['updates'] = []
    self.children['comments'] = []
    #first, see if URL is pointing to an extant story. if not, see if
    #we've been pointed to a comment/reply.
    if not os.path.exists(os.path.join(os.path.join(Config.story_path, self.path), self.filename)):
      found = False
      temp = os.path.splitext(self.filename)[0]
      while temp != self.filename.split('.')[0]:
        temp = os.path.splitext(temp)[0]
        if os.path.exists(os.path.join(os.path.join(Config.story_path, self.path), temp+'.'+Config.story_extension)):
          found = True
          self.filename = temp+'.'+Config.story_extension
          self.name, self.ext = os.path.splitext(self.filename)
          self.path_name = os.path.join(self.path, self.name)
          break
      if found == False:
        self.name = None
        return

    #find children, if any.
    root, ext = os.path.splitext(self.filename)
    if os.path.exists(os.path.join(Config.comment_path, path)):
      dir = os.listdir(os.path.join(Config.comment_path, path))
      for item in dir:
        i_root, i_ext = os.path.splitext(item)
        i_ext = i_ext[1:] #remove initial '.'
        if (i_ext == Config.comment_extension) and (root == os.path.splitext(i_root)[0]):
          self.children['comments'].append(Comment(path, item, flavour, opts))
          self.num_comments += self.children['comments'][-1].child_count

    if os.path.exists(os.path.join(Config.update_path, path)):
      dir = os.listdir(os.path.join(Config.update_path, path))
      for item in dir:
        i_root, i_ext = os.path.splitext(item)
        i_ext = i_ext[1:] #remove initial '.'
        if (i_ext == Config.update_extension) and (root == os.path.splitext(i_root)[0]):
          self.children['updates'].append(Update(path, item, flavour, opts))

  def loadTemplate(self):
    for update in self.children['updates']:
      update.blog = self.blog
      update.story = self
    for comment in self.children['comments']:
      comment.blog = self.blog
      comment.story = self
    Item.loadTemplate(self)

  def preloadContent(self):
    Item.preloadContent(self)
    #get last comment and update from children:
    self.lastupdate = self.lastcomment = 0
    for update in self.children['updates']:
      if update.posttime > self.lastupdate:
        self.lastupdate = update.posttime
    for comment in self.children['comments']:
      if comment.posttime > self.lastcomment:
        self.lastcomment = comment.posttime
      if comment.lastreply > self.lastcomment:
        self.lastcomment = comment.lastreply

  def loadContent(self):
    Item.loadContent(self)
    if not self.__dict__.has_key('title'): #if it hasn't already been loaded
      #might be a comment that's being referred to...need to guess at story name
      #by stripping off extensions
      try:
        f = file(os.path.join(os.path.join(Config.story_path, self.path), self.filename))
      except:
        self.template = ''
        return
      self.title = f.readline().strip()
      self.body = ''
#      p = CommentParser()
      lines = f.readlines()
      f.close()
      for line in lines:
        self.body += line
#        p.feed(line)
#      self.body = p.parsedbuffer
#      p.close()

  def render(self):
    return Item.render(self)


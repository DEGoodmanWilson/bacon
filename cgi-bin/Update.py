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

class Update(Item):
  def __init__(self, path, filename, flavour=None, opts=None):
    Item.__init__(self, path, filename, flavour, opts)
    self.classType = 'update'

  def loadTemplate(self):
    Item.loadTemplate(self)

  def preloadContent(self):
    Item.preloadContent(self)

  def loadContent(self):
    Item.loadContent(self)
    if not self.__dict__.has_key('title'): #if it hasn't already been loaded
      f = file(os.path.join(os.path.join(Config.update_path, self.path), self.filename))
      self.title = f.readline().strip()
      self.body = ''
      line = f.readline()
      while(line != ''):
        self.body += line
        line = f.readline()
      f.close()

  def render(self):
    return Item.render(self)


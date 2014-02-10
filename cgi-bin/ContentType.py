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

from Item import Item

class ContentType(Item):
  def __init__(self, flavor):
    Item.__init__(self, None, None, flavor)
    self.classType = 'content-type'

  def loadTemplate(self):
    Item.loadTemplate(self)

  def render(self):
    return self.template

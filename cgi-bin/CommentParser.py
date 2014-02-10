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

from HTMLParser import HTMLParser
import Config

class CommentParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.parsedbuffer = ''

  def reset(self):
    HTMLParser.reset(self)
    self.parsedbuffer = ''

#  def handle_entityref(self, e):
#  def handle_charref(self, e):

  def handle_starttag(self, tag, attrs):
    r = ''
    if tag in Config.allowed_tags and tag != 'a':
      r = '<'+tag+'>'
    elif tag == 'a' and tag in Config.allowed_tags:
      r = '<a rel="nofollow"'
      for attr in attrs:
        if attr != 'rel':
          r+= ' '+attr[0]+'="'+attr[1]+'"'
      r+= '>'
    self.parsedbuffer += r

  def handle_endtag(self, tag):
    r = ''
    if tag in Config.allowed_tags and tag != 'a':
      r = '</'+tag+'>'
    elif tag == 'a' and tag in Config.allowed_tags:
      r = '</a>'
    self.parsedbuffer += r

  def handle_data(self, data):
    self.parsedbuffer += data

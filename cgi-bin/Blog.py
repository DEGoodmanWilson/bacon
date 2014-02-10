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
from Story import Story
import Local

class Blog(Item):
  def __init__(self, path='', filename=None, flavour=None, opts=None):
    Item.__init__(self, path, filename, flavour, opts)
    self.classType = 'blog'
    self.children['stories'] = []
    #check if a specific date was specified:
    if opts != None and opts.has_key('date'): self.date = opts['date']
    else: self.date = [None,None,None]
    #find children, if any
    if filename != None and filename != 'index.'+Config.story_extension:
      s = Story(self.path, filename, flavour, opts)
      if s.name != None:
        self.children['stories'].append(s)
    else:
      lenp = len(Config.story_path)+1
      for root, dirs, files in os.walk(os.path.join(Config.story_path,self.path)):
        for file in files:
          i_root, i_ext = os.path.splitext(file)
          i_ext = i_ext[1:] #remove initial '.'
          if (i_ext == Config.story_extension):
            self.children['stories'].append(Story(root[lenp:], file, flavour, opts))

    self.item_limit = Config.item_limit
    if opts != None and opts['form'].getfirst('item_limit', '') != '':
      self.item_limit = int(opts['form'].getfirst('item_limit',''))
    self.start = 0
    if opts != None and opts['form'].getfirst('start', '') != '':
      self.start = int(opts['form'].getfirst('start', ''))
    self.post_str = ''
    self.post_str2 = ''
    if opts != None and len(opts['form'].keys()) >0:
      key = opts['form'].keys()[0]
      self.post_str += '?'+key+'='+opts['form'].getfirst(key)
      self.post_str2 += '&'+key+'='+opts['form'].getfirst(key)
      for key in opts['form'].keys()[1:]:
        self.post_str += '&amp;'+key+'='+opts['form'].getfirst(key)
        self.post_str2 += '&amp;'+key+'='+opts['form'].getfirst(key)

  def loadTemplate(self):
    for child in self.children['stories']:
      child.blog = self
    Item.loadTemplate(self)

  def preloadContent(self):
    Item.preloadContent(self)
    #weed out children not on date, if date is set:
    if self.date[0] != None:
      temp = []
      for child in self.children['stories']:
        if int(child.yr) == self.date[0]:
          if self.date[1] == None or self.date[1] == int(child.mo_num):
            if self.date[2] == None or self.date[2] == int(child.da):
              temp.append(child)
      self.children['stories'] = temp
    #reverse sort order
    self.num_stories = len(self.children['stories'])
    self.children['stories'] = self.children['stories'][-(self.start+self.item_limit):(self.num_stories-self.start)]
    self.children['stories'].reverse()
    #set last update time
    if len(self.children['stories']) > 0:
      import datetime
      import time
      import Globals
      self.posttime = self.children['stories'][0].posttime
      date = datetime.datetime.fromtimestamp(self.posttime, Local.Local)
      self.ISOtime = date.isoformat() #TODO: no time set if no stories!
      self.yr = "%0.4d"%(date.year,)
      self.mo_num = "%0.2d"%(date.month,)
      self.mo = Globals.months[date.month]
      self.da = "%0.2d"%(date.day,)
      self.dw = Globals.days[time.localtime(self.posttime)[6]]
      self.hr = "%0.2d"%(date.hour,)
      self.min = "%0.2d"%(date.minute,)
      self.timezone = date.tzname()

  def loadContent(self):
    Item.loadContent(self)

  def render(self):
    return Item.render(self)
